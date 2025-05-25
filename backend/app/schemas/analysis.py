from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime

class UploadResponse(BaseModel):
    file_id: str
    filename: str
    file_path: str
    file_size: int

class EmotionData(BaseModel):
    dominant_emotion: str
    confidence: float
    emotion_scores: Dict[str, float]
    face_count: int
    timestamp_data: List[Dict[str, Any]]

class SpeechData(BaseModel):
    transcript: str
    confidence: float
    speaking_rate: float
    volume_level: float
    tone_analysis: Dict[str, Any]
    filler_words: List[str]
    pause_analysis: Dict[str, float]

class TextData(BaseModel):
    sentiment: str
    sentiment_score: float
    key_phrases: List[str]
    professionalism_score: float
    clarity_score: float
    persuasiveness_score: float

class CoachingRecommendation(BaseModel):
    category: str
    priority: str  # high, medium, low
    title: str
    description: str
    actionable_steps: List[str]
    examples: List[str]

class AnalysisResponse(BaseModel):
    file_id: str
    analysis_data: Dict[str, Any]
    coaching_recommendations: List[CoachingRecommendation]
    timestamp: Optional[datetime] = None
    
class AnalysisRequest(BaseModel):
    file_id: str
    analysis_types: Optional[List[str]] = ["emotion", "speech", "text"] 