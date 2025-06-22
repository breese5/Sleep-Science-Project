"""
Chat endpoints for the Sleep Science Explainer Bot.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

from backend.core.logging import get_logger
from backend.core.config import settings
from backend.models.chat import ChatBot
from backend.models.analytics import AnalyticsService

router = APIRouter()
logger = get_logger(__name__)


class ChatMessage(BaseModel):
    """Individual chat message model."""
    role: str = Field(..., description="Role of the message sender (user/assistant)")
    content: str = Field(..., description="Content of the message")
    timestamp: Optional[datetime] = None


class ChatRequest(BaseModel):
    """Chat request model."""
    message: str = Field(..., description="User's message")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")
    user_id: Optional[str] = Field(None, description="User ID for analytics")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str = Field(..., description="Bot's response")
    conversation_id: str = Field(..., description="Conversation ID")
    timestamp: datetime = Field(..., description="Response timestamp")
    sources: Optional[List[Dict[str, Any]]] = Field(None, description="Sources used for response")
    confidence: Optional[float] = Field(None, description="Confidence score of the response")


class ConversationHistory(BaseModel):
    """Conversation history model."""
    conversation_id: str
    messages: List[ChatMessage]
    created_at: datetime
    updated_at: datetime


# Initialize services (these will be properly initialized later)
chat_bot = ChatBot()
analytics_service = AnalyticsService()


@router.post("/chat", response_model=ChatResponse)
async def chat_with_bot(request: ChatRequest) -> ChatResponse:
    """
    Main chat endpoint for interacting with the Sleep Science Explainer Bot.
    
    This endpoint processes user messages and returns AI-generated responses
    about sleep science topics, research papers, and health guidelines.
    """
    logger.info(
        "Chat request received",
        conversation_id=request.conversation_id,
        user_id=request.user_id,
        message_length=len(request.message)
    )
    
    try:
        # Generate response using the chat bot
        response_data = await chat_bot.generate_response(
            message=request.message,
            conversation_id=request.conversation_id,
            context=request.context
        )
        
        # Log analytics
        if request.user_id:
            await analytics_service.log_interaction(
                user_id=request.user_id,
                conversation_id=response_data["conversation_id"],
                message=request.message,
                response=response_data["response"],
                topic="sleep_science"  # TODO: Extract topic from message
            )
        
        return ChatResponse(
            response=response_data["response"],
            conversation_id=response_data["conversation_id"],
            timestamp=datetime.utcnow(),
            sources=response_data.get("sources"),
            confidence=response_data.get("confidence")
        )
        
    except Exception as e:
        logger.error(
            "Error generating chat response",
            error=str(e),
            conversation_id=request.conversation_id
        )
        raise HTTPException(
            status_code=500,
            detail="Failed to generate response. Please try again."
        )


@router.get("/chat/conversation/{conversation_id}", response_model=ConversationHistory)
async def get_conversation_history(conversation_id: str) -> ConversationHistory:
    """
    Retrieve conversation history for a specific conversation ID.
    """
    logger.info("Retrieving conversation history", conversation_id=conversation_id)
    
    try:
        history = await chat_bot.get_conversation_history(conversation_id)
        return history
    except Exception as e:
        logger.error(
            "Error retrieving conversation history",
            error=str(e),
            conversation_id=conversation_id
        )
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )


@router.delete("/chat/conversation/{conversation_id}")
async def delete_conversation(conversation_id: str) -> Dict[str, str]:
    """
    Delete a conversation and its history.
    """
    logger.info("Deleting conversation", conversation_id=conversation_id)
    
    try:
        await chat_bot.delete_conversation(conversation_id)
        return {"message": "Conversation deleted successfully"}
    except Exception as e:
        logger.error(
            "Error deleting conversation",
            error=str(e),
            conversation_id=conversation_id
        )
        raise HTTPException(
            status_code=500,
            detail="Failed to delete conversation"
        )


@router.get("/chat/topics")
async def get_available_topics() -> Dict[str, List[str]]:
    """
    Get available sleep science topics that the bot can discuss.
    """
    logger.info("Retrieving available topics")
    
    topics = [
        "sleep_cycles",
        "sleep_disorders",
        "sleep_hygiene",
        "sleep_research",
        "sleep_medicine",
        "sleep_apnea",
        "insomnia",
        "circadian_rhythms",
        "sleep_quality",
        "sleep_duration",
        "sleep_environment",
        "sleep_and_health"
    ]
    
    return {"topics": topics} 