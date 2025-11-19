/**
 * Footer Component
 * Application footer with information
 */
import { APP_NAME } from '../../utils/constants';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 mt-auto">
      <div className="container mx-auto px-4 py-6">
        <div className="flex flex-col md:flex-row items-center justify-between">
          <p className="text-gray-600 dark:text-gray-400 text-sm">
            © {currentYear} {APP_NAME}. Powered by NewsAPI.org
          </p>
          <p className="text-gray-500 dark:text-gray-500 text-xs mt-2 md:mt-0">
            Built with React, FastAPI & TailwindCSS
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
