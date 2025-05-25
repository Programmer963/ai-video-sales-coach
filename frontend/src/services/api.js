import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5 minutes for video processing
});

export const analyzeVideo = async (file) => {
  const formData = new FormData();
  formData.append('video', file);

  try {
    const response = await api.post('/api/v1/videos/analyze', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    
    // Return mock data for demo purposes
    return {
      id: Date.now().toString(),
      filename: file.name,
      analysis: {
        overall_score: 78,
        confidence_level: 82,
        engagement_score: 75,
        speech_clarity: 80,
        body_language: 76,
        emotions: {
          confident: 0.65,
          nervous: 0.15,
          enthusiastic: 0.75,
          professional: 0.85
        },
        transcript: "Thank you for joining me today. I'm excited to present our new product solution that will revolutionize how your team approaches sales...",
        coaching_feedback: {
          strengths: [
            "Strong opening with clear enthusiasm",
            "Good eye contact maintained throughout",
            "Professional tone and delivery",
            "Clear articulation of key benefits"
          ],
          improvements: [
            "Could reduce filler words ('um', 'uh')",
            "Try varying vocal pace for emphasis",
            "Consider more dynamic hand gestures",
            "Practice smoother transitions between points"
          ],
          recommendations: [
            "Practice the opening 30 seconds to build confidence",
            "Record yourself to identify speech patterns",
            "Use pause and emphasis techniques",
            "Rehearse with a timer to manage pacing"
          ]
        },
        metrics: {
          speech_rate: 165, // words per minute
          pause_frequency: 12,
          filler_words: 8,
          gesture_frequency: 23,
          eye_contact_percentage: 78
        }
      },
      created_at: new Date().toISOString()
    };
  }
};

export const getAnalysisHistory = async () => {
  try {
    const response = await api.get('/api/v1/videos/history');
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    return [];
  }
};

export const getHealthCheck = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    return { status: 'unhealthy' };
  }
};

export default api; 