import React, { useState } from 'react';
import { FaSearch, FaSpinner } from 'react-icons/fa';

const AISearchBar = ({ onSubmit }) => {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    
    setIsLoading(true);
    try {
      await onSubmit(query);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form 
      onSubmit={handleSubmit}
      className="fixed bottom-8 left-1/2 transform -translate-x-1/2 w-4/5 max-w-2xl flex items-center bg-gray-800 rounded-full px-4 py-2 shadow-lg border border-gray-700"
    >
      <input
        type="text"
        placeholder="AI에게 질문하기..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="flex-1 bg-transparent border-none outline-none text-white placeholder-gray-400 px-4 py-2"
        disabled={isLoading}
      />
      <button
        type="submit"
        className="ml-2 p-2 bg-blue-600 hover:bg-blue-700 rounded-full text-white disabled:bg-blue-400"
        disabled={isLoading}
      >
        {isLoading ? (
          <FaSpinner className="w-5 h-5 animate-spin" />
        ) : (
          <FaSearch className="w-5 h-5" />
        )}
      </button>
    </form>
  );
};

export default AISearchBar;
