import json
import time
from typing import Optional, Tuple

import requests
from django.conf import settings

from .prompts import build_system_prompt, detect_language

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def _get_timeout() -> float:
    try:
        return float(getattr(settings, "GROQ_TIMEOUT_SECONDS", 30) or 30)
    except (TypeError, ValueError):
        return 30.0


def generate_answer(message: str, context_text: str) -> Tuple[str, str, Optional[int]]:
    api_key = getattr(settings, "GROQ_API_KEY", "")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set.")

    model = getattr(settings, "GROQ_MODEL", "llama3-8b-8192")
    language = detect_language(message)
    system_prompt = build_system_prompt(context_text, language)

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ],
        "temperature": 0,
        "top_p": 1,
        "max_tokens": getattr(settings, "AI_MAX_TOKENS", 220),
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    last_error = None
    for attempt in range(2):
        try:
            response = requests.post(
                GROQ_URL,
                headers=headers,
                data=json.dumps(payload),
                timeout=_get_timeout(),
            )
            if response.status_code < 200 or response.status_code >= 300:
                raise RuntimeError(
                    f"Groq API error: {response.status_code} {response.text}"
                )

            data = response.json()
            answer = data["choices"][0]["message"]["content"].strip()
            tokens_used = None
            usage = data.get("usage")
            if usage:
                tokens_used = usage.get("total_tokens")
            model_used = data.get("model", model)
            return answer, model_used, tokens_used
        except (requests.RequestException, ValueError, KeyError, RuntimeError) as error:
            last_error = error
            if attempt == 0:
                time.sleep(0.5)
                continue
            break

    raise RuntimeError(f"Groq request failed: {last_error}")
