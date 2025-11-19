"""
Caching utility for API responses.
"""
from cachetools import TTLCache
from typing import Any, Optional
import hashlib
import json


class NewsCache:
    """
    TTL-based cache for NewsAPI responses.
    Helps reduce API calls and improve response times.
    """

    def __init__(self, ttl: int = 180, maxsize: int = 100):
        """
        Initialize cache with TTL and max size.

        Args:
            ttl: Time-to-live in seconds (default: 180s = 3 minutes)
            maxsize: Maximum number of cached items (default: 100)
        """
        self._cache = TTLCache(maxsize=maxsize, ttl=ttl)

    def _generate_key(self, endpoint: str, params: dict) -> str:
        """
        Generate a unique cache key from endpoint and parameters.

        Args:
            endpoint: API endpoint name
            params: Query parameters dictionary

        Returns:
            Unique cache key string
        """
        # Sort params for consistent key generation
        sorted_params = sorted(params.items())
        param_str = json.dumps(sorted_params, sort_keys=True)

        # Create hash for long parameter strings
        param_hash = hashlib.md5(param_str.encode()).hexdigest()

        return f"{endpoint}:{param_hash}"

    def get(self, endpoint: str, params: dict) -> Optional[Any]:
        """
        Get cached response if available.

        Args:
            endpoint: API endpoint name
            params: Query parameters dictionary

        Returns:
            Cached response or None if not found
        """
        key = self._generate_key(endpoint, params)
        return self._cache.get(key)

    def set(self, endpoint: str, params: dict, value: Any) -> None:
        """
        Store response in cache.

        Args:
            endpoint: API endpoint name
            params: Query parameters dictionary
            value: Response data to cache
        """
        key = self._generate_key(endpoint, params)
        self._cache[key] = value

    def clear(self) -> None:
        """Clear all cached items."""
        self._cache.clear()

    def size(self) -> int:
        """Get current number of cached items."""
        return len(self._cache)
