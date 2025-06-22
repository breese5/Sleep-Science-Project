"""
Sleep recommendations data client for the Sleep Science Explainer Bot.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
import json

from backend.core.logging import LoggerMixin


class SleepRecommendationsClient(LoggerMixin):
    """
    Client for sleep recommendations from various sources.
    
    This client provides recommendations from:
    - Bryan Johnson (Blueprint protocol)
    - Andrew Huberman (Huberman Lab)
    - EightSleep (sleep optimization)
    - CDC (clinical guidelines)
    """
    
    def __init__(self):
        """Initialize the sleep recommendations client."""
        self.logger.info("Initializing SleepRecommendationsClient")
        
        # Load recommendations data
        self.recommendations = self._load_recommendations()
        
        self.logger.info("SleepRecommendationsClient initialized successfully")
    
    def _load_recommendations(self) -> Dict[str, Any]:
        """Load sleep recommendations from various sources."""
        return {
            "bryan_johnson": {
                "name": "Bryan Johnson - Blueprint Protocol",
                "source": "bryan_johnson",
                "recommendations": [
                    {
                        "id": "bj_001",
                        "title": "Sleep Schedule Optimization",
                        "content": "Maintain a consistent sleep schedule with 8-9 hours of sleep per night. Go to bed between 9-10 PM and wake up between 5-6 AM to align with natural circadian rhythms.",
                        "category": "sleep_schedule",
                        "priority": "high"
                    },
                    {
                        "id": "bj_002",
                        "title": "Sleep Environment",
                        "content": "Keep bedroom temperature between 65-67°F (18-19°C), use blackout curtains, and eliminate all light sources. Consider using a sleep mask and earplugs for optimal conditions.",
                        "category": "sleep_environment",
                        "priority": "high"
                    },
                    {
                        "id": "bj_003",
                        "title": "Pre-Sleep Routine",
                        "content": "Avoid screens 2-3 hours before bed, engage in relaxing activities like reading or meditation, and avoid caffeine after 2 PM.",
                        "category": "sleep_hygiene",
                        "priority": "medium"
                    },
                    {
                        "id": "bj_004",
                        "title": "Sleep Tracking",
                        "content": "Use sleep tracking devices to monitor sleep quality, duration, and patterns. Aim for consistent deep sleep and REM cycles.",
                        "category": "sleep_monitoring",
                        "priority": "medium"
                    }
                ]
            },
            "andrew_huberman": {
                "name": "Andrew Huberman - Huberman Lab",
                "source": "andrew_huberman",
                "recommendations": [
                    {
                        "id": "ah_001",
                        "title": "Morning Light Exposure",
                        "content": "Get 10-30 minutes of bright light exposure within 30-60 minutes of waking up. This helps set your circadian rhythm and improves sleep quality later.",
                        "category": "circadian_rhythm",
                        "priority": "high"
                    },
                    {
                        "id": "ah_002",
                        "title": "Evening Light Management",
                        "content": "Avoid bright light exposure 2-3 hours before bed. Use dim, warm lighting and consider blue light blocking glasses if using screens.",
                        "category": "circadian_rhythm",
                        "priority": "high"
                    },
                    {
                        "id": "ah_003",
                        "title": "Temperature Regulation",
                        "content": "Your body temperature naturally drops 2-3 degrees before sleep. Take a hot bath or shower 1-2 hours before bed to facilitate this drop.",
                        "category": "sleep_physiology",
                        "priority": "medium"
                    },
                    {
                        "id": "ah_004",
                        "title": "Caffeine Timing",
                        "content": "Avoid caffeine 8-10 hours before bed. Caffeine has a half-life of 5-6 hours, so it can significantly impact sleep quality.",
                        "category": "sleep_hygiene",
                        "priority": "high"
                    },
                    {
                        "id": "ah_005",
                        "title": "Exercise Timing",
                        "content": "Exercise in the morning or early afternoon. Avoid intense exercise within 3-4 hours of bedtime as it can raise body temperature and delay sleep.",
                        "category": "exercise",
                        "priority": "medium"
                    }
                ]
            },
            "eightsleep": {
                "name": "EightSleep - Sleep Optimization",
                "source": "eightsleep",
                "recommendations": [
                    {
                        "id": "es_001",
                        "title": "Temperature Control",
                        "content": "Use temperature regulation technology to maintain optimal sleep temperature. Cool your body to 65-67°F during sleep for better quality rest.",
                        "category": "sleep_environment",
                        "priority": "high"
                    },
                    {
                        "id": "es_002",
                        "title": "Sleep Stages Optimization",
                        "content": "Focus on getting adequate deep sleep (20-25% of total sleep) and REM sleep (20-25% of total sleep). These stages are crucial for recovery and cognitive function.",
                        "category": "sleep_stages",
                        "priority": "high"
                    },
                    {
                        "id": "es_003",
                        "title": "Heart Rate Variability",
                        "content": "Monitor heart rate variability (HRV) as it's a key indicator of recovery and sleep quality. Higher HRV generally indicates better sleep and recovery.",
                        "category": "sleep_monitoring",
                        "priority": "medium"
                    },
                    {
                        "id": "es_004",
                        "title": "Sleep Consistency",
                        "content": "Maintain consistent sleep and wake times, even on weekends. This helps regulate your circadian rhythm and improves overall sleep quality.",
                        "category": "sleep_schedule",
                        "priority": "high"
                    }
                ]
            },
            "cdc": {
                "name": "CDC - Sleep Guidelines",
                "source": "cdc",
                "recommendations": [
                    {
                        "id": "cdc_001",
                        "title": "Sleep Duration Guidelines",
                        "content": "Adults should get 7 or more hours of sleep per night. Teenagers need 8-10 hours, and school-age children need 9-12 hours.",
                        "category": "sleep_duration",
                        "priority": "high"
                    },
                    {
                        "id": "cdc_002",
                        "title": "Sleep Hygiene Practices",
                        "content": "Go to bed and wake up at the same time every day, including weekends. Make sure your bedroom is quiet, dark, and at a comfortable temperature.",
                        "category": "sleep_hygiene",
                        "priority": "high"
                    },
                    {
                        "id": "cdc_003",
                        "title": "Electronic Device Management",
                        "content": "Remove electronic devices from the bedroom, including TVs, computers, and smartphones. The light from these devices can interfere with sleep.",
                        "category": "sleep_environment",
                        "priority": "medium"
                    },
                    {
                        "id": "cdc_004",
                        "title": "Physical Activity",
                        "content": "Be physically active during the day, which can help you fall asleep more easily at night. However, avoid vigorous exercise close to bedtime.",
                        "category": "exercise",
                        "priority": "medium"
                    },
                    {
                        "id": "cdc_005",
                        "title": "Diet and Sleep",
                        "content": "Avoid large meals, caffeine, and alcohol before bedtime. These can interfere with your ability to fall asleep and stay asleep.",
                        "category": "diet",
                        "priority": "medium"
                    }
                ]
            }
        }
    
    async def search_recommendations(
        self,
        query: str,
        max_results: int = 10,
        sources: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for sleep recommendations.
        
        Args:
            query: Search query
            max_results: Maximum number of results
            sources: List of sources to search (bryan_johnson, andrew_huberman, eightsleep, cdc)
            
        Returns:
            List of matching recommendations
        """
        self.logger.info(
            "Searching sleep recommendations",
            query=query,
            max_results=max_results,
            sources=sources
        )
        
        results = []
        query_lower = query.lower()
        
        # Determine which sources to search
        sources_to_search = sources or list(self.recommendations.keys())
        
        for source in sources_to_search:
            if source not in self.recommendations:
                continue
                
            source_data = self.recommendations[source]
            
            for rec in source_data["recommendations"]:
                # Simple keyword matching
                if (query_lower in rec["title"].lower() or 
                    query_lower in rec["content"].lower() or
                    query_lower in rec["category"].lower()):
                    
                    results.append({
                        **rec,
                        "source_name": source_data["name"],
                        "source": source_data["source"]
                    })
                    
                    if len(results) >= max_results:
                        break
        
        return results[:max_results]
    
    async def get_recommendations_by_category(
        self,
        category: str,
        source: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get recommendations by category.
        
        Args:
            category: Category to filter by
            source: Optional source filter
            
        Returns:
            List of recommendations in the category
        """
        self.logger.info("Getting recommendations by category", category=category, source=source)
        
        results = []
        sources_to_search = [source] if source else list(self.recommendations.keys())
        
        for source_name in sources_to_search:
            if source_name not in self.recommendations:
                continue
                
            source_data = self.recommendations[source_name]
            
            for rec in source_data["recommendations"]:
                if rec["category"] == category:
                    results.append({
                        **rec,
                        "source_name": source_data["name"],
                        "source": source_data["source"]
                    })
        
        return results
    
    async def get_all_recommendations(self) -> Dict[str, Any]:
        """
        Get all recommendations organized by source.
        
        Returns:
            Dictionary of all recommendations
        """
        return self.recommendations
    
    async def get_recommendation_by_id(self, rec_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific recommendation by ID.
        
        Args:
            rec_id: Recommendation ID
            
        Returns:
            Recommendation data or None
        """
        for source_data in self.recommendations.values():
            for rec in source_data["recommendations"]:
                if rec["id"] == rec_id:
                    return {
                        **rec,
                        "source_name": source_data["name"],
                        "source": source_data["source"]
                    }
        
        return None 