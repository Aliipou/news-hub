"""
Data models for filter options.
"""
from pydantic import BaseModel


class Language(BaseModel):
    """Language option."""
    code: str
    name: str


class Country(BaseModel):
    """Country option."""
    code: str
    name: str


class SortOption(BaseModel):
    """Sort option."""
    value: str
    label: str


class FiltersResponse(BaseModel):
    """Response model for filters endpoint."""
    categories: list[str]
    languages: list[Language]
    countries: list[Country]
    sort_options: list[SortOption]
