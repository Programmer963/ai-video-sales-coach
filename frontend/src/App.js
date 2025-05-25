import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import VideoUpload from './components/VideoUpload';
import AnalysisResults from './components/AnalysisResults';
import Dashboard from './components/Dashboard';
import Navigation from './components/Navigation';
import './App.css';

function App() {
  const [currentAnalysis, setCurrentAnalysis] = useState(null);

  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <Navigation />
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route 
              path="/" 
              element={
                <Dashboard 
                  currentAnalysis={currentAnalysis}
                  setCurrentAnalysis={setCurrentAnalysis}
                />
              } 
            />
            <Route 
              path="/upload" 
              element={
                <VideoUpload 
                  onAnalysisComplete={setCurrentAnalysis}
                />
              } 
            />
            <Route 
              path="/results" 
              element={
                <AnalysisResults 
                  analysis={currentAnalysis}
                />
              } 
            />
          </Routes>
        </main>
        <Toaster position="top-right" />
      </div>
    </Router>
  );
}

export default App; 