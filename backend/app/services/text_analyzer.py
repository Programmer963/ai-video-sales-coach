import asyncio
import logging
from typing import Dict, List, Any
import re
from collections import Counter
import numpy as np

logger = logging.getLogger(__name__)

class TextAnalyzer:
    """Service for analyzing text content for sentiment, persuasiveness, and communication effectiveness"""
    
    def __init__(self):
        # Positive sentiment words
        self.positive_words = [
            'excellent', 'amazing', 'fantastic', 'great', 'wonderful', 'outstanding',
            'beneficial', 'effective', 'successful', 'proven', 'innovative', 'revolutionary',
            'powerful', 'exceptional', 'remarkable', 'impressive', 'valuable', 'advantageous'
        ]
        
        # Negative sentiment words
        self.negative_words = [
            'terrible', 'awful', 'bad', 'poor', 'weak', 'disappointing',
            'difficult', 'challenging', 'problematic', 'concerning', 'inadequate',
            'insufficient', 'limited', 'restricted', 'complicated', 'confusing'
        ]
        
        # Persuasive language indicators
        self.persuasive_words = [
            'proven', 'guaranteed', 'exclusive', 'limited', 'opportunity', 'benefit',
            'advantage', 'solution', 'results', 'success', 'growth', 'increase',
            'improve', 'enhance', 'optimize', 'maximize', 'achieve', 'deliver'
        ]
        
        # Professional vocabulary
        self.professional_words = [
            'strategy', 'implementation', 'optimization', 'efficiency', 'productivity',
            'performance', 'methodology', 'framework', 'analysis', 'evaluation',
            'assessment', 'recommendation', 'proposal', 'initiative', 'objective'
        ]
    
    async def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze text for sentiment, persuasiveness, and communication effectiveness
        
        Args:
            text: Text content to analyze
            
        Returns:
            Dictionary containing text analysis results
        """
        try:
            logger.info("Analyzing text content")
            
            # Run analysis in thread pool for CPU-intensive operations
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                self._analyze_text_sync, 
                text
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing text: {str(e)}")
            return self._get_default_text_data()
    
    def _analyze_text_sync(self, text: str) -> Dict[str, Any]:
        """Synchronous text analysis"""
        if not text or not text.strip():
            return self._get_default_text_data()
        
        # Basic text preprocessing
        cleaned_text = self._preprocess_text(text)
        words = cleaned_text.split()
        
        # Sentiment analysis
        sentiment_data = self._analyze_sentiment(cleaned_text, words)
        
        # Persuasiveness analysis
        persuasiveness_data = self._analyze_persuasiveness(cleaned_text, words)
        
        # Professionalism analysis
        professionalism_data = self._analyze_professionalism(cleaned_text, words)
        
        # Clarity analysis
        clarity_data = self._analyze_clarity(text, words)
        
        # Key phrase extraction
        key_phrases = self._extract_key_phrases(cleaned_text)
        
        # Communication style analysis
        style_analysis = self._analyze_communication_style(text, words)
        
        return {
            "sentiment": sentiment_data["sentiment"],
            "sentiment_score": sentiment_data["score"],
            "key_phrases": key_phrases,
            "professionalism_score": professionalism_data["score"],
            "clarity_score": clarity_data["score"],
            "persuasiveness_score": persuasiveness_data["score"],
            "word_count": len(words),
            "sentence_count": len(re.split(r'[.!?]+', text)),
            "detailed_analysis": {
                "sentiment_breakdown": sentiment_data,
                "persuasiveness_breakdown": persuasiveness_data,
                "professionalism_breakdown": professionalism_data,
                "clarity_breakdown": clarity_data,
                "communication_style": style_analysis
            },
            "recommendations": self._generate_text_recommendations({
                "sentiment": sentiment_data,
                "persuasiveness": persuasiveness_data,
                "professionalism": professionalism_data,
                "clarity": clarity_data
            })
        }
    
    def _preprocess_text(self, text: str) -> str:
        """Clean and preprocess text"""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        # Convert to lowercase for analysis
        return text.lower()
    
    def _analyze_sentiment(self, text: str, words: List[str]) -> Dict[str, Any]:
        """Analyze sentiment of the text"""
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)
        
        # Calculate sentiment score
        total_sentiment_words = positive_count + negative_count
        if total_sentiment_words == 0:
            sentiment_score = 0.0
            sentiment = "neutral"
        else:
            sentiment_score = (positive_count - negative_count) / len(words)
            if sentiment_score > 0.02:
                sentiment = "positive"
            elif sentiment_score < -0.02:
                sentiment = "negative"
            else:
                sentiment = "neutral"
        
        return {
            "sentiment": sentiment,
            "score": sentiment_score,
            "positive_words_count": positive_count,
            "negative_words_count": negative_count,
            "positive_words": [word for word in words if word in self.positive_words],
            "negative_words": [word for word in words if word in self.negative_words]
        }
    
    def _analyze_persuasiveness(self, text: str, words: List[str]) -> Dict[str, Any]:
        """Analyze persuasiveness of the text"""
        persuasive_count = sum(1 for word in words if word in self.persuasive_words)
        persuasive_ratio = persuasive_count / len(words) if words else 0
        
        # Check for persuasive structures
        call_to_action = len(re.findall(r'\b(call|contact|reach|schedule|book|sign|register)\b', text))
        urgency_indicators = len(re.findall(r'\b(now|today|immediately|limited|exclusive|urgent)\b', text))
        benefit_statements = len(re.findall(r'\b(benefit|advantage|gain|improve|increase|save)\b', text))
        
        # Calculate overall persuasiveness score
        structure_score = min(1.0, (call_to_action + urgency_indicators + benefit_statements) / 10)
        vocabulary_score = min(1.0, persuasive_ratio * 10)
        
        persuasiveness_score = (structure_score + vocabulary_score) / 2
        
        return {
            "score": persuasiveness_score,
            "persuasive_words_count": persuasive_count,
            "persuasive_words": [word for word in words if word in self.persuasive_words],
            "call_to_action_count": call_to_action,
            "urgency_indicators": urgency_indicators,
            "benefit_statements": benefit_statements,
            "structure_score": structure_score,
            "vocabulary_score": vocabulary_score
        }
    
    def _analyze_professionalism(self, text: str, words: List[str]) -> Dict[str, Any]:
        """Analyze professionalism of the text"""
        professional_count = sum(1 for word in words if word in self.professional_words)
        professional_ratio = professional_count / len(words) if words else 0
        
        # Check for unprofessional elements
        casual_words = ['like', 'yeah', 'okay', 'cool', 'awesome', 'stuff', 'things']
        casual_count = sum(1 for word in words if word in casual_words)
        
        # Check for proper grammar indicators (simplified)
        proper_capitalization = len(re.findall(r'\b[A-Z][a-z]+\b', text)) / len(words) if words else 0
        
        # Calculate professionalism score
        vocabulary_score = min(1.0, professional_ratio * 15)
        casual_penalty = min(0.5, casual_count / len(words) * 10) if words else 0
        
        professionalism_score = max(0.0, vocabulary_score - casual_penalty + 0.5)
        
        return {
            "score": min(1.0, professionalism_score),
            "professional_words_count": professional_count,
            "professional_words": [word for word in words if word in self.professional_words],
            "casual_words_count": casual_count,
            "vocabulary_score": vocabulary_score,
            "casual_penalty": casual_penalty
        }
    
    def _analyze_clarity(self, original_text: str, words: List[str]) -> Dict[str, Any]:
        """Analyze clarity and readability of the text"""
        sentences = re.split(r'[.!?]+', original_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Average sentence length
        avg_sentence_length = np.mean([len(s.split()) for s in sentences]) if sentences else 0
        
        # Complex words (words with 3+ syllables, simplified estimation)
        complex_words = [word for word in words if len(word) > 8]
        complex_word_ratio = len(complex_words) / len(words) if words else 0
        
        # Readability score (simplified Flesch-like calculation)
        if sentences and words:
            readability_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * complex_word_ratio)
            readability_score = max(0, min(100, readability_score)) / 100  # Normalize to 0-1
        else:
            readability_score = 0.0
        
        return {
            "score": readability_score,
            "average_sentence_length": avg_sentence_length,
            "complex_word_ratio": complex_word_ratio,
            "sentence_count": len(sentences),
            "readability_level": self._get_readability_level(readability_score)
        }
    
    def _extract_key_phrases(self, text: str) -> List[str]:
        """Extract key phrases from the text"""
        # Simple key phrase extraction based on common sales/business terms
        phrases = []
        
        # Look for noun phrases (simplified)
        noun_phrases = re.findall(r'\b(?:our|the|a|an)\s+\w+(?:\s+\w+)*(?:\s+(?:solution|product|service|platform|system|approach|strategy|method))\b', text)
        phrases.extend(noun_phrases[:5])  # Limit to top 5
        
        # Look for benefit phrases
        benefit_phrases = re.findall(r'\b(?:increase|improve|enhance|reduce|save|boost|optimize)\s+\w+(?:\s+\w+)*\b', text)
        phrases.extend(benefit_phrases[:3])
        
        # Look for quantified benefits
        number_phrases = re.findall(r'\b\d+%?\s+\w+(?:\s+\w+)*\b', text)
        phrases.extend(number_phrases[:3])
        
        return list(set(phrases))  # Remove duplicates
    
    def _analyze_communication_style(self, text: str, words: List[str]) -> Dict[str, Any]:
        """Analyze communication style"""
        # Personal pronouns usage
        first_person = len(re.findall(r'\b(I|me|my|myself)\b', text, re.IGNORECASE))
        second_person = len(re.findall(r'\b(you|your|yourself)\b', text, re.IGNORECASE))
        third_person = len(re.findall(r'\b(he|she|they|them|their)\b', text, re.IGNORECASE))
        
        # Question usage
        questions = len(re.findall(r'\?', text))
        
        # Emphasis words
        emphasis_words = ['very', 'really', 'extremely', 'absolutely', 'definitely', 'certainly']
        emphasis_count = sum(1 for word in words if word in emphasis_words)
        
        return {
            "first_person_usage": first_person,
            "second_person_usage": second_person,
            "third_person_usage": third_person,
            "question_count": questions,
            "emphasis_word_count": emphasis_count,
            "style_indicators": {
                "personal": first_person > second_person,
                "engaging": second_person > 0,
                "interactive": questions > 0,
                "emphatic": emphasis_count > 0
            }
        }
    
    def _get_readability_level(self, score: float) -> str:
        """Convert readability score to level description"""
        if score >= 0.9:
            return "Very Easy"
        elif score >= 0.8:
            return "Easy"
        elif score >= 0.7:
            return "Fairly Easy"
        elif score >= 0.6:
            return "Standard"
        elif score >= 0.5:
            return "Fairly Difficult"
        else:
            return "Difficult"
    
    def _generate_text_recommendations(self, analysis: Dict) -> List[Dict[str, str]]:
        """Generate recommendations for text improvement"""
        recommendations = []
        
        # Sentiment recommendations
        if analysis["sentiment"]["score"] < 0:
            recommendations.append({
                "category": "tone",
                "priority": "high",
                "title": "Improve Positive Language",
                "description": "Your message contains more negative than positive language. Consider reframing challenges as opportunities."
            })
        
        # Persuasiveness recommendations
        if analysis["persuasiveness"]["score"] < 0.5:
            recommendations.append({
                "category": "persuasion",
                "priority": "medium",
                "title": "Strengthen Persuasive Elements",
                "description": "Add more benefit statements and clear calls to action to increase persuasiveness."
            })
        
        # Professionalism recommendations
        if analysis["professionalism"]["score"] < 0.7:
            recommendations.append({
                "category": "professionalism",
                "priority": "medium",
                "title": "Enhance Professional Language",
                "description": "Use more professional vocabulary and reduce casual expressions."
            })
        
        # Clarity recommendations
        if analysis["clarity"]["score"] < 0.6:
            recommendations.append({
                "category": "clarity",
                "priority": "high",
                "title": "Improve Readability",
                "description": "Simplify sentence structure and reduce complex words for better clarity."
            })
        
        return recommendations
    
    def _get_default_text_data(self) -> Dict[str, Any]:
        """Return default text data when analysis fails"""
        return {
            "sentiment": "neutral",
            "sentiment_score": 0.0,
            "key_phrases": [],
            "professionalism_score": 0.0,
            "clarity_score": 0.0,
            "persuasiveness_score": 0.0,
            "word_count": 0,
            "sentence_count": 0,
            "detailed_analysis": {},
            "recommendations": []
        } 