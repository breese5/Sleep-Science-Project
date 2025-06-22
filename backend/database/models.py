"""
Database models for the Sleep Science Explainer Bot.
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """User model for tracking user interactions."""
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    total_interactions = Column(Integer, default=0)
    
    # Relationships
    conversations = relationship("Conversation", back_populates="user")
    interactions = relationship("Interaction", back_populates="user")


class Conversation(Base):
    """Conversation model for storing chat sessions."""
    __tablename__ = "conversations"
    
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    title = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", order_by="Message.timestamp")


class Message(Base):
    """Message model for storing individual chat messages."""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String(36), ForeignKey("conversations.id"))
    role = Column(String(20))  # 'user' or 'assistant'
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    message_length = Column(Integer)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")


class Interaction(Base):
    """Interaction model for analytics tracking."""
    __tablename__ = "interactions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(36), ForeignKey("users.id"))
    conversation_id = Column(String(36), ForeignKey("conversations.id"))
    message = Column(Text)
    response = Column(Text)
    topic = Column(String(100))
    message_length = Column(Integer)
    response_length = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
    additional_data = Column(JSON, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="interactions")


class ResearchPaper(Base):
    """Research paper model for caching paper data."""
    __tablename__ = "research_papers"
    
    id = Column(String(50), primary_key=True)
    title = Column(String(500))
    authors = Column(JSON)  # List of author names
    abstract = Column(Text)
    journal = Column(String(255))
    publication_date = Column(DateTime)
    doi = Column(String(100), nullable=True)
    pmid = Column(String(20), nullable=True)
    keywords = Column(JSON)  # List of keywords
    source = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class SleepRecommendation(Base):
    """Sleep recommendation model for caching recommendation data."""
    __tablename__ = "sleep_recommendations"
    
    id = Column(String(20), primary_key=True)
    title = Column(String(255))
    content = Column(Text)
    category = Column(String(50))
    priority = Column(String(20))
    source_name = Column(String(100))
    source = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)


class AnalyticsMetric(Base):
    """Analytics metrics model for storing aggregated data."""
    __tablename__ = "analytics_metrics"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    metric_name = Column(String(100))
    metric_value = Column(Float)
    metric_data = Column(JSON)  # Additional metric data
    date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow) 