import numpy as np
import cv2
from typing import Dict, List, Any
import logging
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)

class EmotionDetector:
    """Service for detecting emotions from video frames using facial analysis"""
    
    def __init__(self):
        self.emotion_labels = [
            'angry', 'disgust', 'fear', 'happy', 
            'sad', 'surprise', 'neutral'
        ]
        # In production, would load a trained emotion detection model
        # For now, using mock analysis
    
    async def analyze_emotions(self, frames: List[np.ndarray]) -> Dict[str, Any]:
        """
        Analyze emotions from video frames
        
        Args:
            frames: List of video frames as numpy arrays
            
        Returns:
            Dictionary containing emotion analysis results
        """
        try:
            logger.info(f"Analyzing emotions from {len(frames)} frames")
            
            # Run analysis in thread pool for CPU-intensive operations
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                self._analyze_emotions_sync, 
                frames
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing emotions: {str(e)}")
            return self._get_default_emotion_data()
    
    def _analyze_emotions_sync(self, frames: List[np.ndarray]) -> Dict[str, Any]:
        """Synchronous emotion analysis"""
        if not frames:
            return self._get_default_emotion_data()
        
        # Initialize face detector
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        frame_emotions = []
        total_faces_detected = 0
        
        for i, frame in enumerate(frames):
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            
            # Detect faces
            faces = face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
            )
            
            total_faces_detected += len(faces)
            
            # For each face, generate mock emotion analysis
            face_emotions = []
            for (x, y, w, h) in faces:
                # Extract face region
                face_region = gray[y:y+h, x:x+w]
                
                # Mock emotion prediction (in production, use trained model)
                emotion_scores = self._predict_emotions_mock()
                
                face_emotions.append({
                    "face_bbox": [int(x), int(y), int(w), int(h)],
                    "emotion_scores": emotion_scores,
                    "dominant_emotion": max(emotion_scores, key=emotion_scores.get),
                    "confidence": max(emotion_scores.values())
                })
            
            frame_emotions.append({
                "frame_index": i,
                "timestamp": i * 0.5,  # Assuming 2 FPS sampling
                "faces": face_emotions,
                "face_count": len(faces)
            })
        
        # Calculate overall statistics
        all_emotions = []
        for frame_data in frame_emotions:
            for face_data in frame_data["faces"]:
                all_emotions.append(face_data["dominant_emotion"])
        
        # Calculate dominant emotion across all frames
        if all_emotions:
            emotion_counts = {emotion: all_emotions.count(emotion) for emotion in self.emotion_labels}
            dominant_emotion = max(emotion_counts, key=emotion_counts.get)
            overall_confidence = emotion_counts[dominant_emotion] / len(all_emotions)
        else:
            dominant_emotion = "neutral"
            overall_confidence = 0.0
        
        return {
            "dominant_emotion": dominant_emotion,
            "confidence": overall_confidence,
            "emotion_scores": self._calculate_average_emotions(frame_emotions),
            "face_count": total_faces_detected,
            "frames_analyzed": len(frames),
            "timestamp_data": frame_emotions,
            "analysis_summary": {
                "avg_faces_per_frame": total_faces_detected / len(frames) if frames else 0,
                "emotion_stability": self._calculate_emotion_stability(frame_emotions),
                "engagement_level": self._calculate_engagement_level(frame_emotions)
            }
        }
    
    def _predict_emotions_mock(self) -> Dict[str, float]:
        """Mock emotion prediction - in production would use trained model"""
        # Generate realistic emotion scores that sum to 1.0
        base_scores = np.random.dirichlet(np.ones(len(self.emotion_labels)), size=1)[0]
        
        # Add some bias towards common sales emotions
        adjustments = {
            'happy': 0.1,
            'neutral': 0.05,
            'surprise': 0.02,
            'fear': -0.05,
            'angry': -0.08
        }
        
        emotion_scores = {}
        for i, emotion in enumerate(self.emotion_labels):
            score = base_scores[i] + adjustments.get(emotion, 0)
            emotion_scores[emotion] = max(0.0, min(1.0, score))
        
        # Normalize to ensure sum is 1.0
        total = sum(emotion_scores.values())
        emotion_scores = {k: v/total for k, v in emotion_scores.items()}
        
        return emotion_scores
    
    def _calculate_average_emotions(self, frame_emotions: List[Dict]) -> Dict[str, float]:
        """Calculate average emotion scores across all frames"""
        if not frame_emotions:
            return {emotion: 0.0 for emotion in self.emotion_labels}
        
        emotion_sums = {emotion: 0.0 for emotion in self.emotion_labels}
        total_faces = 0
        
        for frame_data in frame_emotions:
            for face_data in frame_data["faces"]:
                for emotion, score in face_data["emotion_scores"].items():
                    emotion_sums[emotion] += score
                total_faces += 1
        
        if total_faces == 0:
            return emotion_sums
        
        return {emotion: score/total_faces for emotion, score in emotion_sums.items()}
    
    def _calculate_emotion_stability(self, frame_emotions: List[Dict]) -> float:
        """Calculate how stable emotions are across frames"""
        if len(frame_emotions) < 2:
            return 1.0
        
        dominant_emotions = []
        for frame_data in frame_emotions:
            if frame_data["faces"]:
                # Get most confident face emotion
                best_face = max(frame_data["faces"], key=lambda x: x["confidence"])
                dominant_emotions.append(best_face["dominant_emotion"])
        
        if len(dominant_emotions) < 2:
            return 1.0
        
        # Calculate consistency (same emotion across frames)
        most_common = max(set(dominant_emotions), key=dominant_emotions.count)
        stability = dominant_emotions.count(most_common) / len(dominant_emotions)
        
        return stability
    
    def _calculate_engagement_level(self, frame_emotions: List[Dict]) -> float:
        """Calculate engagement level based on positive emotions and face detection"""
        if not frame_emotions:
            return 0.0
        
        positive_emotions = ['happy', 'surprise']
        engagement_scores = []
        
        for frame_data in frame_emotions:
            if frame_data["faces"]:
                for face_data in frame_data["faces"]:
                    positive_score = sum(
                        face_data["emotion_scores"].get(emotion, 0) 
                        for emotion in positive_emotions
                    )
                    engagement_scores.append(positive_score)
        
        return np.mean(engagement_scores) if engagement_scores else 0.0
    
    def _get_default_emotion_data(self) -> Dict[str, Any]:
        """Return default emotion data when analysis fails"""
        return {
            "dominant_emotion": "neutral",
            "confidence": 0.0,
            "emotion_scores": {emotion: 0.0 for emotion in self.emotion_labels},
            "face_count": 0,
            "frames_analyzed": 0,
            "timestamp_data": [],
            "analysis_summary": {
                "avg_faces_per_frame": 0.0,
                "emotion_stability": 0.0,
                "engagement_level": 0.0
            }
        } 