/**
 * HomePage Component
 * Displays top headlines with category filters
 */
import { useState, useEffect } from 'react';
import { getHeadlines, getFilters } from '../services/api';
import NewsList from '../components/news/NewsList';
import { NewsListSkeleton } from '../components/news/NewsCardSkeleton';
import Loading from '../components/common/Loading';
import ErrorMessage from '../components/common/ErrorMessage';
import Pagination from '../components/pagination/Pagination';
import { DEFAULT_PAGE_SIZE } from '../utils/constants';

const HomePage = () => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [categories, setCategories] = useState([]);

  // Load filter options
  useEffect(() => {
    const loadCategories = async () => {
      try {
        const data = await getFilters();
        setCategories(data.categories || []);
      } catch (err) {
        console.error('Failed to load categories:', err);
      }
    };
    loadCategories();
  }, []);

  // Fetch headlines
  useEffect(() => {
    const fetchHeadlines = async () => {
      setLoading(true);
      setError(null);

      try {
        const params = {
          page: currentPage,
          page_size: DEFAULT_PAGE_SIZE,
        };

        if (selectedCategory) {
          params.category = selectedCategory;
        }

        const data = await getHeadlines(params);
        setArticles(data.articles || []);
        setTotalPages(data.total_pages || 1);
      } catch (err) {
        setError(err.message || 'Failed to load headlines');
      } finally {
        setLoading(false);
      }
    };

    fetchHeadlines();
  }, [currentPage, selectedCategory]);

  const handleCategoryChange = (category) => {
    setSelectedCategory(category);
    setCurrentPage(1); // Reset to first page when category changes
  };

  const handleRetry = () => {
    setCurrentPage(1);
    window.location.reload();
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            Top Headlines
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Latest news from around the world
          </p>
        </div>

        {/* Category Filters */}
        <div className="mb-6 flex flex-wrap gap-2">
          <button
            onClick={() => handleCategoryChange('')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              selectedCategory === ''
                ? 'bg-primary-600 text-white'
                : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
            }`}
          >
            All
          </button>
          {categories.map((category) => (
            <button
              key={category}
              onClick={() => handleCategoryChange(category)}
              className={`px-4 py-2 rounded-lg font-medium capitalize transition-colors ${
                selectedCategory === category
                  ? 'bg-primary-600 text-white'
                  : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              {category}
            </button>
          ))}
        </div>

        {/* Content */}
        {loading ? (
          <NewsListSkeleton count={DEFAULT_PAGE_SIZE} />
        ) : error ? (
          <ErrorMessage message={error} onRetry={handleRetry} />
        ) : (
          <>
            <NewsList articles={articles} />
            <Pagination
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={setCurrentPage}
            />
          </>
        )}
      </div>
    </div>
  );
};

export default HomePage;
