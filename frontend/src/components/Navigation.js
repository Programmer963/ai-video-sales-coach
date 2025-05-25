import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navigation = () => {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <nav className="bg-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">AI</span>
            </div>
            <h1 className="text-xl font-bold text-gray-800">
              Video Sales Coach
            </h1>
          </div>
          
          <div className="flex space-x-6">
            <Link
              to="/"
              className={`px-4 py-2 rounded-lg transition-colors duration-200 ${
                isActive('/') 
                  ? 'bg-blue-500 text-white' 
                  : 'text-gray-600 hover:text-blue-500 hover:bg-blue-50'
              }`}
            >
              Dashboard
            </Link>
            <Link
              to="/upload"
              className={`px-4 py-2 rounded-lg transition-colors duration-200 ${
                isActive('/upload') 
                  ? 'bg-blue-500 text-white' 
                  : 'text-gray-600 hover:text-blue-500 hover:bg-blue-50'
              }`}
            >
              Upload Video
            </Link>
            <Link
              to="/results"
              className={`px-4 py-2 rounded-lg transition-colors duration-200 ${
                isActive('/results') 
                  ? 'bg-blue-500 text-white' 
                  : 'text-gray-600 hover:text-blue-500 hover:bg-blue-50'
              }`}
            >
              Results
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation; 