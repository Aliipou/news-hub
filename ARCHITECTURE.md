# News Aggregator - Architecture & Design Document

## 1. System Overview

### 1.1 Application Purpose
A modern, responsive web application that aggregates news from NewsAPI.org, providing users with:
- Real-time top headlines browsing
- Advanced keyword search with filters
- Clean, professional UI/UX
- Fast, cached responses
- Mobile-responsive design

### 1.2 System Architecture (3-Tier)

```
┌──────────────────────────────────────────────────────────┐
│                    Presentation Layer                     │
│                                                            │
│  React 18 + Vite + TailwindCSS                            │
│  - Component-based UI                                      │
│  - Client-side routing (React Router)                     │
│  - State management (React hooks)                         │
│  - Responsive design (mobile-first)                       │
└─────────────────┬────────────────────────────────────────┘
                  │
                  │ REST API (JSON over HTTP)
                  │
┌─────────────────▼────────────────────────────────────────┐
│                    Application Layer                      │
│                                                            │
│  FastAPI (Python 3.11+)                                   │
│  - RESTful API endpoints                                  │
│  - Request validation (Pydantic)                          │
│  - CORS handling                                          │
│  - Error handling & logging                               │
│  - Response caching (in-memory)                           │
└─────────────────┬────────────────────────────────────────┘
                  │
                  │ HTTPS Requests
                  │
┌─────────────────▼────────────────────────────────────────┐
│                    External Service Layer                 │
│                                                            │
│  NewsAPI.org                                              │
│  - Top headlines endpoint                                 │
│  - Everything (search) endpoint                           │
│  - Rate limit: 100 requests/day (free tier)              │
└───────────────────────────────────────────────────────────┘
```

## 2. Technology Stack

### 2.1 Backend Stack

| Technology | Version | Purpose | Justification |
|------------|---------|---------|---------------|
| Python | 3.11+ | Runtime | Modern, async support, type hints |
| FastAPI | 0.104+ | Web Framework | Fast, async, auto docs, type validation |
| Pydantic | 2.0+ | Data Validation | Type safety, automatic validation |
| httpx | 0.25+ | HTTP Client | Async HTTP for NewsAPI calls |
| python-dotenv | 1.0+ | Config Management | Environment variable loading |
| cachetools | 5.3+ | Caching | In-memory TTL cache for API responses |
| pytest | 7.4+ | Testing | Comprehensive test framework |
| pytest-asyncio | 0.21+ | Async Testing | Test async endpoints |

### 2.2 Frontend Stack

| Technology | Version | Purpose | Justification |
|------------|---------|---------|---------------|
| React | 18.2+ | UI Library | Modern, component-based, large ecosystem |
| Vite | 5.0+ | Build Tool | Fast HMR, optimized builds |
| React Router | 6.20+ | Routing | Client-side navigation |
| TailwindCSS | 3.3+ | Styling | Utility-first, responsive, customizable |
| Axios | 1.6+ | HTTP Client | Promise-based, interceptors support |
| Vitest | 1.0+ | Testing | Fast, Vite-native test runner |
| React Testing Library | 14.0+ | Component Testing | User-centric testing |

## 3. Detailed Architecture

### 3.1 Backend Architecture (Layered)

```
┌─────────────────────────────────────────────────────────┐
│                    API Layer (Routers)                   │
│  - Route definitions                                     │
│  - Request/Response models                               │
│  - HTTP status codes                                     │
│  - Input validation                                      │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│                 Service Layer (Business Logic)           │
│  - NewsAPI integration                                   │
│  - Data transformation                                   │
│  - Caching logic                                         │
│  - Error handling                                        │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│                 Utils Layer (Shared)                     │
│  - Configuration management                              │
│  - Constants                                             │
│  - Helper functions                                      │
└─────────────────────────────────────────────────────────┘
```

### 3.2 Frontend Architecture (Component-Based)

