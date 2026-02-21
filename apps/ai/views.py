import hashlib
import logging
import time

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .models import AssistantLog
from .provider import generate_with_fallback
from .ratelimit import check_rate_limit
from .retrieval import build_context_text


class ChatAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        message = (request.data.get("message") or request.POST.get("message") or "").strip()
        ip_address = request.META.get("REMOTE_ADDR")

        if not message:
            return JsonResponse({"answer": "Message is required."}, status=400)
        if len(message) >= 500:
            return JsonResponse({"answer": "Message is too long."}, status=400)

        if not check_rate_limit(ip_address):
            return JsonResponse({"answer": "AI service is currently unavailable. Please try again."}, status=429)

        context_text = build_context_text(message)

        normalized = " ".join(message.lower().split())
        cache_key = f"ai:answer:{hashlib.sha256(normalized.encode('utf-8')).hexdigest()}"
        cached = cache.get(cache_key)
        if cached:
            return JsonResponse({"answer": cached})
        try:
            start = time.time()
            answer, model_used, tokens_used, provider = generate_with_fallback(message, context_text)
            latency_ms = int((time.time() - start) * 1000)
            AssistantLog.objects.create(
                ip_address=ip_address,
                message=message,
                answer=answer,
                status="ok",
                provider=provider,
                model_used=model_used,
                tokens_used=tokens_used,
                latency_ms=latency_ms,
            )
            cache.set(cache_key, answer, timeout=settings.AI_CACHE_TTL_SECONDS)
            logging.getLogger("apps.ai").info(
                "ai_request provider=%s model=%s tokens=%s latency_ms=%s status=ok",
                provider,
                model_used,
                tokens_used,
                latency_ms,
            )
            return JsonResponse({"answer": answer})
        except Exception as error:
            logging.getLogger("apps.ai").exception(
                "ai_request provider=%s status=error",
                getattr(settings, "AI_PROVIDER", "groq"),
            )
            AssistantLog.objects.create(
                ip_address=ip_address,
                message=message,
                answer=str(error),
                status="error",
            )
            if settings.DEBUG:
                return JsonResponse({"answer": f"DEBUG: {error}"}, status=500)
            return JsonResponse({"answer": "Assistant is temporarily unavailable."}, status=500)
