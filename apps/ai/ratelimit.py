from django.core.cache import cache


def check_rate_limit(ip_address: str, limit: int = 20, window_seconds: int = 60) -> bool:
    if not ip_address:
        return True
    cache_key = f"ai_rate:{ip_address}"
    rate = cache.get(cache_key, 0)
    if rate >= limit:
        return False
    cache.set(cache_key, rate + 1, timeout=window_seconds)
    return True
