/**
 * NewsCardSkeleton Component
 * Loading skeleton for news cards
 */
const NewsCardSkeleton = () => {
  return (
    <div className="card overflow-hidden h-full animate-pulse">
      {/* Image Skeleton */}
      <div className="w-full h-48 bg-gray-300 dark:bg-gray-700"></div>

      {/* Content Skeleton */}
      <div className="p-4">
        {/* Source and Date */}
        <div className="flex items-center justify-between mb-2">
          <div className="h-3 bg-gray-300 dark:bg-gray-700 rounded w-20"></div>
          <div className="h-3 bg-gray-300 dark:bg-gray-700 rounded w-16"></div>
        </div>

        {/* Title */}
        <div className="space-y-2 mb-4">
          <div className="h-4 bg-gray-300 dark:bg-gray-700 rounded"></div>
          <div className="h-4 bg-gray-300 dark:bg-gray-700 rounded w-3/4"></div>
        </div>

        {/* Description */}
        <div className="space-y-2 mb-4">
          <div className="h-3 bg-gray-300 dark:bg-gray-700 rounded"></div>
          <div className="h-3 bg-gray-300 dark:bg-gray-700 rounded"></div>
          <div className="h-3 bg-gray-300 dark:bg-gray-700 rounded w-5/6"></div>
        </div>

        {/* Button */}
        <div className="h-4 bg-gray-300 dark:bg-gray-700 rounded w-28"></div>
      </div>
    </div>
  );
};

const NewsListSkeleton = ({ count = 9 }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {Array.from({ length: count }).map((_, index) => (
        <NewsCardSkeleton key={index} />
      ))}
    </div>
  );
};

export { NewsCardSkeleton, NewsListSkeleton };
