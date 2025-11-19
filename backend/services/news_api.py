"""
NewsAPI service layer.
Handles all interactions with the NewsAPI.org external service.
"""
import httpx
from typing import Optional, Dict, Any
from datetime import datetime
import math

from backend.utils.config import get_settings
from backend.utils.cache import NewsCache
from backend.models.article import NewsResponse, Article


class NewsAPIError(Exception):
    """Custom exception for NewsAPI errors."""
    pass


class NewsAPIService:
    """
    Service for interacting with NewsAPI.org.
    Implements caching and error handling.
    """

    def __init__(self):
        """Initialize the NewsAPI service with settings and cache."""
        self.settings = get_settings()
        self.base_url = self.settings.news_api_base_url
        self.api_key = self.settings.news_api_key
        self.cache = NewsCache(ttl=self.settings.cache_ttl)

    async def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make an HTTP request to NewsAPI.

        Args:
            endpoint: API endpoint (e.g., 'top-headlines', 'everything')
            params: Query parameters

        Returns:
            JSON response from NewsAPI

        Raises:
            NewsAPIError: If the API request fails
        """
        # Add API key to parameters
        params['apiKey'] = self.api_key

        url = f"{self.base_url}/{endpoint}"

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)

                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    raise NewsAPIError("Invalid API key")
                elif response.status_code == 429:
                    raise NewsAPIError("Rate limit exceeded")
                else:
                    error_data = response.json()
                    message = error_data.get('message', 'Unknown error')
                    raise NewsAPIError(f"NewsAPI error: {message}")

        except httpx.TimeoutException:
            raise NewsAPIError("Request timeout - NewsAPI is taking too long to respond")
        except httpx.RequestError as e:
            raise NewsAPIError(f"Network error: {str(e)}")

    def _transform_response(
        self,
        data: Dict[str, Any],
        page: int,
        page_size: int
    ) -> NewsResponse:
        """
        Transform NewsAPI response to our standardized format.

        Args:
            data: Raw NewsAPI response
            page: Current page number
            page_size: Items per page

        Returns:
            Standardized NewsResponse object
        """
        total_results = data.get('totalResults', 0)
        total_pages = math.ceil(total_results / page_size) if total_results > 0 else 0

        articles = data.get('articles', [])

        return NewsResponse(
            status=data.get('status', 'ok'),
            totalResults=total_results,
            page=page,
            pageSize=page_size,
            totalPages=total_pages,
            articles=articles
        )

    async def get_top_headlines(
        self,
        country: Optional[str] = None,
        category: Optional[str] = None,
        page: int = 1,
        page_size: int = 10
    ) -> NewsResponse:
        """
        Fetch top headlines from NewsAPI.

        Args:
            country: 2-letter country code (e.g., 'us', 'gb')
            category: Category filter (business, technology, etc.)
            page: Page number (1-indexed)
            page_size: Number of articles per page

        Returns:
            NewsResponse with articles

        Raises:
            NewsAPIError: If the API request fails
        """
        # Build cache key parameters
        cache_params = {
            'country': country or 'us',  # Default to US
            'category': category,
            'page': page,
            'pageSize': page_size
        }

        # Check cache
        cached = self.cache.get('headlines', cache_params)
        if cached:
            return NewsResponse(**cached)

        # Build API request parameters
        params = {'pageSize': page_size, 'page': page}

        if country:
            params['country'] = country
        else:
            params['country'] = 'us'  # Default country

        if category:
            params['category'] = category

        # Make API request
        data = await self._make_request('top-headlines', params)

        # Transform response
        response = self._transform_response(data, page, page_size)

        # Cache the result
        self.cache.set('headlines', cache_params, response.model_dump())

        return response

    async def search_news(
        self,
        query: str,
        language: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        sort_by: str = 'publishedAt',
        page: int = 1,
        page_size: int = 10
    ) -> NewsResponse:
        """
        Search news articles by keyword.

        Args:
            query: Search keyword (required)
            language: 2-letter language code (e.g., 'en', 'es')
            from_date: Start date (ISO 8601 format)
            to_date: End date (ISO 8601 format)
            sort_by: Sort option (relevancy, popularity, publishedAt)
            page: Page number (1-indexed)
            page_size: Number of articles per page

        Returns:
            NewsResponse with articles

        Raises:
            NewsAPIError: If the API request fails
        """
        if not query or query.strip() == '':
            raise NewsAPIError("Search query cannot be empty")

        # Build cache key parameters
        cache_params = {
            'q': query,
            'language': language,
            'from': from_date,
            'to': to_date,
            'sortBy': sort_by,
            'page': page,
            'pageSize': page_size
        }

        # Check cache
        cached = self.cache.get('search', cache_params)
        if cached:
            return NewsResponse(**cached)

        # Build API request parameters
        params = {
            'q': query,
            'sortBy': sort_by,
            'pageSize': page_size,
            'page': page
        }

        if language:
            params['language'] = language

        if from_date:
            params['from'] = from_date

        if to_date:
            params['to'] = to_date

        # Make API request
        data = await self._make_request('everything', params)

        # Transform response
        response = self._transform_response(data, page, page_size)

        # Cache the result
        self.cache.set('search', cache_params, response.model_dump())

        return response

    def clear_cache(self) -> None:
        """Clear all cached responses."""
        self.cache.clear()

    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        return {
            'size': self.cache.size(),
            'max_size': 100,
            'ttl_seconds': self.settings.cache_ttl
        }
