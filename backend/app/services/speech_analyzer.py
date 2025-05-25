import asyncio
import logging
from typing import Dict, List, Any
import re
import numpy as np

logger = logging.getLogger(__name__)

class SpeechAnalyzer:
    """Service for analyzing speech patterns, tone, and delivery"""
    
    def __init__(self):
        # Common filler words in sales presentations
        self.filler_words = [
            'um', 'uh', 'like', 'you know', 'so', 'actually', 'basically',
            'literally', 'right', 'okay', 'well', 'I mean', 'kind of', 'sort of'
        ]
        
        # Words indicating confidence/uncertainty
        self.confidence_indicators = {
            'confident': ['definitely', 'certainly', 'absolutely', 'guaranteed', 'proven', 'established'],
            'uncertain': ['maybe', 'perhaps', 'possibly', 'might', 'could be', 'I think', 'probably']
        }
    
    async def analyze_speech(self, audio_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze speech patterns from audio data
        
        Args:
            audio_data: Dictionary containing audio information
            
        Returns:
            Dictionary containing speech analysis results
        """
        try:
            logger.info("Analyzing speech patterns")
            
            # In production, this would:
            # 1. Extract audio features using librosa
            # 2. Analyze prosodic features (pitch, rhythm, volume)
            # 3. Use speech-to-text for transcript analysis
            # 4. Calculate speaking rate, pauses, etc.
            
            # For now, generating realistic mock analysis
            result = await self._analyze_speech_mock(audio_data)
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing speech: {str(e)}")
            return self._get_default_speech_data()
    
    async def _analyze_speech_mock(self, audio_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mock speech analysis - in production would analyze actual audio"""
        
        # Generate realistic mock transcript for analysis
        mock_transcript = self._generate_mock_transcript()
        
        # Analyze transcript
        transcript_analysis = self._analyze_transcript(mock_transcript)
        
        # Generate prosodic analysis
        prosodic_analysis = self._generate_prosodic_analysis(audio_data)
        
        # Calculate overall speech metrics
        speech_metrics = self._calculate_speech_metrics(
            mock_transcript, prosodic_analysis
        )
        
        return {
            "transcript": mock_transcript,
            "confidence": 0.92,  # Mock transcription confidence
            "speaking_rate": speech_metrics["speaking_rate"],
            "volume_level": prosodic_analysis["average_volume"],
            "tone_analysis": prosodic_analysis["tone_analysis"],
            "filler_words": transcript_analysis["filler_words"],
            "pause_analysis": prosodic_analysis["pause_analysis"],
            "linguistic_analysis": transcript_analysis,
            "delivery_metrics": speech_metrics,
            "recommendations": self._generate_speech_recommendations(speech_metrics)
        }
    
    def _generate_mock_transcript(self) -> str:
        """Generate a realistic sales presentation transcript"""
        return """Hello everyone, thank you for your time today. Um, I'm really excited to show you our new solution. 
        This product can, you know, significantly improve your team's productivity. We've seen, uh, companies achieve 
        up to 40% efficiency gains. The interface is, like, really user-friendly and I think you'll find it intuitive. 
        Basically, what we're offering is a comprehensive platform that, well, addresses all your current challenges. 
        I mean, the ROI is absolutely phenomenal. So, any questions about the features I've demonstrated?"""
    
    def _analyze_transcript(self, transcript: str) -> Dict[str, Any]:
        """Analyze transcript for linguistic patterns"""
        words = transcript.lower().split()
        total_words = len(words)
        
        # Count filler words
        filler_count = {}
        total_fillers = 0
        for filler in self.filler_words:
            count = transcript.lower().count(filler)
            if count > 0:
                filler_count[filler] = count
                total_fillers += count
        
        # Analyze confidence indicators
        confident_words = []
        uncertain_words = []
        
        for word_type, word_list in self.confidence_indicators.items():
            for word in word_list:
                if word in transcript.lower():
                    if word_type == 'confident':
                        confident_words.append(word)
                    else:
                        uncertain_words.append(word)
        
        # Calculate readability and professionalism
        sentences = re.split(r'[.!?]+', transcript)
        avg_sentence_length = np.mean([len(s.split()) for s in sentences if s.strip()])
        
        # Professional language score
        professional_score = self._calculate_professional_score(transcript)
        
        return {
            "total_words": total_words,
            "filler_words": filler_count,
            "filler_percentage": (total_fillers / total_words) * 100 if total_words > 0 else 0,
            "confident_language": confident_words,
            "uncertain_language": uncertain_words,
            "confidence_ratio": len(confident_words) / (len(uncertain_words) + 1),
            "average_sentence_length": avg_sentence_length,
            "professional_score": professional_score
        }
    
    def _generate_prosodic_analysis(self, audio_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock prosodic analysis"""
        return {
            "average_volume": 0.65,
            "volume_variance": 0.12,
            "pitch_analysis": {
                "average_pitch": 180.5,  # Hz
                "pitch_range": 85.3,
                "pitch_stability": 0.78
            },
            "tone_analysis": {
                "energy_level": 0.72,
                "enthusiasm_score": 0.68,
                "monotone_risk": 0.25
            },
            "pause_analysis": {
                "total_pause_time": 4.2,  # seconds
                "average_pause_length": 0.8,
                "pause_frequency": 5.2,  # pauses per minute
                "strategic_pauses": 3,
                "filler_pauses": 2
            }
        }
    
    def _calculate_speech_metrics(self, transcript: str, prosodic: Dict) -> Dict[str, Any]:
        """Calculate overall speech delivery metrics"""
        words = transcript.split()
        duration = 45.0  # Mock duration in seconds
        
        speaking_rate = len(words) / (duration / 60)  # words per minute
        
        # Calculate delivery scores
        clarity_score = self._calculate_clarity_score(transcript, prosodic)
        engagement_score = self._calculate_engagement_score(prosodic)
        confidence_score = self._calculate_confidence_score(transcript, prosodic)
        
        return {
            "speaking_rate": speaking_rate,
            "optimal_rate_range": [120, 150],  # words per minute
            "clarity_score": clarity_score,
            "engagement_score": engagement_score,
            "confidence_score": confidence_score,
            "overall_delivery_score": np.mean([clarity_score, engagement_score, confidence_score])
        }
    
    def _calculate_professional_score(self, transcript: str) -> float:
        """Calculate professionalism score based on language use"""
        # Simple scoring based on various factors
        score = 0.7  # Base score
        
        # Deduct for excessive filler words
        filler_ratio = sum(transcript.lower().count(filler) for filler in self.filler_words) / len(transcript.split())
        score -= filler_ratio * 0.5
        
        # Add for professional vocabulary
        professional_words = ['solution', 'productivity', 'efficiency', 'ROI', 'comprehensive', 'platform']
        professional_count = sum(1 for word in professional_words if word in transcript.lower())
        score += (professional_count / len(professional_words)) * 0.2
        
        return max(0.0, min(1.0, score))
    
    def _calculate_clarity_score(self, transcript: str, prosodic: Dict) -> float:
        """Calculate speech clarity score"""
        # Based on volume consistency, speaking rate, and pauses
        volume_consistency = 1.0 - prosodic.get("volume_variance", 0.5)
        pause_quality = min(1.0, prosodic["pause_analysis"]["strategic_pauses"] / 5.0)
        
        return np.mean([volume_consistency, pause_quality, 0.8])  # 0.8 is base clarity
    
    def _calculate_engagement_score(self, prosodic: Dict) -> float:
        """Calculate engagement score based on energy and variation"""
        energy = prosodic["tone_analysis"]["energy_level"]
        enthusiasm = prosodic["tone_analysis"]["enthusiasm_score"]
        monotone_penalty = 1.0 - prosodic["tone_analysis"]["monotone_risk"]
        
        return np.mean([energy, enthusiasm, monotone_penalty])
    
    def _calculate_confidence_score(self, transcript: str, prosodic: Dict) -> float:
        """Calculate confidence score"""
        # Linguistic confidence
        confident_words = len(self.confidence_indicators['confident'])
        uncertain_words = len(self.confidence_indicators['uncertain'])
        linguistic_confidence = confident_words / (confident_words + uncertain_words + 1)
        
        # Vocal confidence (volume, pitch stability)
        vocal_confidence = prosodic["pitch_analysis"]["pitch_stability"]
        
        return np.mean([linguistic_confidence, vocal_confidence])
    
    def _generate_speech_recommendations(self, metrics: Dict) -> List[Dict[str, str]]:
        """Generate specific recommendations for speech improvement"""
        recommendations = []
        
        # Speaking rate recommendations
        speaking_rate = metrics["speaking_rate"]
        if speaking_rate < 120:
            recommendations.append({
                "category": "pacing",
                "priority": "medium",
                "title": "Increase Speaking Pace",
                "description": f"Your speaking rate of {speaking_rate:.0f} WPM is below the optimal range. Consider speaking slightly faster to maintain audience engagement."
            })
        elif speaking_rate > 150:
            recommendations.append({
                "category": "pacing",
                "priority": "high",
                "title": "Slow Down Speech",
                "description": f"Your speaking rate of {speaking_rate:.0f} WPM may be too fast. Slow down to ensure clarity and comprehension."
            })
        
        # Confidence recommendations
        if metrics["confidence_score"] < 0.7:
            recommendations.append({
                "category": "confidence",
                "priority": "high",
                "title": "Boost Vocal Confidence",
                "description": "Use more definitive language and maintain consistent volume to project confidence."
            })
        
        # Engagement recommendations
        if metrics["engagement_score"] < 0.6:
            recommendations.append({
                "category": "engagement",
                "priority": "medium",
                "title": "Increase Energy and Variation",
                "description": "Add more vocal variety and energy to keep your audience engaged."
            })
        
        return recommendations
    
    def _get_default_speech_data(self) -> Dict[str, Any]:
        """Return default speech data when analysis fails"""
        return {
            "transcript": "",
            "confidence": 0.0,
            "speaking_rate": 0.0,
            "volume_level": 0.0,
            "tone_analysis": {},
            "filler_words": {},
            "pause_analysis": {},
            "linguistic_analysis": {},
            "delivery_metrics": {},
            "recommendations": []
        }