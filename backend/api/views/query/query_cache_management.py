import hashlib
from typing import Optional
from urllib.parse import urlencode

from django.core.cache import cache
from rest_framework.request import Request
from rest_framework.response import Response

TIMEOUT = 60 * 60 * 24

class QueryViewCache:

    cache_key: Optional[str] = None
    search_term_id: Optional[str] = None
    response: Optional[Response] = None

    @staticmethod
    def get_cache_key(request: Request, key_prefix='query'):
        param_string = urlencode(sorted(request.GET.items()))
        hash_key = hashlib.md5(param_string.encode()).hexdigest()
        key = f"{key_prefix}:{hash_key}"

        return key

    def __init__(self, request: Request):
        self.cache_key = QueryViewCache.get_cache_key(request)

    def check_cache_for_response(self) -> bool:
        cached = cache.get(self.cache_key)

        if not cached:
            return False

        # use cached results if present
        search_term_id = cached["search_term_id"]
        response = cached["response"]

        # use cached response
        self.response = Response(**response)
        self.search_term_id = search_term_id

        return True


    def cache_response(self, response: Response, search_term_id) -> None:
        if not self.cache_key:
            raise Exception("Cache key not set")

        # cache results
        cache.set(self.cache_key, {
            "search_term_id": search_term_id,
            "response": {
                "data": response.data,
                "status": response.status_code,
                "headers": response.headers,
            }
        }, timeout=TIMEOUT)