import time
from typing import Optional, Tuple

from django.conf import settings
from openai import OpenAI
from openai import APIConnectionError, APIError, RateLimitError, APITimeoutError

from .prompts import build_system_prompt, detect_language


def _get_timeout() -> float:
    try:
        return float(getattr(settings, "OPENAI_TIMEOUT_SECONDS", 30) or 30)
    except (TypeError, ValueError):
        return 30.0


def generate_answer(message: str, context_text: str) -> Tuple[str, str, Optional[int]]:
    api_key = getattr(settings, "OPENAI_API_KEY", "")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    model = getattr(settings, "OPENAI_MODEL", "gpt-5-mini")
    client = OpenAI(api_key=api_key, timeout=_get_timeout())

    language = detect_language(message)
    system_prompt = build_system_prompt(context_text, language)
    last_error = None

    for attempt in range(2):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message},
                ],
                temperature=0,
                top_p=1,
                max_tokens=getattr(settings, "AI_MAX_TOKENS", 220),
            )
            answer = response.choices[0].message.content.strip()
            tokens_used = None
            if response.usage:
                tokens_used = getattr(response.usage, "total_tokens", None)
            return answer, response.model, tokens_used
        except (APITimeoutError, APIConnectionError, APIError, RateLimitError) as error:
            last_error = error
            if attempt == 0:
                time.sleep(0.5)
                continue
            break

    raise RuntimeError(f"OpenAI request failed: {last_error}")
