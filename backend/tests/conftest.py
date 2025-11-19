"""
Pytest configuration and fixtures
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def mock_news_response():
    """Mock NewsAPI response data"""
    return {
        "status": "ok",
        "totalResults": 38,
        "articles": [
            {
                "source": {"id": "bbc-news", "name": "BBC News"},
                "author": "John Doe",
                "title": "Test Article Title",
                "description": "This is a test article description",
                "url": "https://example.com/article1",
                "urlToImage": "https://example.com/image1.jpg",
                "publishedAt": "2024-01-15T10:30:00Z",
                "content": "Test article content"
            },
            {
                "source": {"id": None, "name": "Tech News"},
                "author": "Jane Smith",
                "title": "Another Test Article",
                "description": "Another test description",
                "url": "https://example.com/article2",
                "urlToImage": None,
                "publishedAt": "2024-01-15T09:00:00Z",
                "content": "More test content"
            }
        ]
    }
