"""
Data models for news articles.
"""
from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from typing import Optional
from datetime import datetime


class Source(BaseModel):
    """News source information."""
    id: Optional[str] = None
    name: str


class Article(BaseModel):
    """Individual news article model."""
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    source: Source
    author: Optional[str] = None
    title: str
    description: Optional[str] = None
    url: HttpUrl
    url_to_image: Optional[HttpUrl] = Field(None, alias="urlToImage")
    published_at: datetime = Field(alias="publishedAt")
    content: Optional[str] = None


class NewsResponse(BaseModel):
    """Response model for news endpoints."""
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    status: str
    total_results: int = Field(alias="totalResults")
    page: int = 1
    page_size: int = Field(alias="pageSize")
    total_pages: int = Field(alias="totalPages")
    articles: list[Article]
