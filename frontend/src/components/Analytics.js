import React, { useState, useEffect } from 'react';
import { BarChart3, Users, MessageCircle, TrendingUp } from 'lucide-react';
import axios from 'axios';

const Analytics = () => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState(30);

  useEffect(() => {
    fetchAnalytics();
  }, [timeRange]);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`/api/v1/analytics/overview?days=${timeRange}`);
      setAnalytics(response.data);
    } catch (error) {
      console.error('Error fetching analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-6xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="text-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-2 text-gray-600">Loading analytics...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <BarChart3 className="text-blue-600" size={24} />
            <h1 className="text-2xl font-bold text-gray-800">Analytics Dashboard</h1>
          </div>
          
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(Number(e.target.value))}
            className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value={7}>Last 7 days</option>
            <option value={30}>Last 30 days</option>
            <option value={90}>Last 90 days</option>
          </select>
        </div>

        {analytics ? (
          <>
            {/* Key Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="bg-blue-50 rounded-lg p-6">
                <div className="flex items-center">
                  <MessageCircle className="text-blue-600" size={24} />
                  <div className="ml-4">
                    <p className="text-sm font-medium text-blue-600">Total Interactions</p>
                    <p className="text-2xl font-bold text-blue-900">{analytics.total_interactions}</p>
                  </div>
                </div>
              </div>
              
              <div className="bg-green-50 rounded-lg p-6">
                <div className="flex items-center">
                  <Users className="text-green-600" size={24} />
                  <div className="ml-4">
                    <p className="text-sm font-medium text-green-600">Unique Users</p>
                    <p className="text-2xl font-bold text-green-900">{analytics.unique_users}</p>
                  </div>
                </div>
              </div>
              
              <div className="bg-purple-50 rounded-lg p-6">
                <div className="flex items-center">
                  <TrendingUp className="text-purple-600" size={24} />
                  <div className="ml-4">
                    <p className="text-sm font-medium text-purple-600">Avg Message Length</p>
                    <p className="text-2xl font-bold text-purple-900">{analytics.avg_message_length}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Top Topics */}
            <div className="mb-8">
              <h2 className="text-lg font-semibold text-gray-800 mb-4">Popular Topics</h2>
              <div className="grid gap-4">
                {analytics.top_topics.map((topic, index) => (
                  <div key={topic.topic} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div className="flex items-center">
                      <span className="text-sm font-medium text-gray-500 w-8">{index + 1}</span>
                      <span className="text-gray-800 capitalize">
                        {topic.topic.replace('_', ' ')}
                      </span>
                    </div>
                    <span className="text-sm font-semibold text-blue-600">
                      {topic.count} interactions
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Time Period Info */}
            <div className="bg-gray-50 rounded-lg p-4">
              <h3 className="text-sm font-medium text-gray-700 mb-2">Analysis Period</h3>
              <p className="text-sm text-gray-600">
                {new Date(analytics.period_start).toLocaleDateString()} - {new Date(analytics.period_end).toLocaleDateString()}
                <span className="ml-2 text-gray-500">({analytics.period_days} days)</span>
              </p>
            </div>
          </>
        ) : (
          <div className="text-center py-8">
            <BarChart3 size={48} className="mx-auto mb-4 text-gray-300" />
            <p className="text-gray-600">No analytics data available.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Analytics; 