```
┌─────────────────────────────────────────────────────────┐
│                    Pages (Route Components)              │
│  HomePage.jsx      - Display top headlines              │
│  SearchPage.jsx    - Search with filters                │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│              Components (Reusable UI)                    │
│  Presentational:                                         │
│    NewsCard       - Single article display               │
│    NewsList       - Grid of articles                     │
│    SearchBar      - Search input                         │
│    FilterSidebar  - Category/language/date filters       │
│    Pagination     - Page navigation                      │
│    Loading        - Loading spinner                      │
│    ErrorMessage   - Error display                        │
│                                                           │
│  Layout:                                                  │
│    Navbar         - App navigation                       │
│    Footer         - Footer info                          │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────┐
│              Services & Hooks                            │
│  api.js          - Axios instance + API calls            │
│  useNews.js      - Custom hook for news fetching         │
│  useDebounce.js  - Debounce hook for search              │
└─────────────────────────────────────────────────────────┘
```

## 4. Folder Structure

### 4.1 Backend Structure

```
backend/
├── main.py                     # FastAPI app initialization
├── routers/                    # API endpoints
│   ├── __init__.py
│   ├── headlines.py           # GET /api/headlines
│   ├── search.py              # GET /api/search
│   └── filters.py             # GET /api/filters
├── services/                   # Business logic
│   ├── __init__.py
│   └── news_api.py            # NewsAPI client + caching
├── models/                     # Pydantic models
│   ├── __init__.py
│   ├── article.py             # Article data model
│   └── filters.py             # Filter options model
├── utils/                      # Shared utilities
│   ├── __init__.py
│   ├── config.py              # Settings management
│   └── cache.py               # Cache implementation
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── test_news_api.py       # Service tests
│   ├── test_headlines.py      # Headlines router tests
│   ├── test_search.py         # Search router tests
│   └── conftest.py            # Pytest fixtures
└── .env.example               # Environment template
```

### 4.2 Frontend Structure

```
frontend/
├── public/
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── common/            # Shared components
│   │   │   ├── Navbar.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── Loading.jsx
│   │   │   └── ErrorMessage.jsx
│   │   ├── news/              # News-specific components
│   │   │   ├── NewsCard.jsx
│   │   │   ├── NewsList.jsx
│   │   │   └── NewsCardSkeleton.jsx
│   │   ├── search/            # Search components
│   │   │   ├── SearchBar.jsx
│   │   │   ├── FilterSidebar.jsx
│   │   │   └── FilterChip.jsx
│   │   └── pagination/
│   │       └── Pagination.jsx
│   ├── pages/
│   │   ├── HomePage.jsx       # Top headlines page
│   │   ├── SearchPage.jsx     # Search results page
│   │   └── NotFoundPage.jsx   # 404 page
│   ├── services/
│   │   └── api.js             # API client
│   ├── hooks/
│   │   ├── useNews.js         # Fetch news data
│   │   ├── useDebounce.js     # Debounce input
│   │   └── useDarkMode.js     # Dark mode toggle
│   ├── utils/
│   │   ├── constants.js       # App constants
│   │   └── helpers.js         # Helper functions
│   ├── App.jsx                # Main app component
│   ├── main.jsx               # Entry point
│   └── index.css              # Global styles
├── tests/
│   ├── components/
│   └── services/
├── package.json
├── vite.config.js
├── tailwind.config.js
└── .env.example
```

## 5. API Design

### 5.1 Endpoint Specifications

#### 5.1.1 GET /api/headlines

**Purpose:** Fetch top headlines

**Query Parameters:**
- `country` (optional): 2-letter country code (e.g., 'us', 'gb')
- `category` (optional): Category filter (business, technology, etc.)
- `page` (optional, default: 1): Page number
- `page_size` (optional, default: 10): Articles per page

**Response (200 OK):**
```json
{
  "status": "ok",
  "total_results": 85,
  "page": 1,
  "page_size": 10,
  "total_pages": 9,
  "articles": [
    {
      "source": {
        "id": "bbc-news",
        "name": "BBC News"
      },
      "author": "John Doe",
      "title": "Article Title",
      "description": "Article description...",
      "url": "https://...",
      "url_to_image": "https://...",
      "published_at": "2024-01-15T10:30:00Z",
      "content": "Article content..."
    }
  ]
}
```

**Error Responses:**
- 400 Bad Request: Invalid parameters
- 500 Internal Server Error: API failure
- 503 Service Unavailable: NewsAPI down

#### 5.1.2 GET /api/search

**Purpose:** Search news articles

