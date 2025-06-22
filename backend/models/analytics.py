"""
Analytics service for the Sleep Science Explainer Bot.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import json

from backend.core.logging import LoggerMixin
from backend.core.config import settings


class AnalyticsService(LoggerMixin):
    """
    Analytics service for tracking user interactions and generating insights.
    
    This service handles:
    - User interaction logging
    - Topic popularity analysis
    - Usage statistics
    - Performance metrics
    """
    
    def __init__(self):
        """Initialize the analytics service."""
        self.logger.info("Initializing AnalyticsService")
        
        # In-memory storage for analytics (in production, this would be in a database)
        self.interactions: List[Dict[str, Any]] = []
        self.topic_counts: Dict[str, int] = {}
        self.user_sessions: Dict[str, Dict[str, Any]] = {}
        
        self.logger.info("AnalyticsService initialized successfully")
    
    async def log_interaction(
        self,
        user_id: str,
        conversation_id: str,
        message: str,
        response: str,
        topic: str,
        additional_data: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Log a user interaction for analytics.
        
        Args:
            user_id: Unique identifier for the user
            conversation_id: Conversation identifier
            message: User's message
            response: Bot's response
            topic: Topic category
            additional_data: Additional analytics data
        """
        interaction = {
            "user_id": user_id,
            "conversation_id": conversation_id,
            "message": message,
            "response": response,
            "topic": topic,
            "timestamp": datetime.utcnow(),
            "message_length": len(message),
            "response_length": len(response),
            "additional_data": additional_data or {}
        }
        
        self.interactions.append(interaction)
        
        # Update topic counts
        self.topic_counts[topic] = self.topic_counts.get(topic, 0) + 1
        
        # Update user session
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {
                "first_seen": datetime.utcnow(),
                "last_seen": datetime.utcnow(),
                "total_interactions": 0,
                "topics": set()
            }
        
        self.user_sessions[user_id]["last_seen"] = datetime.utcnow()
        self.user_sessions[user_id]["total_interactions"] += 1
        self.user_sessions[user_id]["topics"].add(topic)
        
        self.logger.debug(
            "Logged interaction",
            user_id=user_id,
            conversation_id=conversation_id,
            topic=topic
        )
    
    async def get_popular_topics(
        self,
        days: int = 30,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get most popular topics over a time period.
        
        Args:
            days: Number of days to look back
            limit: Maximum number of topics to return
            
        Returns:
            List of popular topics with counts
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Filter interactions by date
        recent_interactions = [
            interaction for interaction in self.interactions
            if interaction["timestamp"] >= cutoff_date
        ]
        
        # Count topics
        topic_counts = {}
        for interaction in recent_interactions:
            topic = interaction["topic"]
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        # Sort by count and return top topics
        sorted_topics = sorted(
            topic_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]
        
        return [
            {"topic": topic, "count": count}
            for topic, count in sorted_topics
        ]
    
    async def get_user_analytics(
        self,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Get analytics for a specific user.
        
        Args:
            user_id: User identifier
            
        Returns:
            User analytics data
        """
        if user_id not in self.user_sessions:
            return {"error": "User not found"}
        
        session = self.user_sessions[user_id]
        user_interactions = [
            interaction for interaction in self.interactions
            if interaction["user_id"] == user_id
        ]
        
        # Calculate user statistics
        total_messages = len(user_interactions)
        avg_message_length = sum(
            interaction["message_length"] for interaction in user_interactions
        ) / total_messages if total_messages > 0 else 0
        
        # Get user's topic preferences
        user_topic_counts = {}
        for interaction in user_interactions:
            topic = interaction["topic"]
            user_topic_counts[topic] = user_topic_counts.get(topic, 0) + 1
        
        return {
            "user_id": user_id,
            "first_seen": session["first_seen"],
            "last_seen": session["last_seen"],
            "total_interactions": session["total_interactions"],
            "total_messages": total_messages,
            "avg_message_length": round(avg_message_length, 2),
            "topics": list(session["topics"]),
            "topic_preferences": user_topic_counts,
            "session_duration": (session["last_seen"] - session["first_seen"]).total_seconds()
        }
    
    async def get_overall_statistics(
        self,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Get overall application statistics.
        
        Args:
            days: Number of days to look back
            
        Returns:
            Overall statistics
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Filter interactions by date
        recent_interactions = [
            interaction for interaction in self.interactions
            if interaction["timestamp"] >= cutoff_date
        ]
        
        if not recent_interactions:
            return {
                "total_interactions": 0,
                "unique_users": 0,
                "avg_message_length": 0,
                "top_topics": [],
                "period_days": days
            }
        
        # Calculate statistics
        total_interactions = len(recent_interactions)
        unique_users = len(set(
            interaction["user_id"] for interaction in recent_interactions
        ))
        
        avg_message_length = sum(
            interaction["message_length"] for interaction in recent_interactions
        ) / total_interactions
        
        # Get top topics
        topic_counts = {}
        for interaction in recent_interactions:
            topic = interaction["topic"]
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        top_topics = sorted(
            topic_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        return {
            "total_interactions": total_interactions,
            "unique_users": unique_users,
            "avg_message_length": round(avg_message_length, 2),
            "top_topics": [
                {"topic": topic, "count": count}
                for topic, count in top_topics
            ],
            "period_days": days,
            "period_start": cutoff_date,
            "period_end": datetime.utcnow()
        }
    
    async def get_conversation_analytics(
        self,
        conversation_id: str
    ) -> Dict[str, Any]:
        """
        Get analytics for a specific conversation.
        
        Args:
            conversation_id: Conversation identifier
            
        Returns:
            Conversation analytics data
        """
        conversation_interactions = [
            interaction for interaction in self.interactions
            if interaction["conversation_id"] == conversation_id
        ]
        
        if not conversation_interactions:
            return {"error": "Conversation not found"}
        
        # Calculate conversation statistics
        total_messages = len(conversation_interactions)
        user_id = conversation_interactions[0]["user_id"]
        
        # Get conversation topics
        topics = list(set(
            interaction["topic"] for interaction in conversation_interactions
        ))
        
        # Calculate average message and response lengths
        avg_message_length = sum(
            interaction["message_length"] for interaction in conversation_interactions
        ) / total_messages
        
        avg_response_length = sum(
            interaction["response_length"] for interaction in conversation_interactions
        ) / total_messages
        
        return {
            "conversation_id": conversation_id,
            "user_id": user_id,
            "total_messages": total_messages,
            "topics": topics,
            "avg_message_length": round(avg_message_length, 2),
            "avg_response_length": round(avg_response_length, 2),
            "start_time": conversation_interactions[0]["timestamp"],
            "end_time": conversation_interactions[-1]["timestamp"],
            "duration_seconds": (
                conversation_interactions[-1]["timestamp"] - 
                conversation_interactions[0]["timestamp"]
            ).total_seconds()
        }
    
    async def cleanup_old_data(self, days: int = 90) -> None:
        """
        Clean up old analytics data.
        
        Args:
            days: Number of days to keep data for
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Remove old interactions
        self.interactions = [
            interaction for interaction in self.interactions
            if interaction["timestamp"] >= cutoff_date
        ]
        
        # Clean up user sessions
        expired_users = []
        for user_id, session in self.user_sessions.items():
            if session["last_seen"] < cutoff_date:
                expired_users.append(user_id)
        
        for user_id in expired_users:
            del self.user_sessions[user_id]
        
        self.logger.info(
            "Cleaned up old analytics data",
            cutoff_date=cutoff_date,
            remaining_interactions=len(self.interactions),
            remaining_users=len(self.user_sessions)
        ) 