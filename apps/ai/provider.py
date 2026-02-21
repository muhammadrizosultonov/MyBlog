from django.conf import settings

from django.conf import settings

from .groq_client import generate_answer as groq_generate
from .openai_client import generate_answer as openai_generate


def generate_with_provider(message: str, context_text: str):
    provider = (getattr(settings, "AI_PROVIDER", "groq") or "groq").lower()

    if provider == "openai":
        return openai_generate(message, context_text), "openai"
    return groq_generate(message, context_text), "groq"


def generate_with_fallback(message: str, context_text: str):
    try:
        (answer, model, tokens), provider = generate_with_provider(message, context_text)
        return answer, model, tokens, provider
    except Exception:
        if not getattr(settings, "AI_FALLBACK_ENABLED", False):
            raise

        fallback = "openai" if settings.AI_PROVIDER == "groq" else "groq"
        if fallback == "openai":
            answer, model, tokens = openai_generate(message, context_text)
        else:
            answer, model, tokens = groq_generate(message, context_text)
        return answer, model, tokens, fallback
