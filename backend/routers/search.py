"""
Search router - Handles news search requests.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from backend.services.news_api import NewsAPIService, NewsAPIError
from backend.models.article import NewsResponse

router = APIRouter(prefix="/api/search", tags=["search"])


@router.get("", response_model=NewsResponse)
async def search_news(
    q: str = Query(
        ...,
        description="Search query (keyword or phrase)",
        min_length=1,
        max_length=500
    ),
    language: Optional[str] = Query(
        None,
        description="2-letter ISO language code (e.g., en, es, fr)",
        max_length=2,
        pattern="^[a-z]{2}$"
    ),
    from_date: Optional[str] = Query(
        None,
        alias="from",
        description="Start date (ISO 8601 format: YYYY-MM-DD)",
        pattern="^\\d{4}-\\d{2}-\\d{2}$"
    ),
    to_date: Optional[str] = Query(
        None,
        alias="to",
        description="End date (ISO 8601 format: YYYY-MM-DD)",
        pattern="^\\d{4}-\\d{2}-\\d{2}$"
    ),
    sort_by: str = Query(
        "publishedAt",
        description="Sort order",
        pattern="^(relevancy|popularity|publishedAt)$"
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
    Search news articles by keyword.

    Search through millions of articles from NewsAPI.

    - **q**: Search query (required)
    - **language**: Filter by language (2-letter code)
    - **from**: Start date for articles (YYYY-MM-DD)
    - **to**: End date for articles (YYYY-MM-DD)
    - **sort_by**: Sort order (relevancy, popularity, publishedAt)
    - **page**: Page number for pagination
    - **page_size**: Number of articles per page (1-100)

    Returns a paginated list of matching articles.
    """
    try:
        service = NewsAPIService()
        response = await service.search_news(
            query=q,
            language=language,
            from_date=from_date,
            to_date=to_date,
            sort_by=sort_by,
            page=page,
            page_size=page_size
        )
        return response

    except NewsAPIError as e:
        if "empty" in str(e).lower():
            raise HTTPException(status_code=400, detail={
                "error": "INVALID_QUERY",
                "message": str(e)
            })
        raise HTTPException(status_code=500, detail={
            "error": "API_ERROR",
            "message": str(e)
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail={
            "error": "INTERNAL_ERROR",
            "message": "An unexpected error occurred"
        })
