"""
Analytics endpoints for the Sleep Science Explainer Bot.
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import func, distinct

from backend.core.logging import get_logger
from backend.database.connection import db_manager
from backend.database.models import Interaction, User
from backend.models.analytics import AnalyticsService

router = APIRouter()
logger = get_logger(__name__)


class AnalyticsOverview(BaseModel):
    """Analytics overview model."""
    total_interactions: int
    unique_users: int
    avg_message_length: float
    top_topics: List[Dict[str, Any]]
    period_days: int
    period_start: datetime
    period_end: datetime


class TopicAnalytics(BaseModel):
    """Topic analytics model."""
    topic: str
    count: int
    percentage: float
    avg_message_length: float


class UserAnalytics(BaseModel):
    """User analytics model."""
    user_id: str
    first_seen: datetime
    last_seen: datetime
    total_interactions: int
    total_messages: int
    avg_message_length: float
    topics: List[str]
    topic_preferences: Dict[str, int]
    session_duration: float


# Initialize analytics service
analytics_service = AnalyticsService()


@router.get("/analytics/overview", response_model=AnalyticsOverview)
async def get_analytics_overview(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze")
) -> AnalyticsOverview:
    """
    Get overall analytics overview.
    
    Args:
        days: Number of days to look back for analysis
        
    Returns:
        Overview of application analytics
    """
    logger.info("Analytics overview requested", days=days)
    
    db_session = db_manager.get_session()
    try:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        # Base query for the time period
        query = db_session.query(Interaction).filter(Interaction.timestamp.between(start_date, end_date))

        total_interactions = query.count()
        
        # Since user_id is not fully implemented in the Interaction model yet,
        # we'll count unique conversations as a proxy for users for now.
        unique_users = query.with_entities(func.count(distinct(Interaction.conversation_id))).scalar()
        
        avg_message_length = query.with_entities(func.avg(Interaction.message_length)).scalar()

        # Since topic is hardcoded, we'll create a placeholder for top_topics
        top_topics = []
        if total_interactions > 0:
            top_topics.append({"topic": "sleep_science", "count": total_interactions})
        
        return AnalyticsOverview(
            total_interactions=total_interactions or 0,
            unique_users=unique_users or 0,
            avg_message_length=round(avg_message_length, 2) if avg_message_length else 0.0,
            top_topics=top_topics,
            period_days=days,
            period_start=start_date,
            period_end=end_date
        )
        
    except Exception as e:
        logger.error("Error getting analytics overview", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve analytics overview"
        )
    finally:
        db_session.close()


@router.get("/analytics/topics", response_model=List[TopicAnalytics])
async def get_topic_analytics(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of topics")
) -> List[TopicAnalytics]:
    """
    Get analytics for popular topics.
    
    Args:
        days: Number of days to look back
        limit: Maximum number of topics to return
        
    Returns:
        List of topic analytics
    """
    logger.info("Topic analytics requested", days=days, limit=limit)
    
    try:
        popular_topics = await analytics_service.get_popular_topics(
            days=days,
            limit=limit
        )
        
        # Calculate percentages and additional metrics
        total_interactions = sum(topic["count"] for topic in popular_topics)
        
        topic_analytics = []
        for topic_data in popular_topics:
            percentage = (topic_data["count"] / total_interactions * 100) if total_interactions > 0 else 0
            
            topic_analytics.append(TopicAnalytics(
                topic=topic_data["topic"],
                count=topic_data["count"],
                percentage=round(percentage, 2),
                avg_message_length=0.0  # TODO: Calculate actual average
            ))
        
        return topic_analytics
        
    except Exception as e:
        logger.error("Error getting topic analytics", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve topic analytics"
        )


@router.get("/analytics/users/{user_id}", response_model=UserAnalytics)
async def get_user_analytics(user_id: str) -> UserAnalytics:
    """
    Get analytics for a specific user.
    
    Args:
        user_id: User identifier
        
    Returns:
        User analytics data
    """
    logger.info("User analytics requested", user_id=user_id)
    
    try:
        user_stats = await analytics_service.get_user_analytics(user_id)
        
        if "error" in user_stats:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        
        return UserAnalytics(
            user_id=user_stats["user_id"],
            first_seen=user_stats["first_seen"],
            last_seen=user_stats["last_seen"],
            total_interactions=user_stats["total_interactions"],
            total_messages=user_stats["total_messages"],
            avg_message_length=user_stats["avg_message_length"],
            topics=user_stats["topics"],
            topic_preferences=user_stats["topic_preferences"],
            session_duration=user_stats["session_duration"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting user analytics", error=str(e), user_id=user_id)
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve user analytics"
        )


@router.get("/analytics/conversations/{conversation_id}")
async def get_conversation_analytics(conversation_id: str) -> Dict[str, Any]:
    """
    Get analytics for a specific conversation.
    
    Args:
        conversation_id: Conversation identifier
        
    Returns:
        Conversation analytics data
    """
    logger.info("Conversation analytics requested", conversation_id=conversation_id)
    
    try:
        conversation_stats = await analytics_service.get_conversation_analytics(conversation_id)
        
        if "error" in conversation_stats:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found"
            )
        
        return conversation_stats
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Error getting conversation analytics",
            error=str(e),
            conversation_id=conversation_id
        )
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve conversation analytics"
        )


@router.get("/analytics/trends")
async def get_usage_trends(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    interval: str = Query("daily", description="Time interval (daily, weekly, monthly)")
) -> Dict[str, Any]:
    """
    Get usage trends over time.
    
    Args:
        days: Number of days to look back
        interval: Time interval for grouping data
        
    Returns:
        Usage trends data
    """
    logger.info("Usage trends requested", days=days, interval=interval)
    
    try:
        # TODO: Implement actual trend calculation
        # For now, return placeholder data
        trends = {
            "period_days": days,
            "interval": interval,
            "data": [
                {
                    "date": (datetime.utcnow() - timedelta(days=i)).strftime("%Y-%m-%d"),
                    "interactions": 0,
                    "users": 0
                }
                for i in range(days, 0, -1)
            ]
        }
        
        return trends
        
    except Exception as e:
        logger.error("Error getting usage trends", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve usage trends"
        )


@router.post("/analytics/cleanup")
async def cleanup_analytics_data(
    days: int = Query(90, ge=1, le=365, description="Number of days to keep data for")
) -> Dict[str, str]:
    """
    Clean up old analytics data.
    
    Args:
        days: Number of days to keep data for
        
    Returns:
        Cleanup status message
    """
    logger.info("Analytics cleanup requested", retention_days=days)
    
    try:
        await analytics_service.cleanup_old_data(days=days)
        
        return {
            "message": f"Successfully cleaned up analytics data older than {days} days"
        }
        
    except Exception as e:
        logger.error("Error cleaning up analytics data", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to cleanup analytics data"
        )


@router.get("/analytics/export")
async def export_analytics_data(
    format: str = Query("json", description="Export format (json, csv)"),
    days: int = Query(30, ge=1, le=365, description="Number of days to export")
) -> Dict[str, Any]:
    """
    Export analytics data.
    
    Args:
        format: Export format
        days: Number of days to export
        
    Returns:
        Exported analytics data
    """
    logger.info("Analytics export requested", format=format, days=days)
    
    try:
        # TODO: Implement actual data export
        # For now, return placeholder
        export_data = {
            "format": format,
            "period_days": days,
            "exported_at": datetime.utcnow(),
            "data": {
                "interactions": [],
                "users": [],
                "topics": []
            }
        }
        
        return export_data
        
    except Exception as e:
        logger.error("Error exporting analytics data", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to export analytics data"
        ) 