"""
Headlines router - Handles top headlines requests.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from backend.services.news_api import NewsAPIService, NewsAPIError
from backend.models.article import NewsResponse

router = APIRouter(prefix="/api/headlines", tags=["headlines"])


@router.get("", response_model=NewsResponse)
async def get_headlines(
    country: Optional[str] = Query(
        None,
        description="2-letter ISO country code (e.g., us, gb, ca)",
        max_length=2,
        pattern="^[a-z]{2}$"
    ),
    category: Optional[str] = Query(
        None,
        description="News category",
        pattern="^(business|entertainment|general|health|science|sports|technology)$"
    ),
    page: int = Query(
        1,
        ge=1,
        description="Page number (1-indexed)"
    ),
    page_size: int = Query(
        10,
        ge=1,
        le=100,
        description="Number of articles per page (max 100)"
    )
):
    """
    Get top headlines.

    Fetches the latest top headlines from NewsAPI with optional filters.

    - **country**: Filter by country (2-letter code)
    - **category**: Filter by category (business, entertainment, etc.)
    - **page**: Page number for pagination
    - **page_size**: Number of articles per page (1-100)

    Returns a paginated list of news articles.
    """
    try:
        service = NewsAPIService()
        response = await service.get_top_headlines(
            country=country,
            category=category,
            page=page,
            page_size=page_size
        )
        return response

    except NewsAPIError as e:
        raise HTTPException(status_code=500, detail={
            "error": "API_ERROR",
            "message": str(e)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "error": "INTERNAL_ERROR",
            "message": "An unexpected error occurred"
        })
