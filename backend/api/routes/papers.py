"""
Papers endpoints for the Sleep Science Explainer Bot.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from backend.core.logging import get_logger
from backend.data.nih_client import NIHClient
from backend.data.sleep_recommendations import SleepRecommendationsClient

router = APIRouter()
logger = get_logger(__name__)


class ResearchPaper(BaseModel):
    """Research paper model."""
    id: str
    title: str
    authors: List[str]
    abstract: str
    journal: str
    publication_date: datetime
    doi: Optional[str] = None
    pmid: Optional[str] = None
    keywords: List[str] = []
    source: str = "pubmed"


class SleepRecommendation(BaseModel):
    """Sleep recommendation model."""
    id: str
    title: str
    content: str
    category: str
    priority: str
    source_name: str
    source: str


class PaperSearchRequest(BaseModel):
    """Paper search request model."""
    query: str = Field(..., description="Search query")
    max_results: int = Field(10, description="Maximum number of results")
    publication_date_from: Optional[datetime] = Field(None, description="Start date for publication filter")
    publication_date_to: Optional[datetime] = Field(None, description="End date for publication filter")


class PaperSearchResponse(BaseModel):
    """Paper search response model."""
    papers: List[ResearchPaper]
    recommendations: List[SleepRecommendation]
    total_count: int
    query: str
    search_timestamp: datetime


# Initialize clients
nih_client = NIHClient()
sleep_recommendations_client = SleepRecommendationsClient()


@router.get("/papers/search", response_model=PaperSearchResponse)
async def search_papers(
    query: str = Query(..., description="Search query for sleep science papers"),
    max_results: int = Query(10, ge=1, le=50, description="Maximum number of results"),
    source: str = Query("all", description="Data source (pubmed, recommendations, all)")
) -> PaperSearchResponse:
    """
    Search for sleep science research papers and recommendations.
    
    This endpoint searches through NIH PubMed and sleep recommendations
    from Bryan Johnson, Andrew Huberman, EightSleep, and CDC.
    """
    logger.info(
        "Paper search requested",
        query=query,
        max_results=max_results,
        source=source
    )
    
    try:
        papers = []
        recommendations = []
        
        if source.lower() == "pubmed":
            # Search PubMed only
            pubmed_results = await nih_client.search_papers(
                query=query,
                max_results=max_results
            )
            papers.extend(pubmed_results)
        elif source.lower() == "recommendations":
            # Search recommendations only
            rec_results = await sleep_recommendations_client.search_recommendations(
                query=query,
                max_results=max_results
            )
            recommendations.extend(rec_results)
        else:
            # Search both sources
            pubmed_results = await nih_client.search_papers(
                query=query,
                max_results=max_results // 2
            )
            rec_results = await sleep_recommendations_client.search_recommendations(
                query=query,
                max_results=max_results // 2
            )
            papers.extend(pubmed_results)
            recommendations.extend(rec_results)
        
        return PaperSearchResponse(
            papers=papers,
            recommendations=recommendations,
            total_count=len(papers) + len(recommendations),
            query=query,
            search_timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(
            "Error searching papers",
            error=str(e),
            query=query
        )
        raise HTTPException(
            status_code=500,
            detail="Failed to search papers. Please try again."
        )


@router.get("/papers/{paper_id}", response_model=ResearchPaper)
async def get_paper_details(paper_id: str) -> ResearchPaper:
    """
    Get detailed information about a specific research paper.
    
    Args:
        paper_id: Unique identifier for the paper
        
    Returns:
        Detailed paper information
    """
    logger.info("Paper details requested", paper_id=paper_id)
    
    try:
        # Try to get paper from PubMed
        if paper_id.startswith("PMID"):
            paper = await nih_client.get_paper_details(paper_id)
        else:
            raise HTTPException(
                status_code=404,
                detail="Paper not found"
            )
        
        if not paper:
            raise HTTPException(
                status_code=404,
                detail="Paper not found"
            )
        
        return paper
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Error getting paper details",
            error=str(e),
            paper_id=paper_id
        )
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve paper details"
        )


@router.get("/recommendations/{rec_id}", response_model=SleepRecommendation)
async def get_recommendation_details(rec_id: str) -> SleepRecommendation:
    """
    Get detailed information about a specific sleep recommendation.
    
    Args:
        rec_id: Unique identifier for the recommendation
        
    Returns:
        Detailed recommendation information
    """
    logger.info("Recommendation details requested", rec_id=rec_id)
    
    try:
        recommendation = await sleep_recommendations_client.get_recommendation_by_id(rec_id)
        
        if not recommendation:
            raise HTTPException(
                status_code=404,
                detail="Recommendation not found"
            )
        
        return SleepRecommendation(**recommendation)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Error getting recommendation details",
            error=str(e),
            rec_id=rec_id
        )
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve recommendation details"
        )


@router.get("/papers/recent", response_model=List[ResearchPaper])
async def get_recent_papers(
    days: int = Query(30, ge=1, le=365, description="Number of days to look back"),
    max_results: int = Query(20, ge=1, le=100, description="Maximum number of results")
) -> List[ResearchPaper]:
    """
    Get recent sleep science research papers.
    
    Args:
        days: Number of days to look back
        max_results: Maximum number of results to return
        
    Returns:
        List of recent research papers
    """
    logger.info(
        "Recent papers requested",
        days=days,
        max_results=max_results
    )
    
    try:
        # Get recent papers from PubMed
        recent_papers = await nih_client.get_recent_papers(
            days=days,
            max_results=max_results
        )
        
        return recent_papers
        
    except Exception as e:
        logger.error(
            "Error getting recent papers",
            error=str(e),
            days=days
        )
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve recent papers"
        )


@router.get("/recommendations", response_model=List[SleepRecommendation])
async def get_recommendations(
    category: Optional[str] = Query(None, description="Filter by category"),
    source: Optional[str] = Query(None, description="Filter by source"),
    max_results: int = Query(20, ge=1, le=100, description="Maximum number of results")
) -> List[SleepRecommendation]:
    """
    Get sleep recommendations.
    
    Args:
        category: Optional category filter
        source: Optional source filter
        max_results: Maximum number of results to return
        
    Returns:
        List of sleep recommendations
    """
    logger.info(
        "Recommendations requested",
        category=category,
        source=source,
        max_results=max_results
    )
    
    try:
        if category:
            recommendations = await sleep_recommendations_client.get_recommendations_by_category(
                category=category,
                source=source
            )
        else:
            all_recs = await sleep_recommendations_client.get_all_recommendations()
            recommendations = []
            for source_data in all_recs.values():
                if source and source_data["source"] != source:
                    continue
                for rec in source_data["recommendations"]:
                    recommendations.append({
                        **rec,
                        "source_name": source_data["name"],
                        "source": source_data["source"]
                    })
        
        return [SleepRecommendation(**rec) for rec in recommendations[:max_results]]
        
    except Exception as e:
        logger.error(
            "Error getting recommendations",
            error=str(e)
        )
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve recommendations"
        )


@router.get("/papers/topics")
async def get_paper_topics() -> Dict[str, List[str]]:
    """
    Get available topics for paper search.
    
    Returns:
        Dictionary of available topics and their search terms
    """
    logger.info("Paper topics requested")
    
    topics = {
        "sleep_cycles": [
            "circadian rhythm",
            "sleep wake cycle",
            "REM sleep",
            "NREM sleep"
        ],
        "sleep_disorders": [
            "insomnia",
            "sleep apnea",
            "narcolepsy",
            "restless leg syndrome"
        ],
        "sleep_hygiene": [
            "sleep hygiene",
            "sleep environment",
            "bedtime routine",
            "sleep habits"
        ],
        "sleep_research": [
            "sleep research",
            "sleep studies",
            "sleep science",
            "sleep medicine"
        ],
        "sleep_and_health": [
            "sleep and health",
            "sleep and disease",
            "sleep and mental health",
            "sleep and physical health"
        ]
    }
    
    return {"topics": topics}


@router.get("/recommendations/categories")
async def get_recommendation_categories() -> Dict[str, List[str]]:
    """
    Get available categories for sleep recommendations.
    
    Returns:
        Dictionary of available categories
    """
    logger.info("Recommendation categories requested")
    
    categories = [
        "sleep_schedule",
        "sleep_environment", 
        "sleep_hygiene",
        "sleep_monitoring",
        "circadian_rhythm",
        "sleep_physiology",
        "exercise",
        "sleep_stages",
        "sleep_duration",
        "diet"
    ]
    
    return {"categories": categories}


@router.post("/papers/summarize")
async def summarize_paper(
    paper_id: str,
    summary_length: str = Query("medium", description="Summary length (short, medium, long)")
) -> Dict[str, Any]:
    """
    Generate a summary of a research paper.
    
    Args:
        paper_id: Paper identifier
        summary_length: Desired summary length
        
    Returns:
        Paper summary and key insights
    """
    logger.info(
        "Paper summarization requested",
        paper_id=paper_id,
        summary_length=summary_length
    )
    
    try:
        # Get paper details
        paper = await get_paper_details(paper_id)
        
        # TODO: Implement AI summarization using Bedrock
        # For now, return a placeholder
        summary = {
            "paper_id": paper_id,
            "title": paper.title,
            "summary": f"This is a placeholder summary for {paper.title}. The actual summarization will be implemented using AWS Bedrock.",
            "key_findings": [
                "Key finding 1",
                "Key finding 2",
                "Key finding 3"
            ],
            "clinical_implications": "Clinical implications will be generated by AI",
            "summary_length": summary_length,
            "generated_at": datetime.utcnow()
        }
        
        return summary
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Error summarizing paper",
            error=str(e),
            paper_id=paper_id
        )
        raise HTTPException(
            status_code=500,
            detail="Failed to generate paper summary"
        ) 