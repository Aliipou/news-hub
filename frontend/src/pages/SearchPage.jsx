/**
 * SearchPage Component
 * Search news with filters
 */
import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { searchNews } from '../services/api';
import SearchBar from '../components/search/SearchBar';
import FilterSidebar from '../components/search/FilterSidebar';
import NewsList from '../components/news/NewsList';
import { NewsListSkeleton } from '../components/news/NewsCardSkeleton';
import ErrorMessage from '../components/common/ErrorMessage';
import Pagination from '../components/pagination/Pagination';
import { useDebounce } from '../hooks/useDebounce';
import { DEFAULT_PAGE_SIZE } from '../utils/constants';
import { cleanParams } from '../utils/helpers';

const SearchPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [hasSearched, setHasSearched] = useState(false);

  const [query, setQuery] = useState(searchParams.get('q') || '');
  const [filters, setFilters] = useState({
    language: searchParams.get('language') || '',
    sortBy: searchParams.get('sortBy') || 'publishedAt',
    fromDate: searchParams.get('from') || '',
    toDate: searchParams.get('to') || '',
  });

  // Debounce query
  const debouncedQuery = useDebounce(query, 800);

  // Fetch search results
  useEffect(() => {
    if (!debouncedQuery.trim()) {
      setArticles([]);
      setHasSearched(false);
      return;
    }

    const fetchSearchResults = async () => {
      setLoading(true);
      setError(null);
      setHasSearched(true);

      try {
        const params = cleanParams({
          q: debouncedQuery,
          language: filters.language,
          from: filters.fromDate,
          to: filters.toDate,
          sortBy: filters.sortBy,
          page: currentPage,
          page_size: DEFAULT_PAGE_SIZE,
        });

        // Update URL params
        setSearchParams(params);

        const data = await searchNews(params);
        setArticles(data.articles || []);
        setTotalPages(data.total_pages || 1);
      } catch (err) {
        setError(err.message || 'Failed to search news');
      } finally {
        setLoading(false);
      }
    };

    fetchSearchResults();
  }, [debouncedQuery, filters, currentPage]);

  const handleSearch = (newQuery) => {
    setQuery(newQuery);
    setCurrentPage(1);
  };

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
    setCurrentPage(1);
  };

  const handleRetry = () => {
    window.location.reload();
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            Search News
          </h1>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            Search through millions of articles from various sources
          </p>

          {/* Search Bar */}
          <SearchBar onSearch={handleSearch} initialQuery={query} />
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Filters Sidebar */}
          <aside className="lg:col-span-1">
            <FilterSidebar
              onFilterChange={handleFilterChange}
              initialFilters={filters}
            />
          </aside>

          {/* Results */}
          <main className="lg:col-span-3">
            {!hasSearched ? (
              <div className="text-center py-12">
                <svg
                  className="mx-auto h-16 w-16 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                  />
                </svg>
                <h3 className="mt-4 text-lg font-medium text-gray-900 dark:text-white">
                  Start your search
                </h3>
                <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
                  Enter a keyword or topic to find relevant news articles
                </p>
              </div>
            ) : loading ? (
              <NewsListSkeleton count={DEFAULT_PAGE_SIZE} />
            ) : error ? (
              <ErrorMessage message={error} onRetry={handleRetry} />
            ) : (
              <>
                {articles.length > 0 && (
                  <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                    Showing results for "<strong>{debouncedQuery}</strong>"
                  </p>
                )}
                <NewsList articles={articles} />
                <Pagination
                  currentPage={currentPage}
                  totalPages={totalPages}
                  onPageChange={setCurrentPage}
                />
              </>
            )}
          </main>
        </div>
      </div>
    </div>
  );
};

export default SearchPage;
