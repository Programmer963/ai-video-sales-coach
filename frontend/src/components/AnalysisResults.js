import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, CheckCircle, AlertCircle, Lightbulb } from 'lucide-react';

const AnalysisResults = ({ analysis }) => {
  if (!analysis) {
    return (
      <div className="max-w-4xl mx-auto text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">No Analysis Available</h1>
        <p className="text-gray-600 mb-8">Upload a video to see your analysis results.</p>
        <Link 
          to="/upload"
          className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg font-medium transition-colors"
        >
          Upload Video
        </Link>
      </div>
    );
  }

  const { analysis: data } = analysis;

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <Link to="/" className="flex items-center text-blue-600 hover:text-blue-700 mb-4">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Dashboard
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">Analysis Results</h1>
          <p className="text-gray-600">Video: {analysis.filename}</p>
        </div>
      </div>

      {/* Overall Score */}
      <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl p-8 text-white text-center">
        <h2 className="text-2xl font-bold mb-4">Overall Performance Score</h2>
        <div className="text-6xl font-bold mb-2">{data.overall_score}%</div>
        <p className="text-xl opacity-90">
          {data.overall_score >= 80 ? 'Excellent!' : 
           data.overall_score >= 70 ? 'Good!' : 
           data.overall_score >= 60 ? 'Fair' : 'Needs Improvement'}
        </p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-lg text-center">
          <div className="text-3xl font-bold text-blue-600 mb-2">
            {data.confidence_level}%
          </div>
          <p className="text-gray-600">Confidence Level</p>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-lg text-center">
          <div className="text-3xl font-bold text-green-600 mb-2">
            {data.engagement_score}%
          </div>
          <p className="text-gray-600">Engagement</p>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-lg text-center">
          <div className="text-3xl font-bold text-purple-600 mb-2">
            {data.speech_clarity}%
          </div>
          <p className="text-gray-600">Speech Clarity</p>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-lg text-center">
          <div className="text-3xl font-bold text-orange-600 mb-2">
            {data.body_language}%
          </div>
          <p className="text-gray-600">Body Language</p>
        </div>
      </div>

      {/* Emotional Analysis */}
      <div className="bg-white rounded-xl shadow-lg p-8">
        <h3 className="text-2xl font-bold text-gray-900 mb-6">Emotional Analysis</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {Object.entries(data.emotions).map(([emotion, score]) => (
            <div key={emotion} className="text-center">
              <div className="relative w-20 h-20 mx-auto mb-2">
                <svg className="w-20 h-20 transform -rotate-90" viewBox="0 0 36 36">
                  <path
                    d="M18 2.0845
                      a 15.9155 15.9155 0 0 1 0 31.831
                      a 15.9155 15.9155 0 0 1 0 -31.831"
                    fill="none"
                    stroke="#e5e7eb"
                    strokeWidth="2"
                  />
                  <path
                    d="M18 2.0845
                      a 15.9155 15.9155 0 0 1 0 31.831
                      a 15.9155 15.9155 0 0 1 0 -31.831"
                    fill="none"
                    stroke="#3b82f6"
                    strokeWidth="2"
                    strokeDasharray={`${score * 100}, 100`}
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-sm font-bold text-gray-900">
                    {Math.round(score * 100)}%
                  </span>
                </div>
              </div>
              <p className="text-sm text-gray-600 capitalize">{emotion}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Coaching Feedback */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Strengths */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center mb-4">
            <CheckCircle className="h-6 w-6 text-green-600 mr-2" />
            <h3 className="text-xl font-bold text-gray-900">Strengths</h3>
          </div>
          <ul className="space-y-3">
            {data.coaching_feedback.strengths.map((strength, index) => (
              <li key={index} className="flex items-start">
                <div className="w-2 h-2 bg-green-500 rounded-full mt-2 mr-3 flex-shrink-0" />
                <span className="text-gray-700">{strength}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Areas for Improvement */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center mb-4">
            <AlertCircle className="h-6 w-6 text-orange-600 mr-2" />
            <h3 className="text-xl font-bold text-gray-900">Improvements</h3>
          </div>
          <ul className="space-y-3">
            {data.coaching_feedback.improvements.map((improvement, index) => (
              <li key={index} className="flex items-start">
                <div className="w-2 h-2 bg-orange-500 rounded-full mt-2 mr-3 flex-shrink-0" />
                <span className="text-gray-700">{improvement}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Recommendations */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center mb-4">
            <Lightbulb className="h-6 w-6 text-blue-600 mr-2" />
            <h3 className="text-xl font-bold text-gray-900">Recommendations</h3>
          </div>
          <ul className="space-y-3">
            {data.coaching_feedback.recommendations.map((recommendation, index) => (
              <li key={index} className="flex items-start">
                <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0" />
                <span className="text-gray-700">{recommendation}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Transcript */}
      <div className="bg-white rounded-xl shadow-lg p-8">
        <h3 className="text-2xl font-bold text-gray-900 mb-4">Transcript</h3>
        <div className="bg-gray-50 rounded-lg p-6">
          <p className="text-gray-700 leading-relaxed">{data.transcript}</p>
        </div>
      </div>

      {/* Performance Metrics */}
      <div className="bg-white rounded-xl shadow-lg p-8">
        <h3 className="text-2xl font-bold text-gray-900 mb-6">Detailed Metrics</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">{data.metrics.speech_rate}</div>
            <p className="text-gray-600">Words per minute</p>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">{data.metrics.eye_contact_percentage}%</div>
            <p className="text-gray-600">Eye contact</p>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-600">{data.metrics.filler_words}</div>
            <p className="text-gray-600">Filler words</p>
          </div>
        </div>
      </div>

      {/* Actions */}
      <div className="text-center">
        <Link 
          to="/upload"
          className="bg-blue-500 hover:bg-blue-600 text-white px-8 py-3 rounded-lg font-bold text-lg transition-colors mr-4"
        >
          Analyze Another Video
        </Link>
        <Link 
          to="/"
          className="bg-gray-200 hover:bg-gray-300 text-gray-800 px-8 py-3 rounded-lg font-bold text-lg transition-colors"
        >
          Back to Dashboard
        </Link>
      </div>
    </div>
  );
};

export default AnalysisResults; 