**Query Parameters:**
- `q` (required): Search keyword
- `language` (optional): 2-letter language code
- `from_date` (optional): Start date (ISO 8601)
- `to_date` (optional): End date (ISO 8601)
- `sort_by` (optional): relevancy, popularity, publishedAt
- `page` (optional, default: 1)
- `page_size` (optional, default: 10)

**Response:** Same structure as /api/headlines

#### 5.1.3 GET /api/filters

**Purpose:** Get available filter options

**Response (200 OK):**
```json
{
  "categories": [
    "business", "entertainment", "general",
    "health", "science", "sports", "technology"
  ],
  "languages": [
    {"code": "en", "name": "English"},
    {"code": "es", "name": "Spanish"},
    {"code": "fr", "name": "French"}
  ],
  "countries": [
    {"code": "us", "name": "United States"},
    {"code": "gb", "name": "United Kingdom"}
  ],
  "sort_options": [
    {"value": "publishedAt", "label": "Latest"},
    {"value": "relevancy", "label": "Most Relevant"},
    {"value": "popularity", "label": "Most Popular"}
  ]
}
```

#### 5.1.4 GET /health

**Purpose:** Health check endpoint

**Response (200 OK):**
```json
{
  "status": "ok",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0"
}
```

## 6. Data Models

### 6.1 Backend Models (Pydantic)

```python
class Source(BaseModel):
    id: Optional[str]
    name: str

class Article(BaseModel):
    source: Source
    author: Optional[str]
    title: str
    description: Optional[str]
    url: str
    url_to_image: Optional[str]
    published_at: datetime
    content: Optional[str]

class NewsResponse(BaseModel):
    status: str
    total_results: int
    page: int
    page_size: int
    total_pages: int
    articles: List[Article]
```

### 6.2 Frontend Models (TypeScript interfaces, if using TS)

```typescript
interface Article {
  source: {
    id: string | null;
    name: string;
  };
  author: string | null;
  title: string;
  description: string | null;
  url: string;
  urlToImage: string | null;
  publishedAt: string;
  content: string | null;
}

interface NewsResponse {
  status: string;
  totalResults: number;
  page: number;
  pageSize: number;
  totalPages: number;
  articles: Article[];
}
```

## 7. Caching Strategy

### 7.1 Backend Caching

**Implementation:** TTL (Time-To-Live) cache using Python's `cachetools`

**Cache Key Strategy:**
```python
def get_cache_key(endpoint: str, params: dict) -> str:
    # Example: "headlines:country=us:category=tech:page=1"
    sorted_params = sorted(params.items())
    param_str = ":".join(f"{k}={v}" for k, v in sorted_params)
    return f"{endpoint}:{param_str}"
```

**Cache Duration:** 3 minutes (180 seconds)

**Benefits:**
- Reduces NewsAPI calls (100/day limit on free tier)
- Faster response times
- Better user experience

**Cache Invalidation:**
- Automatic TTL expiration
- Manual clear on server restart

### 7.2 Frontend Caching

**Implementation:** React Query (optional) or simple state management

**Strategy:**
- Cache API responses in React state
- Avoid re-fetching on component re-renders
- Refresh on manual user action (search, page change)

## 8. Security Considerations

### 8.1 API Key Protection

**Problem:** NewsAPI key must not be exposed to frontend/public

**Solution:**
1. Store API key in backend `.env` file
2. Add `.env` to `.gitignore`
3. Frontend calls backend proxy, never NewsAPI directly
4. Provide `.env.example` template for setup

### 8.2 CORS Configuration

**Setup:** Allow frontend origins only
```python
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://your-production-domain.com"
]
```

### 8.3 Input Validation

**Backend:**
- Pydantic models validate all inputs
- Reject invalid query parameters
- Sanitize search strings

**Frontend:**
- Client-side validation before API calls
- Prevent empty searches
- Limit input lengths

### 8.4 Rate Limiting (Future Enhancement)

**Implementation:** FastAPI middleware
- Limit requests per IP address
- Prevent abuse of backend API

## 9. UI/UX Design

### 9.1 Design Principles

1. **Minimalist:** Clean, uncluttered interface
2. **Responsive:** Mobile-first design
3. **Fast:** Optimistic UI updates, skeleton loaders
4. **Accessible:** WCAG 2.1 AA compliance
5. **Consistent:** Uniform spacing, typography, colors

