from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List, Optional
import os
import uuid
from pathlib import Path
import asyncio
import json

from ..services.video_processor import VideoProcessor
from ..services.emotion_detector import EmotionDetector
from ..services.speech_analyzer import SpeechAnalyzer
from ..services.text_analyzer import TextAnalyzer
from ..agents.coaching_agent import CoachingAgent
from ..schemas.analysis import AnalysisResponse, UploadResponse
from ..core.config import settings

router = APIRouter()

# Dependency injection
def get_video_processor():
    return VideoProcessor()

def get_emotion_detector():
    return EmotionDetector()

def get_speech_analyzer():
    return SpeechAnalyzer()

def get_text_analyzer():
    return TextAnalyzer()

def get_coaching_agent():
    return CoachingAgent()

@router.post("/videos/analyze")
async def analyze_video_upload(
    video: UploadFile = File(...),
    video_processor: VideoProcessor = Depends(get_video_processor),
    emotion_detector: EmotionDetector = Depends(get_emotion_detector),
    speech_analyzer: SpeechAnalyzer = Depends(get_speech_analyzer),
    text_analyzer: TextAnalyzer = Depends(get_text_analyzer),
    coaching_agent: CoachingAgent = Depends(get_coaching_agent)
):
    """Upload and analyze a video file in one step"""
    
    # Validate file type
    file_ext = Path(video.filename).suffix.lower()
    if file_ext not in settings.ALLOWED_VIDEO_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file_ext} not allowed. Supported: {settings.ALLOWED_VIDEO_EXTENSIONS}"
        )
    
    # Generate unique filename
    file_id = str(uuid.uuid4())
    filename = f"{file_id}{file_ext}"
    file_path = Path(settings.UPLOAD_DIR) / filename
    
    # Create upload directory if it doesn't exist
    file_path.parent.mkdir(exist_ok=True)
    
    # Save file
    try:
        content = await video.read()
        if len(content) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(status_code=413, detail="File too large")
        
        with open(file_path, "wb") as buffer:
            buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
    try:
        # Process video and extract components
        video_data = await video_processor.process_video(str(file_path))
        
        # Run parallel analysis
        tasks = []
        
        if settings.ENABLE_EMOTION_DETECTION:
            tasks.append(emotion_detector.analyze_emotions(video_data["frames"]))
        
        if settings.ENABLE_SPEECH_ANALYSIS:
            tasks.append(speech_analyzer.analyze_speech(video_data["audio"]))
        
        if settings.ENABLE_TEXT_ANALYSIS and video_data.get("transcript"):
            tasks.append(text_analyzer.analyze_text(video_data["transcript"]))
        
        # Execute analysis tasks
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Compile analysis results
        analysis_data = {
            "file_id": file_id,
            "video_metadata": video_data.get("metadata", {}),
            "emotions": results[0] if len(results) > 0 and not isinstance(results[0], Exception) else {},
            "speech": results[1] if len(results) > 1 and not isinstance(results[1], Exception) else {},
            "text": results[2] if len(results) > 2 and not isinstance(results[2], Exception) else {},
        }
        
        # Generate coaching recommendations
        coaching_recommendations = await coaching_agent.generate_recommendations(analysis_data)
        
        # Format response to match frontend expectations
        return {
            "id": file_id,
            "filename": video.filename,
            "analysis": {
                "overall_score": 78,  # Calculate from analysis data
                "confidence_level": int((analysis_data.get("speech", {}).get("delivery_metrics", {}).get("confidence_score", 0.8)) * 100),
                "engagement_score": int((analysis_data.get("emotions", {}).get("analysis_summary", {}).get("engagement_level", 0.75)) * 100),
                "speech_clarity": int((analysis_data.get("speech", {}).get("delivery_metrics", {}).get("clarity_score", 0.8)) * 100),
                "body_language": 76,  # Default for now
                "emotions": analysis_data.get("emotions", {}).get("emotion_scores", {}),
                "transcript": analysis_data.get("speech", {}).get("transcript", ""),
                "coaching_feedback": {
                    "strengths": [rec["title"] for rec in coaching_recommendations if rec.get("priority") == "low"],
                    "improvements": [rec["description"] for rec in coaching_recommendations if rec.get("priority") == "medium"],
                    "recommendations": [rec["title"] for rec in coaching_recommendations if rec.get("priority") == "high"]
                },
                "metrics": {
                    "speech_rate": analysis_data.get("speech", {}).get("speaking_rate", 165),
                    "pause_frequency": 12,  # Default
                    "filler_words": len(analysis_data.get("speech", {}).get("filler_words", {})),
                    "gesture_frequency": 23,  # Default
                    "eye_contact_percentage": 78  # Default
                }
            },
            "created_at": video_data.get("timestamp")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    finally:
        # Clean up uploaded file
        try:
            if file_path.exists():
                file_path.unlink()
        except Exception:
            pass  # Ignore cleanup errors

@router.get("/videos/history")
async def get_analysis_history():
    """Get analysis history - returns empty for now"""
    return []

@router.post("/upload", response_model=UploadResponse)
async def upload_video(
    file: UploadFile = File(...),
    video_processor: VideoProcessor = Depends(get_video_processor)
):
    """Upload a video file for analysis (legacy endpoint)"""
    
    # Validate file type
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in settings.ALLOWED_VIDEO_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file_ext} not allowed. Supported: {settings.ALLOWED_VIDEO_EXTENSIONS}"
        )
    
    # Generate unique filename
    file_id = str(uuid.uuid4())
    filename = f"{file_id}{file_ext}"
    file_path = Path(settings.UPLOAD_DIR) / filename
    
    # Create upload directory if it doesn't exist
    file_path.parent.mkdir(exist_ok=True)
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            if len(content) > settings.MAX_UPLOAD_SIZE:
                raise HTTPException(status_code=413, detail="File too large")
            buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
    return UploadResponse(
        file_id=file_id,
        filename=file.filename,
        file_path=str(file_path),
        file_size=len(content)
    )

