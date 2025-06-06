from functools import wraps
from typing import Optional

from django.core.cache import cache
from rest_framework.response import Response

TIMEOUT = 60 * 60 * 24
RECENT_SEARCH="recent_search"
FREQUENT_SEARCH="frequent_search"

def get_hash_key(query_type:str) -> str:
    return f'searches:{query_type}'

def save_to_cache(query_type: str, response: Response) -> None:
    key = get_hash_key(query_type)
    cache.set(key, {
        "data": response.data,
        "status": response.status_code,
        "headers": response.headers,
    }, timeout=TIMEOUT)

def get_from_cache(query_type: str) ->  Optional[Response]:
    key = get_hash_key(query_type)
    data = cache.get(key)

    if not data:
        return None

    return Response(**data)

def eject_from_cache(query_type: str) -> None:
    key = get_hash_key(query_type)
    cache.delete(key)


def invalidate_recent_search_cache() -> None:
    eject_from_cache(RECENT_SEARCH)


def cache_response(query_type: str, timeout: int = 60 * 60):
    def decorator(view_method):
        @wraps(view_method)
        def wrapper(self, request, *args, **kwargs):
            cached = get_from_cache(query_type)
            if cached:
                return cached
            response: Response = view_method(self, request, *args, **kwargs)
            save_to_cache(query_type, response)
            return response
        return wrapper
    return decorator