### 9.2 Color Palette (TailwindCSS)

```javascript
// Light Mode
{
  primary: 'blue-600',      // #2563eb
  secondary: 'gray-700',    // #374151
  accent: 'indigo-500',     // #6366f1
  background: 'white',      // #ffffff
  surface: 'gray-50',       // #f9fafb
  text: 'gray-900',         // #111827
  textSecondary: 'gray-600' // #4b5563
}

// Dark Mode
{
  primary: 'blue-500',
  secondary: 'gray-300',
  accent: 'indigo-400',
  background: 'gray-900',
  surface: 'gray-800',
  text: 'gray-100',
  textSecondary: 'gray-400'
}
```

### 9.3 Typography

- **Headings:** font-sans (Inter), bold
- **Body:** font-sans, regular
- **Scale:** text-xs to text-4xl (Tailwind scale)

### 9.4 Component States

1. **Loading:** Skeleton loaders (shimmer effect)
2. **Empty:** Friendly "No results" message with icon
3. **Error:** Red banner with retry button
4. **Success:** Smooth fade-in of content

### 9.5 Responsive Breakpoints

```javascript
// Tailwind default breakpoints
sm: '640px',   // Mobile landscape
md: '768px',   // Tablet
lg: '1024px',  // Desktop
xl: '1280px',  // Large desktop
2xl: '1536px'  // Extra large
```

### 9.6 Key UI Components

#### NewsCard Design
```
┌─────────────────────────────────┐
│  [Image]                        │
│                                 │
├─────────────────────────────────┤
│  Article Title (2 lines max)    │
│                                 │
│  Source • 2 hours ago           │
│                                 │
│  Description (3 lines max)...   │
│                                 │
│  [Read More →]                  │
└─────────────────────────────────┘
```

#### FilterSidebar Design
```
┌─────────────────┐
│ Filters         │
├─────────────────┤
│ Category        │
│ ☑ Technology    │
│ ☐ Business      │
│ ☐ Sports        │
│                 │
│ Language        │
│ • English       │
│ ○ Spanish       │
│                 │
│ Sort By         │
│ ▼ Latest        │
│                 │
│ [Apply]         │
└─────────────────┘
```

## 10. Testing Strategy

### 10.1 Backend Testing

**Unit Tests (pytest):**
- Test NewsAPI service methods
- Test cache functionality
- Test data transformation
- Mock external API calls

**Integration Tests:**
- Test full request/response cycle
- Test error handling
- Test pagination logic

**Coverage Target:** >80%

**Test Files:**
```python
# test_news_api.py
def test_fetch_headlines_success()
def test_fetch_headlines_with_cache()
def test_fetch_headlines_api_error()
def test_search_news_with_filters()

# test_routers.py
def test_headlines_endpoint_200()
def test_headlines_endpoint_invalid_params()
def test_search_endpoint_no_query()
```

### 10.2 Frontend Testing

**Unit Tests (Vitest):**
- Test individual components
- Test hooks
- Test utility functions

**Component Tests (React Testing Library):**
- Test user interactions
- Test conditional rendering
- Test API integration

**E2E Tests (Optional - Playwright):**
- Full user flow testing

**Coverage Target:** >70%

**Test Files:**
```javascript
// NewsCard.test.jsx
describe('NewsCard', () => {
  it('renders article data correctly')
  it('opens link in new tab')
  it('handles missing image gracefully')
})

// useNews.test.js
describe('useNews hook', () => {
  it('fetches headlines on mount')
  it('handles errors')
  it('updates on filter change')
})
```

## 11. Performance Optimization

### 11.1 Backend Optimizations

1. **Async Operations:** All I/O operations are async
2. **Response Compression:** Gzip middleware
3. **Caching:** 3-minute TTL cache
4. **Pagination:** Limit data transfer
5. **Connection Pooling:** Reuse HTTP connections

### 11.2 Frontend Optimizations

1. **Code Splitting:** React.lazy() for routes
2. **Image Optimization:** Lazy loading, responsive images
3. **Debouncing:** Search input debounced (500ms)
4. **Memoization:** React.memo for expensive components
5. **Bundle Size:** Tree-shaking with Vite
6. **CDN:** Serve static assets from CDN (production)

