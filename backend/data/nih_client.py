"""
NIH PubMed API client for the Sleep Science Explainer Bot.
"""

import asyncio
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import httpx
import xml.etree.ElementTree as ET

from backend.core.logging import LoggerMixin
from backend.core.config import settings
from backend.models.papers import ResearchPaper


class NIHClient(LoggerMixin):
    """
    Client for interacting with NIH PubMed API.
    
    This client handles:
    - Searching for sleep science papers
    - Fetching paper details
    - Getting recent publications
    - Parsing PubMed XML responses
    """
    
    def __init__(self):
        """Initialize the NIH client."""
        self.logger.info("Initializing NIHClient")
        
        self.base_url = settings.nih_base_url
        self.api_key = settings.nih_api_key
        self.timeout = 30.0
        
        self.logger.info("NIHClient initialized successfully")
    
    async def search_papers(
        self,
        query: str,
        max_results: int = 10,
        publication_date_from: Optional[datetime] = None,
        publication_date_to: Optional[datetime] = None
    ) -> List[ResearchPaper]:
        """
        Search for sleep science papers in PubMed.
        
        Args:
            query: Search query
            max_results: Maximum number of results
            publication_date_from: Start date for publication filter
            publication_date_to: End date for publication filter
            
        Returns:
            List of research papers
        """
        self.logger.info(
            "Searching PubMed papers",
            query=query,
            max_results=max_results
        )
        
        try:
            # Build search parameters
            params = {
                "db": "pubmed",
                "term": query,
                "retmax": max_results,
                "retmode": "xml",
                "sort": "date"
            }
            
            # Add date filters if provided
            if publication_date_from:
                params["mindate"] = publication_date_from.strftime("%Y/%m/%d")
            if publication_date_to:
                params["maxdate"] = publication_date_to.strftime("%Y/%m/%d")
            
            # Add API key if available
            if self.api_key:
                params["api_key"] = self.api_key
            
            # Make search request
            search_url = f"{self.base_url}/esearch.fcgi"
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(search_url, params=params)
                response.raise_for_status()
                
                # Parse search results
                search_data = ET.fromstring(response.text)
                id_list = search_data.find(".//IdList")
                
                if id_list is None:
                    self.logger.warning("No search results found")
                    return []
                
                # Get paper IDs
                paper_ids = [id_elem.text for id_elem in id_list.findall("Id")]
                
                # Fetch details for each paper
                papers = []
                for paper_id in paper_ids[:max_results]:
                    try:
                        paper = await self._fetch_paper_details(paper_id)
                        if paper:
                            papers.append(paper)
                    except Exception as e:
                        self.logger.warning(
                            f"Failed to fetch paper {paper_id}: {e}"
                        )
                
                return papers
                
        except Exception as e:
            self.logger.error(
                "Error searching PubMed papers",
                error=str(e),
                query=query
            )
            raise
    
    async def get_recent_papers(
        self,
        days: int = 30,
        max_results: int = 20
    ) -> List[ResearchPaper]:
        """
        Get recent sleep science papers.
        
        Args:
            days: Number of days to look back
            max_results: Maximum number of results
            
        Returns:
            List of recent research papers
        """
        self.logger.info(
            "Getting recent PubMed papers",
            days=days,
            max_results=max_results
        )
        
        # Calculate date range
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Search for recent sleep-related papers
        query = "sleep[Title/Abstract] AND (2023[Date - Publication] OR 2024[Date - Publication])"
        
        return await self.search_papers(
            query=query,
            max_results=max_results,
            publication_date_from=start_date,
            publication_date_to=end_date
        )
    
    async def get_paper_details(self, pmid: str) -> Optional[ResearchPaper]:
        """
        Get detailed information about a specific paper.
        
        Args:
            pmid: PubMed ID
            
        Returns:
            Paper details or None if not found
        """
        self.logger.info("Fetching paper details", pmid=pmid)
        
        try:
            return await self._fetch_paper_details(pmid)
        except Exception as e:
            self.logger.error(
                "Error fetching paper details",
                error=str(e),
                pmid=pmid
            )
            return None
    
    async def _fetch_paper_details(self, pmid: str) -> Optional[ResearchPaper]:
        """
        Fetch paper details from PubMed.
        
        Args:
            pmid: PubMed ID
            
        Returns:
            ResearchPaper object or None
        """
        try:
            # Build request parameters
            params = {
                "db": "pubmed",
                "id": pmid,
                "retmode": "xml"
            }
            
            if self.api_key:
                params["api_key"] = self.api_key
            
            # Make request
            fetch_url = f"{self.base_url}/efetch.fcgi"
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(fetch_url, params=params)
                response.raise_for_status()
                
                # Parse XML response
                return self._parse_pubmed_xml(response.text, pmid)
                
        except Exception as e:
            self.logger.error(
                "Error fetching paper details",
                error=str(e),
                pmid=pmid
            )
            return None
    
    def _parse_pubmed_xml(self, xml_content: str, pmid: str) -> Optional[ResearchPaper]:
        """
        Parse PubMed XML response.
        
        Args:
            xml_content: XML content from PubMed
            pmid: PubMed ID
            
        Returns:
            ResearchPaper object or None
        """
        try:
            root = ET.fromstring(xml_content)
            article = root.find(".//PubmedArticle")
            
            if article is None:
                return None
            
            # Extract article information
            medline_citation = article.find(".//MedlineCitation")
            if medline_citation is None:
                return None
            
            # Get title
            title_elem = medline_citation.find(".//ArticleTitle")
            title = title_elem.text if title_elem is not None else "No title available"
            
            # Get authors
            authors = []
            author_list = medline_citation.find(".//AuthorList")
            if author_list is not None:
                for author in author_list.findall("Author"):
                    last_name = author.find("LastName")
                    fore_name = author.find("ForeName")
                    if last_name is not None and fore_name is not None:
                        authors.append(f"{fore_name.text} {last_name.text}")
                    elif last_name is not None:
                        authors.append(last_name.text)
            
            # Get abstract
            abstract_elem = medline_citation.find(".//Abstract/AbstractText")
            abstract = abstract_elem.text if abstract_elem is not None else "No abstract available"
            
            # Get journal
            journal_elem = medline_citation.find(".//Journal/Title")
            journal = journal_elem.text if journal_elem is not None else "Unknown journal"
            
            # Get publication date
            pub_date = self._extract_publication_date(medline_citation)
            
            # Get DOI
            doi = None
            article_id_list = article.find(".//ArticleIdList")
            if article_id_list is not None:
                for article_id in article_id_list.findall("ArticleId"):
                    if article_id.get("IdType") == "doi":
                        doi = article_id.text
                        break
            
            # Get keywords
            keywords = []
            keyword_list = medline_citation.find(".//KeywordList")
            if keyword_list is not None:
                for keyword in keyword_list.findall("Keyword"):
                    if keyword.text:
                        keywords.append(keyword.text)
            
            return ResearchPaper(
                id=f"PMID{pmid}",
                title=title,
                authors=authors,
                abstract=abstract,
                journal=journal,
                publication_date=pub_date,
                doi=doi,
                pmid=pmid,
                keywords=keywords,
                source="pubmed"
            )
            
        except Exception as e:
            self.logger.error(
                "Error parsing PubMed XML",
                error=str(e),
                pmid=pmid
            )
            return None
    
    def _extract_publication_date(self, medline_citation) -> datetime:
        """
        Extract publication date from MedlineCitation.
        
        Args:
            medline_citation: MedlineCitation element
            
        Returns:
            Publication date
        """
        try:
            # Try to get publication date
            pub_date_elem = medline_citation.find(".//PubDate")
            if pub_date_elem is not None:
                year_elem = pub_date_elem.find("Year")
                month_elem = pub_date_elem.find("Month")
                day_elem = pub_date_elem.find("Day")
                
                year = int(year_elem.text) if year_elem is not None else datetime.utcnow().year
                month = int(month_elem.text) if month_elem is not None else 1
                day = int(day_elem.text) if day_elem is not None else 1
                
                return datetime(year, month, day)
            
            # Fallback to current date
            return datetime.utcnow()
            
        except Exception as e:
            self.logger.warning(f"Error extracting publication date: {e}")
            return datetime.utcnow() 