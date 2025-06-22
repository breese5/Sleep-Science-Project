"""
Configuration settings for the Sleep Science Explainer Bot.
"""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings."""
    
    # AWS Configuration
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_default_region: str = "us-east-1"
    aws_bedrock_region: str = "us-east-1"
    
    # Application Configuration
    app_name: str = "SleepScienceBot"
    app_version: str = "1.0.0"
    debug: bool = True
    environment: str = "development"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_prefix: str = "/api/v1"
    
    # Database Configuration
    database_url: str = "postgresql://username:password@localhost:5432/sleep_science_bot"
    database_pool_size: int = 10
    database_max_overflow: int = 20
    
    # Redis Configuration
    redis_url: str = "redis://localhost:6379/0"
    redis_password: Optional[str] = None
    
    # NIH PubMed API Configuration
    nih_api_key: Optional[str] = None
    nih_base_url: str = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    
    # CDC API Configuration
    cdc_base_url: str = "https://data.cdc.gov/resource"
    
    # Security Configuration
    secret_key: str = "your_secret_key_here_make_it_long_and_random"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Bedrock Model Configuration
    bedrock_model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    bedrock_max_tokens: int = 4096
    bedrock_temperature: float = 0.7
    
    # Monitoring Configuration
    log_level: str = "INFO"
    enable_metrics: bool = True
    metrics_port: int = 9090
    
    # S3 Configuration
    s3_bucket_name: str = "sleep-science-bot-data"
    s3_region: str = "us-east-1"
    
    # Frontend Configuration
    frontend_url: str = "http://localhost:3000"
    cors_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Analytics Configuration
    analytics_enabled: bool = True
    analytics_retention_days: int = 90
    
    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600
    
    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v):
        """Validate secret key length."""
        if len(v) < 32:
            raise ValueError("Secret key must be at least 32 characters long")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings() 