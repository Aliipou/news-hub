/**
 * NewsCard Component
 * Displays a single news article in card format
 */
import { formatDate, truncateText, getPlaceholderImage } from '../../utils/helpers';

const NewsCard = ({ article }) => {
  const {
    title,
    description,
    url,
    urlToImage,
    source,
    publishedAt,
    author,
  } = article;

  const handleImageError = (e) => {
    e.target.src = getPlaceholderImage();
  };

  return (
    <article className="card overflow-hidden h-full flex flex-col animate-fade-in">
      {/* Image */}
      <div className="w-full h-48 bg-gray-200 dark:bg-gray-700 overflow-hidden">
        <img
          src={urlToImage || getPlaceholderImage()}
          alt={title}
          className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
          onError={handleImageError}
          loading="lazy"
        />
      </div>

      {/* Content */}
      <div className="p-4 flex-1 flex flex-col">
        {/* Source and Date */}
        <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400 mb-2">
          <span className="font-medium text-primary-600 dark:text-primary-400">
            {source.name}
          </span>
          <time dateTime={publishedAt}>
            {formatDate(publishedAt)}
          </time>
        </div>

        {/* Title */}
        <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2 line-clamp-2">
          {title}
        </h3>

        {/* Description */}
        {description && (
          <p className="text-gray-600 dark:text-gray-300 text-sm mb-4 flex-1 line-clamp-3">
            {truncateText(description, 120)}
          </p>
        )}

        {/* Author (if available) */}
        {author && (
          <p className="text-xs text-gray-500 dark:text-gray-400 mb-3">
            By {author}
          </p>
        )}

        {/* Read More Link */}
        <a
          href={url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 font-medium text-sm transition-colors mt-auto"
        >
          Read full article
          <svg
            className="w-4 h-4 ml-1"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5l7 7-7 7"
            />
          </svg>
        </a>
      </div>
    </article>
  );
};

export default NewsCard;
