import React from 'react';
import { Link } from 'react-router-dom';

const Dashboard = ({ currentAnalysis, setCurrentAnalysis }) => {
  const stats = [
    {
      title: 'Total Videos Analyzed',
      value: '12',
      change: '+3 this week',
      color: 'bg-blue-500'
    },
    {
      title: 'Average Confidence Score',
      value: '78%',
      change: '+5% improvement',
      color: 'bg-green-500'
    },
    {
      title: 'Speech Clarity',
      value: '85%',
      change: '+2% this month',
      color: 'bg-purple-500'
    },
    {
      title: 'Engagement Level',
      value: '82%',
      change: '+7% improvement',
      color: 'bg-orange-500'
    }
  ];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-800 mb-4">
          AI Video Sales Coach Dashboard
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Analyze your sales presentations with advanced AI to improve your performance, 
          boost confidence, and close more deals.
        </p>
      </div>

      {/* Quick Actions */}
      <div className="flex justify-center space-x-4">
        <Link
          to="/upload"
          className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-8 py-3 rounded-lg font-semibold hover:from-blue-600 hover:to-purple-700 transition-all duration-200 transform hover:scale-105 shadow-lg"
        >
          Upload New Video
        </Link>
        {currentAnalysis && (
          <Link
            to="/results"
            className="bg-white text-blue-600 border-2 border-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-all duration-200 transform hover:scale-105 shadow-lg"
          >
            View Latest Results
          </Link>
        )}
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <div key={index} className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow duration-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 mb-1">{stat.title}</p>
                <p className="text-3xl font-bold text-gray-800">{stat.value}</p>
                <p className="text-sm text-green-600 mt-1">{stat.change}</p>
              </div>
              <div className={`w-12 h-12 ${stat.color} rounded-lg flex items-center justify-center`}>
                <div className="w-6 h-6 bg-white rounded opacity-80"></div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Recent Analysis */}
      {currentAnalysis && (
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Latest Analysis</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600">
                {currentAnalysis.analysis?.overall_score || 'N/A'}%
              </div>
              <div className="text-gray-600">Overall Score</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-green-600">
                {currentAnalysis.analysis?.confidence_level || 'N/A'}%
              </div>
              <div className="text-gray-600">Confidence</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-600">
                {currentAnalysis.analysis?.speech_clarity || 'N/A'}%
              </div>
              <div className="text-gray-600">Speech Clarity</div>
            </div>
          </div>
          <div className="mt-4 text-center">
            <Link
              to="/results"
              className="text-blue-600 hover:text-blue-800 font-medium"
            >
              View Detailed Analysis →
            </Link>
          </div>
        </div>
      )}

      {/* Features */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="text-center">
          <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <div className="w-8 h-8 bg-blue-500 rounded"></div>
          </div>
          <h3 className="text-xl font-semibold text-gray-800 mb-2">Emotion Analysis</h3>
          <p className="text-gray-600">
            Advanced facial emotion recognition to understand your emotional delivery and audience engagement.
          </p>
        </div>
        <div className="text-center">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <div className="w-8 h-8 bg-green-500 rounded"></div>
          </div>
          <h3 className="text-xl font-semibold text-gray-800 mb-2">Speech Analysis</h3>
          <p className="text-gray-600">
            Analyze speech patterns, pace, clarity, and filler words to improve your verbal communication.
          </p>
        </div>
        <div className="text-center">
          <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <div className="w-8 h-8 bg-purple-500 rounded"></div>
          </div>
          <h3 className="text-xl font-semibold text-gray-800 mb-2">AI Coaching</h3>
          <p className="text-gray-600">
            Get personalized coaching recommendations powered by advanced AI to enhance your sales performance.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 