@router.post("/analyze/{file_id}", response_model=AnalysisResponse)
async def analyze_video(
    file_id: str,
    video_processor: VideoProcessor = Depends(get_video_processor),
    emotion_detector: EmotionDetector = Depends(get_emotion_detector),
    speech_analyzer: SpeechAnalyzer = Depends(get_speech_analyzer),
    text_analyzer: TextAnalyzer = Depends(get_text_analyzer),
    coaching_agent: CoachingAgent = Depends(get_coaching_agent)
):
    """Analyze uploaded video using multimodal AI (legacy endpoint)"""
    
    # Find the file
    file_path = None
    for ext in settings.ALLOWED_VIDEO_EXTENSIONS:
        potential_path = Path(settings.UPLOAD_DIR) / f"{file_id}{ext}"
        if potential_path.exists():
            file_path = potential_path
            break
    
    if not file_path:
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        # Process video and extract components
        video_data = await video_processor.process_video(str(file_path))
        
        # Run parallel analysis
        tasks = []
        
        if settings.ENABLE_EMOTION_DETECTION:
            tasks.append(emotion_detector.analyze_emotions(video_data["frames"]))
        
        if settings.ENABLE_SPEECH_ANALYSIS:
            tasks.append(speech_analyzer.analyze_speech(video_data["audio"]))
        
        if settings.ENABLE_TEXT_ANALYSIS and video_data.get("transcript"):
            tasks.append(text_analyzer.analyze_text(video_data["transcript"]))
        
        # Execute analysis tasks
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Compile analysis results
        analysis_data = {
            "file_id": file_id,
            "video_metadata": video_data.get("metadata", {}),
            "emotions": results[0] if len(results) > 0 and not isinstance(results[0], Exception) else {},
            "speech": results[1] if len(results) > 1 and not isinstance(results[1], Exception) else {},
            "text": results[2] if len(results) > 2 and not isinstance(results[2], Exception) else {},
        }
        
        # Generate coaching recommendations
        coaching_recommendations = await coaching_agent.generate_recommendations(analysis_data)
        
        return AnalysisResponse(
            file_id=file_id,
            analysis_data=analysis_data,
            coaching_recommendations=coaching_recommendations,
            timestamp=video_data.get("timestamp")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/analysis/{file_id}")
async def get_analysis(file_id: str):
    """Retrieve analysis results for a file"""
    # This would typically fetch from a database
    # For now, return a mock response
    return {
        "file_id": file_id,
        "status": "completed",
        "message": "Analysis data would be retrieved from storage"
    }

@router.delete("/files/{file_id}")
async def delete_file(file_id: str):
    """Delete uploaded file and analysis data"""
    deleted_files = []
    
    # Try to find and delete the file
    for ext in settings.ALLOWED_VIDEO_EXTENSIONS:
        file_path = Path(settings.UPLOAD_DIR) / f"{file_id}{ext}"
        if file_path.exists():
            file_path.unlink()
            deleted_files.append(str(file_path))
    
    if not deleted_files:
        raise HTTPException(status_code=404, detail="File not found")
    
    return {"deleted_files": deleted_files}

@router.get("/health")
async def health_check():
    """Health check endpoint for the API"""
    return {
        "status": "healthy",
        "services": {
            "video_processing": True,
            "emotion_detection": settings.ENABLE_EMOTION_DETECTION,
            "speech_analysis": settings.ENABLE_SPEECH_ANALYSIS,
            "text_analysis": settings.ENABLE_TEXT_ANALYSIS
        }
    } 