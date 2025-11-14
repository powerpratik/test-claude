"""
Query engine for retrieving papers from the knowledge base.
"""

import logging
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from ..knowledge_base.storage import KnowledgeBase
from ..knowledge_base.models import Paper, Theme, KeyFinding

logger = logging.getLogger(__name__)


@dataclass
class QueryParams:
    """Parameters for querying papers."""
    themes: Optional[List[str]] = None
    keywords: Optional[str] = None
    year_min: Optional[int] = None
    year_max: Optional[int] = None
    authors: Optional[str] = None
    limit: int = 100
    include_sections: bool = False
    include_findings: bool = False
    include_themes: bool = True
    summary_level: str = 'brief'  # 'brief' or 'detailed'


class QueryEngine:
    """Engine for querying and retrieving papers."""

    def __init__(self, knowledge_base: KnowledgeBase, config: Optional[Dict] = None):
        """
        Initialize query engine.

        Args:
            knowledge_base: KnowledgeBase instance
            config: Optional configuration
        """
        self.kb = knowledge_base
        self.config = config or {}

    def query(self, params: QueryParams) -> List[Paper]:
        """
        Query papers based on parameters.

        Args:
            params: Query parameters

        Returns:
            List of matching papers
        """
        papers = []

        # Query by themes
        if params.themes:
            papers = self._query_by_themes(params.themes, params.limit)

        # Query by keywords
        elif params.keywords:
            papers = self.kb.search_papers(params.keywords, params.limit)

        # Get all papers
        else:
            papers = self.kb.get_all_papers(params.limit)

        # Apply filters
        if params.year_min or params.year_max:
            papers = self._filter_by_year(papers, params.year_min, params.year_max)

        if params.authors:
            papers = self._filter_by_authors(papers, params.authors)

        # Load additional data
        for paper in papers:
            if params.include_themes:
                paper.themes = self.kb.get_paper_themes(paper.id)

            if params.include_sections:
                paper.sections = self.kb.get_paper_sections(paper.id)

            if params.include_findings:
                paper.findings = self.kb.get_paper_findings(paper.id)

        return papers

    def get_papers_by_theme(self, theme_name: str, limit: Optional[int] = None) -> List[Paper]:
        """
        Get all papers for a theme.

        Args:
            theme_name: Theme name
            limit: Optional limit

        Returns:
            List of papers
        """
        theme = self.kb.get_theme_by_name(theme_name)
        if not theme:
            logger.warning(f"Theme not found: {theme_name}")
            return []

        papers = self.kb.get_papers_by_theme(theme.id)

        if limit:
            papers = papers[:limit]

        return papers

    def get_papers_by_themes(self, theme_names: List[str], limit: Optional[int] = None) -> List[Paper]:
        """
        Get papers matching any of the themes.

        Args:
            theme_names: List of theme names
            limit: Optional limit

        Returns:
            List of papers
        """
        all_papers = []
        seen_ids = set()

        for theme_name in theme_names:
            papers = self.get_papers_by_theme(theme_name)

            for paper in papers:
                if paper.id not in seen_ids:
                    all_papers.append(paper)
                    seen_ids.add(paper.id)

        # Sort by year (most recent first)
        all_papers.sort(key=lambda p: (p.year or 0, p.title), reverse=True)

        if limit:
            all_papers = all_papers[:limit]

        return all_papers

    def get_papers_by_year_range(self, year_min: int, year_max: int) -> List[Paper]:
        """
        Get papers within a year range.

        Args:
            year_min: Minimum year (inclusive)
            year_max: Maximum year (inclusive)

        Returns:
            List of papers
        """
        all_papers = self.kb.get_all_papers()
        filtered = self._filter_by_year(all_papers, year_min, year_max)
        return filtered

    def search_by_keyword(self, keyword: str, limit: int = 50) -> List[Paper]:
        """
        Full-text search for papers.

        Args:
            keyword: Search keyword
            limit: Maximum results

        Returns:
            List of matching papers
        """
        return self.kb.search_papers(keyword, limit)

    def get_paper_context(self, paper_id: int, include_full_text: bool = False) -> Dict[str, Any]:
        """
        Get comprehensive context for a paper.

        Args:
            paper_id: Paper ID
            include_full_text: Whether to include full section content

        Returns:
            Dictionary with paper context
        """
        paper = self.kb.get_paper(paper_id)
        if not paper:
            return {}

        context = {
            'paper': paper,
            'themes': self.kb.get_paper_themes(paper_id),
            'findings': self.kb.get_paper_findings(paper_id),
            'sections': self.kb.get_paper_sections(paper_id),
        }

        # If not including full text, use summaries only
        if not include_full_text:
            for section in context['sections']:
                section.content = ""  # Clear full content

        return context

    def get_theme_overview(self, theme_name: str) -> Dict[str, Any]:
        """
        Get overview of a theme.

        Args:
            theme_name: Theme name

        Returns:
            Dictionary with theme overview
        """
        theme = self.kb.get_theme_by_name(theme_name)
        if not theme:
            return {}

        papers = self.get_papers_by_theme(theme_name)

        # Aggregate statistics
        years = [p.year for p in papers if p.year]
        year_range = (min(years), max(years)) if years else (None, None)

        # Get all findings for theme
        all_findings = []
        for paper in papers[:20]:  # Limit to recent 20 papers
            findings = self.kb.get_paper_findings(paper.id)
            all_findings.extend(findings)

        # Group findings by category
        findings_by_category = {}
        for finding in all_findings:
            category = finding.category
            if category not in findings_by_category:
                findings_by_category[category] = []
            findings_by_category[category].append(finding)

        return {
            'theme': theme,
            'paper_count': len(papers),
            'year_range': year_range,
            'papers': papers,
            'findings_by_category': findings_by_category,
        }

    def get_papers_for_review(self, theme_name: str, min_papers: int = 20) -> Dict[str, Any]:
        """
        Get papers and context for generating a literature review.

        Args:
            theme_name: Theme name
            min_papers: Minimum papers required

        Returns:
            Dictionary with review context
        """
        papers = self.get_papers_by_theme(theme_name)

        if len(papers) < min_papers:
            logger.warning(f"Only {len(papers)} papers found for theme '{theme_name}', minimum is {min_papers}")

        # Load additional context for each paper
        for paper in papers:
            paper.themes = self.kb.get_paper_themes(paper.id)
            paper.findings = self.kb.get_paper_findings(paper.id)
            # Note: Don't load full sections to save context

        # Organize by sub-themes if applicable
        sub_themes = self._identify_sub_themes(papers)

        # Get year distribution
        year_distribution = self._get_year_distribution(papers)

        return {
            'theme': theme_name,
            'papers': papers,
            'paper_count': len(papers),
            'sub_themes': sub_themes,
            'year_distribution': year_distribution,
        }

    def _query_by_themes(self, theme_names: List[str], limit: int) -> List[Paper]:
        """Query papers by multiple themes."""
        return self.get_papers_by_themes(theme_names, limit)

    def _filter_by_year(self, papers: List[Paper], year_min: Optional[int], year_max: Optional[int]) -> List[Paper]:
        """Filter papers by year range."""
        filtered = []

        for paper in papers:
            if not paper.year:
                continue

            if year_min and paper.year < year_min:
                continue

            if year_max and paper.year > year_max:
                continue

            filtered.append(paper)

        return filtered

    def _filter_by_authors(self, papers: List[Paper], author_query: str) -> List[Paper]:
        """Filter papers by author name."""
        filtered = []
        author_lower = author_query.lower()

        for paper in papers:
            if paper.authors and author_lower in paper.authors.lower():
                filtered.append(paper)

        return filtered

    def _identify_sub_themes(self, papers: List[Paper]) -> Dict[str, List[Paper]]:
        """Identify sub-themes within a set of papers."""
        sub_themes = {}

        for paper in papers:
            # Group by themes
            themes = self.kb.get_paper_themes(paper.id)
            for theme in themes:
                if theme.name not in sub_themes:
                    sub_themes[theme.name] = []
                sub_themes[theme.name].append(paper)

        return sub_themes

    def _get_year_distribution(self, papers: List[Paper]) -> Dict[int, int]:
        """Get distribution of papers by year."""
        distribution = {}

        for paper in papers:
            if paper.year:
                distribution[paper.year] = distribution.get(paper.year, 0) + 1

        return dict(sorted(distribution.items()))

    def get_summary_context(self, papers: List[Paper], level: str = 'brief') -> List[Dict[str, str]]:
        """
        Get summary context for papers.

        Args:
            papers: List of papers
            level: 'brief' or 'detailed'

        Returns:
            List of dictionaries with paper summaries
        """
        summaries = []

        for paper in papers:
            summary_text = paper.brief_summary if level == 'brief' else paper.detailed_summary

            summaries.append({
                'id': paper.id,
                'title': paper.title,
                'authors': paper.authors,
                'year': paper.year,
                'summary': summary_text,
            })

        return summaries

    def estimate_context_usage(self, papers: List[Paper], level: str = 'brief') -> int:
        """
        Estimate token usage for papers.

        Args:
            papers: List of papers
            level: Summary level

        Returns:
            Estimated token count
        """
        total_tokens = 0

        for paper in papers:
            summary = paper.brief_summary if level == 'brief' else paper.detailed_summary
            # Rough estimate: 1 token ≈ 0.75 words
            words = len(summary.split())
            tokens = int(words / 0.75)
            total_tokens += tokens

        return total_tokens
