import cv2
import numpy as np
from pathlib import Path
import tempfile
import asyncio
from typing import Dict, List, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class VideoProcessor:
    """Service for processing video files and extracting frames and audio"""
    
    def __init__(self):
        self.temp_dir = Path(tempfile.gettempdir()) / "video_processing"
        self.temp_dir.mkdir(exist_ok=True)
    
    async def process_video(self, video_path: str) -> Dict[str, Any]:
        """
        Process video file and extract frames, audio, and metadata
        
        Args:
            video_path: Path to the video file
            
        Returns:
            Dictionary containing processed video data
        """
        try:
            logger.info(f"Processing video: {video_path}")
            
            # Run CPU-intensive operations in thread pool
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                self._process_video_sync, 
                video_path
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing video {video_path}: {str(e)}")
            raise Exception(f"Video processing failed: {str(e)}")
    
    def _process_video_sync(self, video_path: str) -> Dict[str, Any]:
        """Synchronous video processing"""
        video_path = Path(video_path)
        
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        # Open video file
        cap = cv2.VideoCapture(str(video_path))
        
        if not cap.isOpened():
            raise Exception(f"Could not open video file: {video_path}")
        
        try:
            # Extract video metadata
            metadata = self._extract_metadata(cap)
            
            # Extract frames for emotion analysis
            frames = self._extract_frames(cap, max_frames=30)
            
            # Reset video capture for audio extraction
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            
            # Extract audio (mock implementation - would use ffmpeg in production)
            audio_data = self._extract_audio_mock(video_path)
            
            # Generate mock transcript (would use speech-to-text service)
            transcript = self._generate_mock_transcript()
            
            return {
                "metadata": metadata,
                "frames": frames,
                "audio": audio_data,
                "transcript": transcript,
                "timestamp": datetime.now().isoformat()
            }
            
        finally:
            cap.release()
    
    def _extract_metadata(self, cap) -> Dict[str, Any]:
        """Extract video metadata"""
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = frame_count / fps if fps > 0 else 0
        
        return {
            "fps": fps,
            "frame_count": frame_count,
            "width": width,
            "height": height,
            "duration_seconds": duration,
            "resolution": f"{width}x{height}"
        }
    
    def _extract_frames(self, cap, max_frames: int = 30) -> List[np.ndarray]:
        """Extract representative frames from video"""
        frames = []
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if frame_count == 0:
            return frames
        
        # Calculate frame intervals to get evenly distributed frames
        interval = max(1, frame_count // max_frames)
        
        frame_idx = 0
        while len(frames) < max_frames and frame_idx < frame_count:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            
            if ret:
                # Convert BGR to RGB for further processing
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(frame_rgb)
            
            frame_idx += interval
        
        return frames
    
    def _extract_audio_mock(self, video_path: Path) -> Dict[str, Any]:
        """Mock audio extraction - in production would use ffmpeg"""
        return {
            "sample_rate": 44100,
            "duration": 30.5,
            "channels": 2,
            "format": "wav",
            "audio_file_path": None,  # Would contain path to extracted audio
            "volume_analysis": {
                "average_volume": 0.65,
                "peak_volume": 0.89,
                "silence_periods": [{"start": 2.3, "end": 3.1}]
            }
        }
    
    def _generate_mock_transcript(self) -> str:
        """Mock transcript generation - in production would use Whisper or similar"""
        return """Hello, I'm excited to present our new product to you today. 
        This solution can help your company increase efficiency by up to 40%. 
        Let me walk you through the key features and benefits. 
        As you can see from this demonstration, the interface is intuitive and user-friendly. 
        I believe this would be a perfect fit for your organization's needs."""
    
    async def cleanup_temp_files(self):
        """Clean up temporary files created during processing"""
        try:
            for file_path in self.temp_dir.glob("*"):
                if file_path.is_file():
                    file_path.unlink()
        except Exception as e:
            logger.warning(f"Error cleaning up temp files: {str(e)}") 