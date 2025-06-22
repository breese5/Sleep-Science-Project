"""
Pydantic models for research papers.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class ResearchPaper(BaseModel):
    """Represents a single research paper."""
    pmid: str
    title: str
    abstract: str
    authors: List[str]
    journal: str
    publication_date: datetime
    url: str
    keywords: List[str] = []
    doi: Optional[str] = None
    citation_count: Optional[int] = None

    class Config:
        orm_mode = True 