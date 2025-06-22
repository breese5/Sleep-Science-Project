import React, { useState, useEffect } from 'react';
import { BookOpen, Filter, Search } from 'lucide-react';
import axios from 'axios';

const Recommendations = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        setLoading(true);
        const response = await axios.get('/api/v1/recommendations');
        setRecommendations(response.data);
        const uniqueCategories = [...new Set(response.data.map(rec => rec.category))];
        setCategories(uniqueCategories);
      } catch (error) {
        console.error('Error fetching recommendations:', error);
        setError('Failed to load recommendations. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendations();
  }, []);

  const handleCategoryChange = (category) => {
    setSelectedCategory(category);
  };

  const handleSearch = () => {
    // This function is now empty as the filtering is done on the client-side
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'low':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getSourceColor = (source) => {
    switch (source) {
      case 'bryan_johnson':
        return 'bg-purple-100 text-purple-800';
      case 'andrew_huberman':
        return 'bg-blue-100 text-blue-800';
      case 'eightsleep':
        return 'bg-green-100 text-green-800';
      case 'cdc':
        return 'bg-orange-100 text-orange-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const filteredRecommendations = recommendations
    .filter((rec) =>
      rec.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      rec.content.toLowerCase().includes(searchQuery.toLowerCase())
    )
    .filter((rec) =>
      selectedCategory === '' || selectedCategory === 'all' ? true : rec.category === selectedCategory
    );

  return (
    <div className="container mx-auto p-6 bg-gray-50 min-h-screen">
      <div className="mb-8 text-center">
        <h1 className="text-4xl font-bold text-gray-800 mb-2">Expert Sleep Recommendations</h1>
        <p className="text-lg text-gray-600">
          Curated advice from leading sleep science experts and institutions.
        </p>
        <p className="text-sm text-red-600 mt-4 px-4 py-2 bg-red-100 rounded-md inline-block">
          This is not meant to be medical advice and is made for educational purposes only. Consult with a doctor for further questions.
        </p>
      </div>

      <div className="max-w-6xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex items-center space-x-3 mb-6">
            <BookOpen className="text-blue-600" size={24} />
            <h1 className="text-2xl font-bold text-gray-800">Sleep Recommendations</h1>
          </div>

          {/* Filters */}
          <div className="mb-6 space-y-4">
            <div className="flex flex-wrap gap-4 items-center">
              <div className="flex items-center space-x-2">
                <Filter size={20} className="text-gray-500" />
                <span className="text-sm font-medium text-gray-700">Filter by:</span>
              </div>
              
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Categories</option>
                {categories.map((category) => (
                  <option key={category} value={category}>
                    {category.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                  </option>
                ))}
              </select>
            </div>

            <div className="flex space-x-4">
              <div className="flex-1 relative">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search recommendations..."
                  className="w-full border border-gray-300 rounded-lg pl-10 pr-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                />
                <Search size={20} className="absolute left-3 top-2.5 text-gray-400" />
              </div>
              <button
                onClick={handleSearch}
                disabled={true}
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors disabled:opacity-50"
              >
                Search
              </button>
            </div>
          </div>

          {/* Recommendations */}
          {loading ? (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
              <p className="mt-2 text-gray-600">Loading recommendations...</p>
            </div>
          ) : filteredRecommendations.length === 0 ? (
            <div className="text-center py-8">
              <BookOpen size={48} className="mx-auto mb-4 text-gray-300" />
              <p className="text-gray-600">No recommendations match your criteria.</p>
            </div>
          ) : (
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {filteredRecommendations.map((rec) => (
                <div key={rec.id} className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between mb-3">
                    <h3 className="text-lg font-semibold text-gray-800 line-clamp-2">
                      {rec.title}
                    </h3>
                  </div>
                  
                  <p className="text-gray-600 text-sm mb-4 line-clamp-4">
                    {rec.content}
                  </p>
                  
                  <div className="flex flex-wrap gap-2 mb-4">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(rec.priority)}`}>
                      {rec.priority} priority
                    </span>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSourceColor(rec.source)}`}>
                      {rec.source_name}
                    </span>
                  </div>
                  
                  <div className="text-xs text-gray-500">
                    Category: {rec.category.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Recommendations; 