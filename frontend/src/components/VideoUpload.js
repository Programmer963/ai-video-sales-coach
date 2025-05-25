import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Upload, Video, Loader2 } from 'lucide-react';
import { analyzeVideo } from '../services/api';

const VideoUpload = ({ onAnalysisComplete }) => {
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const navigate = useNavigate();

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0];
    if (!file) return;

    if (!file.type.startsWith('video/')) {
      toast.error('Please upload a video file');
      return;
    }

    setUploading(true);
    setUploadProgress(0);

    try {
      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 200);

      const result = await analyzeVideo(file);
      
      clearInterval(progressInterval);
      setUploadProgress(100);
      
      toast.success('Video analyzed successfully!');
      onAnalysisComplete(result);
      navigate('/results');
      
    } catch (error) {
      console.error('Upload failed:', error);
      toast.error('Analysis failed. Please try again.');
    } finally {
      setUploading(false);
      setUploadProgress(0);
    }
  }, [onAnalysisComplete, navigate]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'video/*': ['.mp4', '.avi', '.mov', '.mkv', '.webm']
    },
    maxFiles: 1,
    disabled: uploading
  });

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          AI Video Sales Coach
        </h1>
        <p className="text-xl text-gray-600">
          Upload your sales presentation for AI-powered analysis and coaching
        </p>
      </div>

      <div className="bg-white rounded-xl shadow-lg p-8">
        <div
          {...getRootProps()}
          className={`
            border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-all
            ${isDragActive 
              ? 'border-blue-500 bg-blue-50' 
              : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
            }
            ${uploading ? 'pointer-events-none opacity-50' : ''}
          `}
        >
          <input {...getInputProps()} />
          
          {uploading ? (
            <div className="space-y-4">
              <Loader2 className="h-16 w-16 text-blue-500 mx-auto animate-spin" />
              <div className="space-y-2">
                <p className="text-lg font-medium text-gray-900">
                  Analyzing your video...
                </p>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${uploadProgress}%` }}
                  />
                </div>
                <p className="text-sm text-gray-500">
                  {uploadProgress}% complete
                </p>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              {isDragActive ? (
                <>
                  <Upload className="h-16 w-16 text-blue-500 mx-auto" />
                  <p className="text-xl font-medium text-blue-600">
                    Drop your video here!
                  </p>
                </>
              ) : (
                <>
                  <Video className="h-16 w-16 text-gray-400 mx-auto" />
                  <div className="space-y-2">
                    <p className="text-xl font-medium text-gray-900">
                      Drag & drop your sales video here
                    </p>
                    <p className="text-gray-500">
                      or click to browse files
                    </p>
                  </div>
                  <div className="flex justify-center">
                    <button className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg font-medium transition-colors">
                      Choose Video File
                    </button>
                  </div>
                </>
              )}
              
              <div className="text-sm text-gray-400 space-y-1">
                <p>Supported formats: MP4, AVI, MOV, MKV, WebM</p>
                <p>Maximum file size: 100MB</p>
              </div>
            </div>
          )}
        </div>

        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
          <div className="space-y-2">
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto">
              <Video className="h-6 w-6 text-blue-600" />
            </div>
            <h3 className="font-medium text-gray-900">Video Analysis</h3>
            <p className="text-sm text-gray-500">
              AI analyzes your presentation style and delivery
            </p>
          </div>
          
          <div className="space-y-2">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto">
              <span className="text-green-600 font-bold text-lg">🎯</span>
            </div>
            <h3 className="font-medium text-gray-900">Coaching Insights</h3>
            <p className="text-sm text-gray-500">
              Get personalized feedback and improvement suggestions
            </p>
          </div>
          
          <div className="space-y-2">
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto">
              <span className="text-purple-600 font-bold text-lg">📈</span>
            </div>
            <h3 className="font-medium text-gray-900">Performance Metrics</h3>
            <p className="text-sm text-gray-500">
              Track confidence, engagement, and communication effectiveness
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VideoUpload; 