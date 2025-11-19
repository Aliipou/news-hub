"""
Unit tests for NewsAPI service
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from backend.services.news_api import NewsAPIService, NewsAPIError
import httpx


@pytest.mark.asyncio
class TestNewsAPIService:
    """Test cases for NewsAPIService"""

    @pytest.fixture
    def service(self):
        """Create a NewsAPIService instance"""
        return NewsAPIService()

    @pytest.fixture
    def mock_successful_response(self, mock_news_response):
        """Mock successful HTTP response"""
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = mock_news_response
        return response

    async def test_get_top_headlines_success(self, service, mock_successful_response):
        """Test successful fetch of top headlines"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_instance = AsyncMock()
            mock_instance.__aenter__.return_value.get = AsyncMock(
                return_value=mock_successful_response
            )
            mock_client.return_value = mock_instance

            result = await service.get_top_headlines(country='us', page=1, page_size=10)

            assert result.status == 'ok'
            assert len(result.articles) == 2
            assert result.total_results == 38
            assert result.page == 1
            assert result.total_pages == 4  # 38 / 10 = 4 pages

    async def test_get_top_headlines_with_category(self, service, mock_successful_response):
        """Test headlines with category filter"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_instance = AsyncMock()
            mock_instance.__aenter__.return_value.get = AsyncMock(
                return_value=mock_successful_response
            )
            mock_client.return_value = mock_instance

            result = await service.get_top_headlines(
                country='us',
                category='technology',
                page=1,
                page_size=10
            )

            assert result.status == 'ok'
            assert len(result.articles) == 2

    async def test_get_top_headlines_cache(self, service, mock_successful_response):
        """Test that caching works for headlines"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_instance = AsyncMock()
            mock_get = AsyncMock(return_value=mock_successful_response)
            mock_instance.__aenter__.return_value.get = mock_get
            mock_client.return_value = mock_instance

            # First call - should hit API
            result1 = await service.get_top_headlines(country='us')
            # Second call - should use cache
            result2 = await service.get_top_headlines(country='us')

            # API should only be called once
            assert mock_get.call_count == 1
            assert result1.total_results == result2.total_results

    async def test_search_news_success(self, service, mock_successful_response):
        """Test successful news search"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_instance = AsyncMock()
            mock_instance.__aenter__.return_value.get = AsyncMock(
                return_value=mock_successful_response
            )
            mock_client.return_value = mock_instance

            result = await service.search_news(
                query='bitcoin',
                language='en',
                sort_by='publishedAt',
                page=1,
                page_size=10
            )

            assert result.status == 'ok'
            assert len(result.articles) == 2

    async def test_search_news_empty_query(self, service):
        """Test search with empty query raises error"""
        with pytest.raises(NewsAPIError) as exc_info:
            await service.search_news(query='', page=1, page_size=10)

        assert 'empty' in str(exc_info.value).lower()

    async def test_api_error_401(self, service):
        """Test handling of 401 Unauthorized error"""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"message": "Invalid API key"}

        with patch('httpx.AsyncClient') as mock_client:
            mock_instance = AsyncMock()
            mock_instance.__aenter__.return_value.get = AsyncMock(
                return_value=mock_response
            )
            mock_client.return_value = mock_instance

            with pytest.raises(NewsAPIError) as exc_info:
                await service.get_top_headlines()

            assert 'Invalid API key' in str(exc_info.value)

    async def test_api_error_429(self, service):
        """Test handling of 429 Rate Limit error"""
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.json.return_value = {"message": "Rate limit exceeded"}

        with patch('httpx.AsyncClient') as mock_client:
            mock_instance = AsyncMock()
            mock_instance.__aenter__.return_value.get = AsyncMock(
                return_value=mock_response
            )
            mock_client.return_value = mock_instance

            with pytest.raises(NewsAPIError) as exc_info:
                await service.get_top_headlines()

            assert 'Rate limit exceeded' in str(exc_info.value)

    async def test_network_timeout(self, service):
        """Test handling of network timeout"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_instance = AsyncMock()
            mock_instance.__aenter__.return_value.get = AsyncMock(
                side_effect=httpx.TimeoutException("Request timeout")
            )
            mock_client.return_value = mock_instance

            with pytest.raises(NewsAPIError) as exc_info:
                await service.get_top_headlines()

            assert 'timeout' in str(exc_info.value).lower()

    async def test_network_error(self, service):
        """Test handling of network errors"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_instance = AsyncMock()
            mock_instance.__aenter__.return_value.get = AsyncMock(
                side_effect=httpx.RequestError("Network error")
            )
            mock_client.return_value = mock_instance

            with pytest.raises(NewsAPIError) as exc_info:
                await service.get_top_headlines()

            assert 'Network error' in str(exc_info.value)

    def test_cache_clear(self, service):
        """Test cache clearing functionality"""
        service.cache.set('test', {'key': 'value'}, {'data': 'test'})
        assert service.cache.size() == 1

        service.clear_cache()
        assert service.cache.size() == 0

    def test_cache_stats(self, service):
        """Test cache statistics"""
        stats = service.get_cache_stats()

        assert 'size' in stats
        assert 'max_size' in stats
        assert 'ttl_seconds' in stats
        assert stats['max_size'] == 100
