import React from 'react';
import { Link } from 'react-router-dom';
import { Upload, TrendingUp, Users, Award } from 'lucide-react';

const Dashboard = ({ currentAnalysis }) => {
  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Welcome Section */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Welcome to AI Video Sales Coach
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Improve your sales presentations with AI-powered analysis. 
          Upload your video to get instant feedback on delivery, confidence, and engagement.
        </p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-lg text-center">
          <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
            <TrendingUp className="h-6 w-6 text-blue-600" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900">Performance</h3>
          <p className="text-gray-500">Track your progress</p>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-lg text-center">
          <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
            <Users className="h-6 w-6 text-green-600" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900">Engagement</h3>
          <p className="text-gray-500">Audience connection</p>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-lg text-center">
          <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-4">
            <Award className="h-6 w-6 text-purple-600" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900">Confidence</h3>
          <p className="text-gray-500">Build presentation skills</p>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-lg text-center">
          <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center mx-auto mb-4">
            <Upload className="h-6 w-6 text-orange-600" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900">Analysis</h3>
          <p className="text-gray-500">AI-powered insights</p>
        </div>
      </div>

      {/* Latest Analysis */}
      {currentAnalysis && (
        <div className="bg-white rounded-xl shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Latest Analysis</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600">
                {currentAnalysis.analysis?.overall_score || 0}%
              </div>
              <p className="text-gray-500">Overall Score</p>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-green-600">
                {currentAnalysis.analysis?.confidence_level || 0}%
              </div>
              <p className="text-gray-500">Confidence</p>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-600">
                {currentAnalysis.analysis?.engagement_score || 0}%
              </div>
              <p className="text-gray-500">Engagement</p>
            </div>
          </div>
          <div className="mt-6 text-center">
            <Link 
              to="/results"
              className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg font-medium transition-colors"
            >
              View Detailed Results
            </Link>
          </div>
        </div>
      )}

      {/* Call to Action */}
      <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl p-8 text-center text-white">
        <h2 className="text-3xl font-bold mb-4">Ready to Improve Your Sales?</h2>
        <p className="text-xl mb-6 opacity-90">
          Upload your first sales video and get instant AI-powered coaching
        </p>
        <Link 
          to="/upload"
          className="bg-white text-blue-600 hover:bg-gray-100 px-8 py-3 rounded-lg font-bold text-lg transition-colors inline-flex items-center space-x-2"
        >
          <Upload className="h-5 w-5" />
          <span>Upload Video Now</span>
        </Link>
      </div>

      {/* Features */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="bg-white p-6 rounded-xl shadow-lg">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">
            🎯 Multimodal Analysis
          </h3>
          <p className="text-gray-600">
            Our AI analyzes video, audio, and text to provide comprehensive feedback 
            on your presentation skills and delivery.
          </p>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-lg">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">
            🤖 Agent-Based Coaching
          </h3>
          <p className="text-gray-600">
            Powered by advanced AI agents that understand sales psychology 
            and provide personalized coaching recommendations.
          </p>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-lg">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">
            📈 Performance Tracking
          </h3>
          <p className="text-gray-600">
            Track your improvement over time with detailed metrics and 
            actionable insights for better sales presentations.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 