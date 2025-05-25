import asyncio
import logging
from typing import Dict, List, Any
import json
from datetime import datetime

logger = logging.getLogger(__name__)

class CoachingAgent:
    """AI agent for generating personalized sales coaching recommendations"""
    
    def __init__(self):
        self.coaching_categories = {
            "presentation_style": "Presentation Delivery & Style",
            "emotional_intelligence": "Emotional Intelligence & Rapport",
            "communication": "Communication Effectiveness",
            "persuasion": "Persuasion & Influence",
            "confidence": "Confidence & Authority",
            "engagement": "Audience Engagement"
        }
        
        # Coaching frameworks and best practices
        self.coaching_frameworks = self._initialize_coaching_frameworks()
    
    def _initialize_coaching_frameworks(self) -> Dict[str, Any]:
        """Initialize coaching frameworks and best practices"""
        return {
            "emotion_coaching": {
                "positive_emotions": {
                    "happy": "Maintain this positive energy throughout your presentation",
                    "surprise": "Good use of surprise elements to maintain interest",
                    "neutral": "Consider adding more emotional variety to engage your audience"
                },
                "negative_emotions": {
                    "fear": "Work on building confidence through practice and preparation",
                    "angry": "Channel this energy into passion for your product/service",
                    "sad": "Focus on the positive outcomes and benefits for your audience"
                }
            },
            "speech_coaching": {
                "pacing": {
                    "too_fast": "Slow down to ensure your message is clearly understood",
                    "too_slow": "Increase your pace to maintain engagement",
                    "optimal": "Excellent pacing - maintain this rhythm"
                },
                "volume": {
                    "too_quiet": "Speak with more volume to project confidence",
                    "too_loud": "Moderate your volume for better audience comfort",
                    "good": "Great volume control"
                }
            },
            "content_coaching": {
                "persuasion": {
                    "low": "Include more benefit statements and social proof",
                    "medium": "Good persuasive elements, consider adding urgency",
                    "high": "Excellent persuasive language"
                },
                "clarity": {
                    "low": "Simplify your language and use shorter sentences",
                    "medium": "Good clarity, ensure key points are emphasized",
                    "high": "Excellent clarity and structure"
                }
            }
        }
    
    async def generate_recommendations(self, analysis_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate personalized coaching recommendations based on multimodal analysis
        
        Args:
            analysis_data: Combined analysis results from all modalities
            
        Returns:
            List of coaching recommendations
        """
        try:
            logger.info("Generating coaching recommendations")
            
            # Run recommendation generation in thread pool
            loop = asyncio.get_event_loop()
            recommendations = await loop.run_in_executor(
                None, 
                self._generate_recommendations_sync, 
                analysis_data
            )
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return self._get_default_recommendations()
    
    def _generate_recommendations_sync(self, analysis_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Synchronous recommendation generation"""
        recommendations = []
        
        # Extract analysis components
        emotions = analysis_data.get("emotions", {})
        speech = analysis_data.get("speech", {})
        text = analysis_data.get("text", {})
        
        # Generate emotion-based recommendations
        emotion_recs = self._generate_emotion_recommendations(emotions)
        recommendations.extend(emotion_recs)
        
        # Generate speech-based recommendations
        speech_recs = self._generate_speech_recommendations(speech)
        recommendations.extend(speech_recs)
        
        # Generate text-based recommendations
        text_recs = self._generate_text_recommendations(text)
        recommendations.extend(text_recs)
        
        # Generate holistic recommendations
        holistic_recs = self._generate_holistic_recommendations(analysis_data)
        recommendations.extend(holistic_recs)
        
        # Priority ranking and deduplication
        recommendations = self._prioritize_and_deduplicate(recommendations)
        
        # Limit to top 8 recommendations
        return recommendations[:8]
    
    def _generate_emotion_recommendations(self, emotions: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate recommendations based on emotion analysis"""
        recommendations = []
        
        if not emotions:
            return recommendations
        
        dominant_emotion = emotions.get("dominant_emotion", "neutral")
        confidence = emotions.get("confidence", 0)
        engagement_level = emotions.get("analysis_summary", {}).get("engagement_level", 0)
        
        # Emotion-specific recommendations
        if dominant_emotion in ["fear", "sad"]:
            recommendations.append({
                "category": "emotional_intelligence",
                "priority": "high",
                "title": "Build Emotional Confidence",
                "description": f"Your predominant emotion ({dominant_emotion}) suggests room for confidence building. Practice positive visualization before presentations.",
                "actionable_steps": [
                    "Practice power poses before presenting",
                    "Use positive self-talk and affirmations",
                    "Focus on the value you're providing to your audience",
                    "Record yourself practicing to build familiarity"
                ],
                "examples": [
                    "Stand with feet shoulder-width apart, hands on hips for 2 minutes before presenting",
                    "Remind yourself: 'I have valuable insights to share'",
                    "Think about how your solution will help the client succeed"
                ]
            })
        
        if engagement_level < 0.5:
            recommendations.append({
                "category": "engagement",
                "priority": "medium",
                "title": "Increase Emotional Engagement",
                "description": "Your emotional expression could be more engaging. Consider using more animated facial expressions and gestures.",
                "actionable_steps": [
                    "Practice varying your facial expressions",
                    "Use hand gestures to emphasize key points",
                    "Make more frequent eye contact with your audience",
                    "Smile genuinely when discussing positive outcomes"
                ],
                "examples": [
                    "Raise eyebrows when sharing surprising statistics",
                    "Use open palm gestures when explaining benefits",
                    "Nod enthusiastically when discussing client success stories"
                ]
            })
        
        # Stability recommendations
        stability = emotions.get("analysis_summary", {}).get("emotion_stability", 1)
        if stability < 0.7:
            recommendations.append({
                "category": "presentation_style",
                "priority": "medium",
                "title": "Improve Emotional Consistency",
                "description": "Your emotions varied significantly throughout the presentation. Work on maintaining consistent positive energy.",
                "actionable_steps": [
                    "Prepare emotional cues for different sections",
                    "Practice maintaining enthusiasm throughout",
                    "Use transitional phrases to maintain energy",
                    "Take brief pauses to reset your emotional state"
                ],
                "examples": [
                    "Start each section with renewed enthusiasm",
                    "Use phrases like 'What's really exciting is...'",
                    "Pause and take a breath before key points"
                ]
            })
        
        return recommendations
    
    def _generate_speech_recommendations(self, speech: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate recommendations based on speech analysis"""
        recommendations = []
        
        if not speech:
            return recommendations
        
        speaking_rate = speech.get("speaking_rate", 0)
        filler_words = speech.get("filler_words", {})
        delivery_metrics = speech.get("delivery_metrics", {})
        
        # Speaking rate recommendations
        if speaking_rate > 0:
            if speaking_rate < 120:
                recommendations.append({
                    "category": "presentation_style",
                    "priority": "medium",
                    "title": "Increase Speaking Pace",
                    "description": f"Your speaking rate of {speaking_rate:.0f} words per minute is below optimal. Consider speaking slightly faster to maintain engagement.",
                    "actionable_steps": [
                        "Practice with a metronome or timer",
                        "Reduce unnecessary pauses between words",
                        "Prepare and rehearse your content thoroughly",
                        "Focus on smooth transitions between ideas"
                    ],
                    "examples": [
                        "Aim for 130-140 words per minute",
                        "Practice reading aloud with energy",
                        "Record yourself and compare to professional speakers"
                    ]
                })
            elif speaking_rate > 150:
                recommendations.append({
                    "category": "presentation_style",
                    "priority": "high",
                    "title": "Slow Down for Clarity",
                    "description": f"Your speaking rate of {speaking_rate:.0f} words per minute may be too fast. Slow down to ensure comprehension.",
                    "actionable_steps": [
                        "Practice deliberate pacing",
                        "Add strategic pauses for emphasis",
                        "Focus on clear articulation",
                        "Allow time for key points to sink in"
                    ],
                    "examples": [
                        "Pause for 2-3 seconds after important statistics",
                        "Slow down when explaining complex concepts",
                        "Use the phrase 'Let me emphasize this point...'"
                    ]
                })
        
        # Filler words recommendations
        total_fillers = sum(filler_words.values()) if filler_words else 0
        if total_fillers > 3:
            recommendations.append({
                "category": "communication",
                "priority": "medium",
                "title": "Reduce Filler Words",
                "description": f"You used {total_fillers} filler words. Reducing these will make you sound more confident and professional.",
                "actionable_steps": [
                    "Practice pausing instead of using fillers",
                    "Slow down your speech to think ahead",
                    "Prepare and rehearse key transitions",
                    "Record yourself to identify filler patterns"
                ],
                "examples": [
                    "Instead of 'um', pause silently for 1-2 seconds",
                    "Replace 'you know' with 'as you can see'",
                    "Use 'let me explain' instead of 'basically'"
                ]
            })
        
        # Confidence recommendations based on delivery metrics
        confidence_score = delivery_metrics.get("confidence_score", 0)
        if confidence_score < 0.7:
            recommendations.append({
                "category": "confidence",
                "priority": "high",
                "title": "Project More Vocal Confidence",
                "description": "Your vocal delivery could project more confidence. Focus on volume, pace, and definitiveness.",
                "actionable_steps": [
                    "Speak with consistent volume",
                    "Use definitive language",
                    "Avoid uptalk (rising intonation on statements)",
                    "Practice breathing exercises for voice control"
                ],
                "examples": [
                    "Say 'This will increase efficiency' instead of 'This might help'",
                    "End statements with falling intonation",
                    "Breathe from your diaphragm for stronger voice projection"
                ]
            })
        
        return recommendations
    
    def _generate_text_recommendations(self, text: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate recommendations based on text analysis"""
        recommendations = []
        
        if not text:
            return recommendations
        
        persuasiveness_score = text.get("persuasiveness_score", 0)
        professionalism_score = text.get("professionalism_score", 0)
        clarity_score = text.get("clarity_score", 0)
        sentiment = text.get("sentiment", "neutral")
        
        # Persuasiveness recommendations
        if persuasiveness_score < 0.6:
            recommendations.append({
                "category": "persuasion",
                "priority": "high",
                "title": "Strengthen Persuasive Language",
                "description": "Your message could be more persuasive. Include more benefit statements and calls to action.",
                "actionable_steps": [
                    "Highlight specific benefits for the client",
                    "Include quantifiable results and ROI",
                    "Add social proof and testimonials",
                    "End with clear next steps"
                ],
                "examples": [
                    "'Companies like yours have seen 40% efficiency gains'",
                    "'This investment will pay for itself in 6 months'",
                    "'Shall we schedule a pilot program next week?'"
                ]
            })
        
        # Professionalism recommendations
        if professionalism_score < 0.7:
            recommendations.append({
                "category": "communication",
                "priority": "medium",
                "title": "Enhance Professional Language",
                "description": "Consider using more professional vocabulary and reducing casual expressions.",
                "actionable_steps": [
                    "Replace casual words with professional alternatives",
                    "Use industry-specific terminology appropriately",
                    "Structure sentences more formally",
                    "Avoid colloquialisms and slang"
                ],
                "examples": [
                    "Say 'solution' instead of 'thing'",
                    "Use 'implement' instead of 'do'",
                    "Replace 'awesome' with 'excellent' or 'outstanding'"
                ]
            })
        
        # Clarity recommendations
        if clarity_score < 0.6:
            recommendations.append({
                "category": "communication",
                "priority": "high",
                "title": "Improve Message Clarity",
                "description": "Your message could be clearer and easier to understand. Simplify complex sentences and concepts.",
                "actionable_steps": [
                    "Use shorter, simpler sentences",
                    "Break complex ideas into steps",
                    "Define technical terms",
                    "Use analogies and examples"
                ],
                "examples": [
                    "Instead of long sentences, use bullet points",
                    "'Think of it like...' for analogies",
                    "'In simple terms, this means...'"
                ]
            })
        
        # Sentiment recommendations
        if sentiment == "negative":
            recommendations.append({
                "category": "communication",
                "priority": "high",
                "title": "Improve Positive Messaging",
                "description": "Your language contains more negative than positive elements. Reframe challenges as opportunities.",
                "actionable_steps": [
                    "Focus on solutions rather than problems",
                    "Use positive language to describe outcomes",
                    "Reframe challenges as opportunities for improvement",
                    "Emphasize benefits and value propositions"
                ],
                "examples": [
                    "'This addresses your efficiency challenges' becomes 'This boosts your efficiency'",
                    "'Problems' become 'opportunities for improvement'",
                    "Focus on 'what you'll gain' not 'what you're missing'"
                ]
            })
        
        return recommendations
    
    def _generate_holistic_recommendations(self, analysis_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate holistic recommendations based on combined analysis"""
        recommendations = []
        
        # Check for consistent themes across modalities
        emotions = analysis_data.get("emotions", {})
        speech = analysis_data.get("speech", {})
        text = analysis_data.get("text", {})
        
        # Low confidence across modalities
        emotion_confidence = emotions.get("analysis_summary", {}).get("engagement_level", 1)
        speech_confidence = speech.get("delivery_metrics", {}).get("confidence_score", 1)
        text_persuasiveness = text.get("persuasiveness_score", 1)
        
        overall_confidence = (emotion_confidence + speech_confidence + text_persuasiveness) / 3
        
        if overall_confidence < 0.6:
            recommendations.append({
                "category": "confidence",
                "priority": "high",
                "title": "Build Overall Presentation Confidence",
                "description": "Multiple indicators suggest room for confidence improvement across your entire presentation approach.",
                "actionable_steps": [
                    "Practice your presentation multiple times",
                    "Prepare for common questions and objections",
                    "Visualize successful outcomes",
                    "Start with smaller, lower-stakes presentations"
                ],
                "examples": [
                    "Practice in front of colleagues for feedback",
                    "Prepare 3-5 success stories you can share",
                    "Imagine the client saying 'yes' at the end"
                ]
            })
        
        # Engagement optimization
        if emotion_confidence < 0.6 and speech_confidence > 0.7:
            recommendations.append({
                "category": "engagement",
                "priority": "medium",
                "title": "Align Emotional and Vocal Energy",
                "description": "Your vocal delivery is strong, but your emotional expression could match that energy level.",
                "actionable_steps": [
                    "Match facial expressions to your vocal enthusiasm",
                    "Use gestures that complement your confident voice",
                    "Practice in front of a mirror",
                    "Record yourself to observe alignment"
                ],
                "examples": [
                    "Smile when your voice conveys excitement",
                    "Use open gestures when speaking confidently",
                    "Make eye contact when making strong statements"
                ]
            })
        
        return recommendations
    
    def _prioritize_and_deduplicate(self, recommendations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioritize and remove duplicate recommendations"""
        # Priority order
        priority_order = {"high": 3, "medium": 2, "low": 1}
        
        # Remove duplicates based on title
        seen_titles = set()
        unique_recommendations = []
        
        for rec in recommendations:
            if rec["title"] not in seen_titles:
                seen_titles.add(rec["title"])
                unique_recommendations.append(rec)
        
        # Sort by priority
        unique_recommendations.sort(
            key=lambda x: priority_order.get(x["priority"], 0), 
            reverse=True
        )
        
        return unique_recommendations
    
    def _get_default_recommendations(self) -> List[Dict[str, Any]]:
        """Return default recommendations when generation fails"""
        return [
            {
                "category": "general",
                "priority": "medium",
                "title": "Practice and Prepare",
                "description": "Regular practice is the foundation of great presentations. Rehearse your content and anticipate questions.",
                "actionable_steps": [
                    "Practice your presentation multiple times",
                    "Prepare for common questions",
                    "Time your presentation sections",
                    "Get feedback from colleagues"
                ],
                "examples": [
                    "Rehearse in front of a mirror",
                    "Record yourself and review",
                    "Practice with different audience scenarios"
                ]
            }
        ] 