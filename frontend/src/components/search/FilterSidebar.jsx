/**
 * FilterSidebar Component
 * Sidebar with filter options for news search
 */
import { useState, useEffect } from 'react';
import { getFilters } from '../../services/api';

const FilterSidebar = ({ onFilterChange, initialFilters = {} }) => {
  const [filters, setFilters] = useState({
    language: initialFilters.language || '',
    sortBy: initialFilters.sortBy || 'publishedAt',
    fromDate: initialFilters.fromDate || '',
    toDate: initialFilters.toDate || '',
  });

  const [filterOptions, setFilterOptions] = useState({
    languages: [],
    sortOptions: [],
  });

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadFilters = async () => {
      try {
        const data = await getFilters();
        setFilterOptions({
          languages: data.languages || [],
          sortOptions: data.sort_options || [],
        });
      } catch (error) {
        console.error('Failed to load filters:', error);
      } finally {
        setLoading(false);
      }
    };
    loadFilters();
  }, []);

  const handleChange = (key, value) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
  };

  const handleApply = () => {
    onFilterChange(filters);
  };

  const handleReset = () => {
    const resetFilters = {
      language: '',
      sortBy: 'publishedAt',
      fromDate: '',
      toDate: '',
    };
    setFilters(resetFilters);
    onFilterChange(resetFilters);
  };

  if (loading) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4">
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-gray-300 dark:bg-gray-700 rounded w-1/2"></div>
          <div className="h-10 bg-gray-300 dark:bg-gray-700 rounded"></div>
          <div className="h-4 bg-gray-300 dark:bg-gray-700 rounded w-1/2"></div>
          <div className="h-10 bg-gray-300 dark:bg-gray-700 rounded"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-4 sticky top-20">
      <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">
        Filters
      </h3>

      {/* Language Filter */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Language
        </label>
        <select
          value={filters.language}
          onChange={(e) => handleChange('language', e.target.value)}
          className="input"
        >
          <option value="">All Languages</option>
          {filterOptions.languages.map((lang) => (
            <option key={lang.code} value={lang.code}>
              {lang.name}
            </option>
          ))}
        </select>
      </div>

      {/* Sort By Filter */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Sort By
        </label>
        <select
          value={filters.sortBy}
          onChange={(e) => handleChange('sortBy', e.target.value)}
          className="input"
        >
          {filterOptions.sortOptions.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>

      {/* From Date */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          From Date
        </label>
        <input
          type="date"
          value={filters.fromDate}
          onChange={(e) => handleChange('fromDate', e.target.value)}
          className="input"
          max={filters.toDate || new Date().toISOString().split('T')[0]}
        />
      </div>

      {/* To Date */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          To Date
        </label>
        <input
          type="date"
          value={filters.toDate}
          onChange={(e) => handleChange('toDate', e.target.value)}
          className="input"
          min={filters.fromDate}
          max={new Date().toISOString().split('T')[0]}
        />
      </div>

      {/* Action Buttons */}
      <div className="space-y-2">
        <button
          onClick={handleApply}
          className="w-full btn-primary"
        >
          Apply Filters
        </button>
        <button
          onClick={handleReset}
          className="w-full btn-secondary"
        >
          Reset
        </button>
      </div>
    </div>
  );
};

export default FilterSidebar;