### 11.3 Performance Targets

- **Initial Load:** <2 seconds
- **API Response Time:** <500ms (cached), <2s (fresh)
- **Time to Interactive:** <3 seconds
- **Lighthouse Score:** >90

## 12. Error Handling

### 12.1 Backend Error Handling

```python
class NewsAPIError(Exception):
    """Custom exception for NewsAPI errors"""
    pass

# Error response format
{
  "detail": {
    "error": "API_ERROR",
    "message": "Failed to fetch news",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

**Error Types:**
- 400: Invalid request parameters
- 401: Invalid API key (should never reach user)
- 429: Rate limit exceeded
- 500: Internal server error
- 503: NewsAPI unavailable

### 12.2 Frontend Error Handling

**User-Friendly Messages:**
- API Error: "Oops! We couldn't load the news. Please try again."
- Network Error: "No internet connection. Check your network."
- No Results: "No articles found. Try different keywords."
- Invalid Input: "Please enter a search term."

**Error UI:**
- Toast notifications for transient errors
- Full-page error for critical failures
- Retry buttons where appropriate

## 13. Deployment Strategy

### 13.1 Development Environment

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev  # Runs on port 5173
```

### 13.2 Production Deployment

**Backend Options:**
1. **Render.com** (Recommended - Free tier)
2. **Railway.app**
3. **Fly.io**
4. **Heroku**

**Frontend Options:**
1. **Vercel** (Recommended - Free tier)
2. **Netlify**
3. **GitHub Pages** (static build)

**Environment Variables (Production):**
- `NEWS_API_KEY`: Your NewsAPI key
- `CORS_ORIGINS`: Production frontend URL
- `DEBUG`: false

### 13.3 CI/CD Pipeline (Optional)

**GitHub Actions:**
1. Run tests on pull requests
2. Build frontend bundle
3. Deploy on merge to main

## 14. Development Workflow

### Phase 1: Setup (Day 1)
1. Initialize Git repository
2. Create backend folder structure
3. Set up FastAPI with basic routes
4. Create frontend with Vite + React
5. Configure Tailwind CSS
6. Test backend-frontend connection

### Phase 2: Core Features (Day 2-3)
1. Implement NewsAPI service
2. Create headlines endpoint
3. Create search endpoint
4. Build HomePage component
5. Build SearchPage component
6. Implement NewsCard component

### Phase 3: Advanced Features (Day 4-5)
1. Add filters functionality
2. Implement pagination
3. Add caching
4. Create FilterSidebar component
5. Add loading states
6. Implement error handling

### Phase 4: Polish & Testing (Day 6)
1. Write backend tests
2. Write frontend tests
3. Add dark mode
4. Improve responsive design
5. Add animations/transitions
6. Fix bugs

### Phase 5: Documentation & Deployment (Day 7)
1. Write comprehensive README
2. Add code comments
3. Create .env.example files
4. Deploy backend
5. Deploy frontend
6. Final testing

## 15. Success Metrics

### 15.1 Functional Requirements
- ✅ Display top headlines
- ✅ Search functionality
- ✅ Filters (category, language, country)
- ✅ Pagination
- ✅ Responsive design
- ✅ Error handling
- ✅ API key security

### 15.2 Non-Functional Requirements
- ✅ Load time <2s
- ✅ Mobile-responsive (all breakpoints)
- ✅ Clean code structure
- ✅ >80% test coverage
- ✅ Comprehensive documentation
- ✅ Deployable to production

### 15.3 Bonus Features
- ⭐ Dark mode toggle
- ⭐ Skeleton loaders
- ⭐ Search debouncing
- ⭐ Favorites (localStorage)
- ⭐ Share functionality
- ⭐ Reading time estimate

---

## 16. Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| NewsAPI rate limit exceeded | High | Implement caching, limit requests |
| API key exposure | Critical | Use backend proxy, .gitignore |
| Slow API responses | Medium | Add caching, show loading states |
| Mobile compatibility issues | Medium | Mobile-first design, test on devices |
| Browser compatibility | Low | Use modern browsers only, polyfills if needed |

---

**This architecture ensures:**
✅ Scalability
✅ Maintainability
✅ Security
✅ Performance
✅ Testability
✅ Professional quality

Ready for implementation!
