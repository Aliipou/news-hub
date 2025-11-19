"""
Filters router - Provides available filter options.
"""
from fastapi import APIRouter

from backend.models.filters import FiltersResponse, Language, Country, SortOption

router = APIRouter(prefix="/api/filters", tags=["filters"])


# Static filter data based on NewsAPI documentation
CATEGORIES = [
    "business",
    "entertainment",
    "general",
    "health",
    "science",
    "sports",
    "technology"
]

LANGUAGES = [
    Language(code="ar", name="Arabic"),
    Language(code="de", name="German"),
    Language(code="en", name="English"),
    Language(code="es", name="Spanish"),
    Language(code="fr", name="French"),
    Language(code="he", name="Hebrew"),
    Language(code="it", name="Italian"),
    Language(code="nl", name="Dutch"),
    Language(code="no", name="Norwegian"),
    Language(code="pt", name="Portuguese"),
    Language(code="ru", name="Russian"),
    Language(code="sv", name="Swedish"),
    Language(code="zh", name="Chinese")
]

COUNTRIES = [
    Country(code="ae", name="United Arab Emirates"),
    Country(code="ar", name="Argentina"),
    Country(code="at", name="Austria"),
    Country(code="au", name="Australia"),
    Country(code="be", name="Belgium"),
    Country(code="bg", name="Bulgaria"),
    Country(code="br", name="Brazil"),
    Country(code="ca", name="Canada"),
    Country(code="ch", name="Switzerland"),
    Country(code="cn", name="China"),
    Country(code="co", name="Colombia"),
    Country(code="cu", name="Cuba"),
    Country(code="cz", name="Czech Republic"),
    Country(code="de", name="Germany"),
    Country(code="eg", name="Egypt"),
    Country(code="fr", name="France"),
    Country(code="gb", name="United Kingdom"),
    Country(code="gr", name="Greece"),
    Country(code="hk", name="Hong Kong"),
    Country(code="hu", name="Hungary"),
    Country(code="id", name="Indonesia"),
    Country(code="ie", name="Ireland"),
    Country(code="il", name="Israel"),
    Country(code="in", name="India"),
    Country(code="it", name="Italy"),
    Country(code="jp", name="Japan"),
    Country(code="kr", name="South Korea"),
    Country(code="lt", name="Lithuania"),
    Country(code="lv", name="Latvia"),
    Country(code="ma", name="Morocco"),
    Country(code="mx", name="Mexico"),
    Country(code="my", name="Malaysia"),
    Country(code="ng", name="Nigeria"),
    Country(code="nl", name="Netherlands"),
    Country(code="no", name="Norway"),
    Country(code="nz", name="New Zealand"),
    Country(code="ph", name="Philippines"),
    Country(code="pl", name="Poland"),
    Country(code="pt", name="Portugal"),
    Country(code="ro", name="Romania"),
    Country(code="rs", name="Serbia"),
    Country(code="ru", name="Russia"),
    Country(code="sa", name="Saudi Arabia"),
    Country(code="se", name="Sweden"),
    Country(code="sg", name="Singapore"),
    Country(code="si", name="Slovenia"),
    Country(code="sk", name="Slovakia"),
    Country(code="th", name="Thailand"),
    Country(code="tr", name="Turkey"),
    Country(code="tw", name="Taiwan"),
    Country(code="ua", name="Ukraine"),
    Country(code="us", name="United States"),
    Country(code="ve", name="Venezuela"),
    Country(code="za", name="South Africa")
]

SORT_OPTIONS = [
    SortOption(value="publishedAt", label="Latest"),
    SortOption(value="relevancy", label="Most Relevant"),
    SortOption(value="popularity", label="Most Popular")
]


@router.get("", response_model=FiltersResponse)
async def get_filters():
    """
    Get available filter options.

    Returns all available filters for news articles:
    - **categories**: Available news categories
    - **languages**: Supported languages with codes
    - **countries**: Supported countries with codes
    - **sort_options**: Available sorting options

    Use these options to populate filter dropdowns in the frontend.
    """
    return FiltersResponse(
        categories=CATEGORIES,
        languages=LANGUAGES,
        countries=COUNTRIES,
        sort_options=SORT_OPTIONS
    )
