/**
 * Application Constants
 */

export const APP_NAME = 'News Aggregator';

export const ROUTES = {
  HOME: '/',
  SEARCH: '/search',
};

export const DEFAULT_PAGE_SIZE = 10;

export const DATE_FORMAT_OPTIONS = {
  year: 'numeric',
  month: 'short',
  day: 'numeric',
  hour: '2-digit',
  minute: '2-digit',
};

export const ERROR_MESSAGES = {
  GENERIC: 'Oops! Something went wrong. Please try again.',
  NO_RESULTS: 'No articles found. Try different keywords or filters.',
  NETWORK: 'No internet connection. Please check your network.',
  API_ERROR: 'Failed to load news. Please try again later.',
};
