"""
Main review generator for creating literature reviews.
"""

import logging
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

try:
    from .templates import ReviewTemplates, CitationManager, TableFormatter
    from .latex_formatter import LaTeXFormatter, OverleafProject
    from ..knowledge_base.storage import KnowledgeBase
    from ..knowledge_base.models import Paper, Theme, FindingCategory
    from ..retrieval.query_engine import QueryEngine, QueryParams
except ImportError:
    from generation.templates import ReviewTemplates, CitationManager, TableFormatter
    from generation.latex_formatter import LaTeXFormatter, OverleafProject
    from knowledge_base.storage import KnowledgeBase
    from knowledge_base.models import Paper, Theme, FindingCategory
    from retrieval.query_engine import QueryEngine, QueryParams

logger = logging.getLogger(__name__)


class ReviewGenerator:
    """Generate comprehensive literature reviews."""

    def __init__(self, knowledge_base: KnowledgeBase, config: Optional[Dict] = None):
        """
        Initialize review generator.

        Args:
            knowledge_base: KnowledgeBase instance
            config: Optional configuration
        """
        self.kb = knowledge_base
        self.config = config or {}
        self.query_engine = QueryEngine(knowledge_base, config)
        self.citation_manager = CitationManager()
        self.templates = ReviewTemplates()
        self.table_formatter = TableFormatter()

    def generate_review(
        self,
        theme: str,
        sections: Optional[List[str]] = None,
        output_format: str = "markdown",
        min_papers: int = 20,
        author: str = "Literature Review Generator"
    ) -> str:
        """
        Generate a complete literature review.

        Args:
            theme: Theme/topic for the review
            sections: Sections to generate (None = all)
            output_format: Output format (currently only markdown)
            min_papers: Minimum number of papers required

        Returns:
            Generated review text
        """
        logger.info(f"Generating literature review for theme: {theme}")

        # Get papers for theme
        review_data = self.query_engine.get_papers_for_review(theme, min_papers)
        papers = review_data['papers']

        if len(papers) < min_papers:
            raise ValueError(
                f"Insufficient papers for review. Found {len(papers)}, need at least {min_papers}"
            )

        # Determine sections to generate
        if sections is None:
            sections = ['abstract', 'introduction', 'background', 'taxonomy', 'analysis', 'discussion', 'conclusion']

        # Generate review content
        review_parts = []

        # Title
        review_parts.append(f"# Literature Review: {theme}\n")
        review_parts.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d')}*\n")
        review_parts.append(f"*Based on {len(papers)} papers*\n\n")

        # Generate each section
        if 'abstract' in sections:
            abstract = self._generate_abstract(theme, papers, review_data)
            review_parts.append(abstract)
            review_parts.append("\n\n")

        if 'introduction' in sections:
            introduction = self._generate_introduction(theme, papers, review_data)
            review_parts.append(introduction)
            review_parts.append("\n\n")

        if 'background' in sections:
            background = self._generate_background(theme, papers)
            review_parts.append(background)
            review_parts.append("\n\n")

        if 'taxonomy' in sections:
            taxonomy = self._generate_taxonomy(theme, papers, review_data)
            review_parts.append(taxonomy)
            review_parts.append("\n\n")

        if 'analysis' in sections:
            analysis = self._generate_analysis(theme, papers, review_data)
            review_parts.append(analysis)
            review_parts.append("\n\n")

        if 'discussion' in sections:
            discussion = self._generate_discussion(theme, papers, review_data)
            review_parts.append(discussion)
            review_parts.append("\n\n")

        if 'conclusion' in sections:
            conclusion = self._generate_conclusion(theme, papers)
            review_parts.append(conclusion)
            review_parts.append("\n\n")

        # Add references
        references = self.citation_manager.generate_references_section()
        review_parts.append(references)

        review_text = "".join(review_parts)

        logger.info(f"Generated review with {self.citation_manager.get_citation_count()} citations")

        # Convert to LaTeX if requested
        if output_format.lower() == "latex":
            review_text = self._convert_to_latex(theme, review_parts, author)

        return review_text

    def _generate_abstract(self, theme: str, papers: List[Paper], review_data: Dict) -> str:
        """Generate abstract section."""
        year_dist = review_data.get('year_distribution', {})
        years = list(year_dist.keys())
        year_range = (min(years), max(years)) if years else (None, None)

        # Start with template
        abstract = self.templates.format_abstract(theme, len(papers), year_range)

        # Generate summary of main themes
        sub_themes = review_data.get('sub_themes', {})
        if sub_themes:
            theme_summary = "The review organizes the literature into the following main themes: " + \
                          ", ".join(sub_themes.keys()) + "."
            abstract = abstract.replace("[SUMMARY OF MAIN THEMES AND TRENDS]", theme_summary)

        # Summarize key findings
        all_contributions = []
        for paper in papers[:10]:  # Sample first 10 papers
            findings = [f for f in paper.findings if f.category == FindingCategory.CONTRIBUTION.value]
            all_contributions.extend(findings[:2])

        if all_contributions:
            findings_summary = "Key contributions include advances in " + theme.lower() + " methodologies, " + \
                             "novel applications, and significant performance improvements."
            abstract = abstract.replace("[KEY FINDINGS AND CONTRIBUTIONS]", findings_summary)

        # Identify gaps
        gaps_summary = f"We identify several open challenges and promising future research directions in {theme.lower()}."
        abstract = abstract.replace("[IDENTIFICATION OF GAPS AND FUTURE DIRECTIONS]", gaps_summary)

        return abstract

    def _generate_introduction(self, theme: str, papers: List[Paper], review_data: Dict) -> str:
        """Generate introduction section."""
        intro = self.templates.format_introduction(theme)

        # Add motivation
        motivation = f"{theme} has become increasingly important in recent years, " + \
                    f"with {len(papers)} significant papers published between " + \
                    f"{min(p.year for p in papers if p.year)} and {max(p.year for p in papers if p.year)}. " + \
                    f"This rapid growth reflects the field's importance and the need for a comprehensive survey."

        intro = intro.replace(f"[EXPLAIN THE IMPORTANCE AND RELEVANCE OF {theme.upper()}]", motivation)

        # Add survey methodology
        methodology = f"We reviewed {len(papers)} papers published in top-tier venues. " + \
                     f"Papers were selected based on their relevance to {theme}, citation count, and contribution significance."

        intro = intro.replace("[DESCRIBE PAPER SELECTION CRITERIA]", methodology)

        return intro

    def _generate_background(self, theme: str, papers: List[Paper]) -> str:
        """Generate background section."""
        background = self.templates.format_background()

        # Find earliest papers for historical context
        sorted_papers = sorted([p for p in papers if p.year], key=lambda x: x.year)

        if sorted_papers:
            early_papers = sorted_papers[:5]
            historical = "The field of " + theme.lower() + " has evolved significantly. "
            historical += "Seminal early works include:\n\n"

            for paper in early_papers:
                cite_num = self.citation_manager.add_citation(paper)
                historical += f"- {paper.title} {self.citation_manager.format_citation(cite_num)}\n"

            background = background.replace("[TRACE THE EVOLUTION OF THE FIELD]", historical)

        return background

    def _generate_taxonomy(self, theme: str, papers: List[Paper], review_data: Dict) -> str:
        """Generate taxonomy section."""
        taxonomy = self.templates.format_taxonomy()

        # Use sub-themes as categories
        sub_themes = review_data.get('sub_themes', {})

        if sub_themes:
            categories_text = []

            for i, (sub_theme, theme_papers) in enumerate(sub_themes.items(), 1):
                category_text = f"\n### 3.2.{i} {sub_theme}\n\n"
                category_text += f"This category includes {len(theme_papers)} papers focusing on {sub_theme.lower()}.\n\n"

                # List key characteristics
                category_text += "**Key Characteristics:**\n"
                category_text += f"- Focus on {sub_theme.lower()} approaches\n"
                category_text += f"- {len(theme_papers)} papers ({len(theme_papers)/len(papers)*100:.1f}% of surveyed work)\n"

                # List a few example papers
                category_text += "\n**Representative Papers:**\n"
                for paper in theme_papers[:3]:
                    cite_num = self.citation_manager.add_citation(paper)
                    category_text += f"- {paper.title} {self.citation_manager.format_citation(cite_num)}\n"

                categories_text.append(category_text)

            # Replace placeholders
            all_categories = "\n".join(categories_text)
            taxonomy = taxonomy.replace(
                "### 3.2.1 Category 1: [NAME]\n\n[BRIEF DESCRIPTION]\n[KEY CHARACTERISTICS]\n\n"
                "### 3.2.2 Category 2: [NAME]\n\n[BRIEF DESCRIPTION]\n[KEY CHARACTERISTICS]\n\n"
                "[... ADDITIONAL CATEGORIES ...]",
                all_categories
            )

        return taxonomy

    def _generate_analysis(self, theme: str, papers: List[Paper], review_data: Dict) -> str:
        """Generate detailed analysis section."""
        analysis_parts = ["# 4. Detailed Analysis\n\n"]

        sub_themes = review_data.get('sub_themes', {})

        if sub_themes:
            for i, (sub_theme, theme_papers) in enumerate(sub_themes.items(), 1):
                section = self._generate_category_analysis(sub_theme, theme_papers, i)
                analysis_parts.append(section)
                analysis_parts.append("\n\n")
        else:
            # If no sub-themes, analyze all papers together
            section = self._generate_category_analysis(theme, papers, 1)
            analysis_parts.append(section)

        return "".join(analysis_parts)

    def _generate_category_analysis(self, category: str, papers: List[Paper], section_num: int) -> str:
        """Generate analysis for a category."""
        analysis = f"## 4.{section_num} {category}\n\n"

        analysis += f"### 4.{section_num}.1 Overview\n\n"
        analysis += f"This section analyzes {len(papers)} papers related to {category.lower()}.\n\n"

        analysis += f"### 4.{section_num}.2 Key Papers and Contributions\n\n"

        # Analyze top papers (by year, most recent first)
        sorted_papers = sorted([p for p in papers if p.year], key=lambda x: x.year, reverse=True)

        for paper in sorted_papers[:10]:  # Analyze top 10 papers
            cite_num = self.citation_manager.add_citation(paper)

            analysis += f"#### {paper.title} {self.citation_manager.format_citation(cite_num)}\n\n"
            analysis += f"**Authors**: {paper.authors if paper.authors else 'N/A'}\n\n"
            analysis += f"**Year**: {paper.year if paper.year else 'N/A'}\n\n"

            # Use brief summary
            if paper.brief_summary:
                analysis += f"**Summary**: {paper.brief_summary}\n\n"

            # Add key contributions
            contributions = [f for f in paper.findings if f.category == FindingCategory.CONTRIBUTION.value]
            if contributions:
                analysis += "**Key Contributions**:\n"
                for contrib in contributions[:3]:
                    analysis += f"- {contrib.finding_text}\n"
                analysis += "\n"

            # Add limitations
            limitations = [f for f in paper.findings if f.category == FindingCategory.LIMITATION.value]
            if limitations:
                analysis += "**Limitations**:\n"
                for limitation in limitations[:2]:
                    analysis += f"- {limitation.finding_text}\n"
                analysis += "\n"

        analysis += f"### 4.{section_num}.3 Comparative Analysis\n\n"
        analysis += self._generate_comparison_text(sorted_papers[:10])
        analysis += "\n"

        analysis += f"### 4.{section_num}.4 Summary\n\n"
        analysis += f"The papers in the {category} category demonstrate significant progress in {category.lower()}. "
        analysis += f"Common themes include improved methodologies, novel applications, and enhanced performance.\n\n"

        return analysis

    def _generate_comparison_text(self, papers: List[Paper]) -> str:
        """Generate comparative analysis text."""
        if not papers:
            return "No papers available for comparison.\n"

        text = "The approaches in this category can be compared along several dimensions:\n\n"

        # Year-based comparison
        year_dist = {}
        for paper in papers:
            if paper.year:
                year_dist[paper.year] = year_dist.get(paper.year, 0) + 1

        if year_dist:
            text += "**Temporal Distribution**:\n\n"
            text += self.table_formatter.create_year_distribution_table(year_dist)
            text += "\n\n"

        # Methodological comparison
        text += "**Methodological Approaches**: "
        text += "The surveyed papers employ diverse methodologies, ranging from theoretical foundations to "
        text += "empirical evaluations. Recent papers tend to focus more on practical applications and scalability.\n\n"

        return text

    def _generate_discussion(self, theme: str, papers: List[Paper], review_data: Dict) -> str:
        """Generate discussion section."""
        discussion = self.templates.format_discussion()

        # Key findings
        findings_text = f"Our survey of {len(papers)} papers in {theme} reveals several important findings:\n\n"

        # Analyze year distribution
        year_dist = review_data.get('year_distribution', {})
        if year_dist:
            recent_years = [y for y in year_dist.keys() if y >= 2020]
            recent_count = sum(year_dist[y] for y in recent_years)
            findings_text += f"1. **Growing Interest**: {recent_count} papers ({recent_count/len(papers)*100:.1f}%) "
            findings_text += f"were published since 2020, indicating strong recent interest.\n\n"

        # Common themes
        sub_themes = review_data.get('sub_themes', {})
        if sub_themes:
            findings_text += f"2. **Diverse Approaches**: The field encompasses {len(sub_themes)} distinct themes: "
            findings_text += ", ".join(sub_themes.keys()) + ".\n\n"

        discussion = discussion.replace("[IDENTIFY OVERARCHING THEMES ACROSS PAPERS]", findings_text)

        # Open challenges
        all_future_work = []
        for paper in papers[:20]:
            fw_findings = [f for f in paper.findings if f.category == FindingCategory.FUTURE_WORK.value]
            all_future_work.extend(fw_findings)

        if all_future_work:
            challenges_text = "Key open challenges identified in the literature include:\n\n"
            for i, fw in enumerate(all_future_work[:5], 1):
                challenges_text += f"{i}. {fw.finding_text}\n"

            discussion = discussion.replace("[IDENTIFY UNRESOLVED TECHNICAL PROBLEMS]", challenges_text)

        return discussion

    def _generate_conclusion(self, theme: str, papers: List[Paper]) -> str:
        """Generate conclusion section."""
        conclusion = self.templates.format_conclusion()

        summary = f"This survey has provided a comprehensive overview of {theme}, analyzing {len(papers)} "
        summary += f"significant papers. We have presented a taxonomy of approaches, provided detailed analysis "
        summary += f"of major categories, and identified key trends and open challenges.\n\n"

        summary += f"The field of {theme.lower()} continues to evolve rapidly, with significant contributions "
        summary += f"across multiple dimensions. Future work should focus on addressing the identified challenges "
        summary += f"and exploring emerging opportunities."

        conclusion = conclusion.replace("[SUMMARIZE THE MAIN CONTRIBUTIONS OF THE SURVEY]", summary)

        return conclusion

    def generate_section(self, theme: str, section_name: str) -> str:
        """
        Generate a single section of a review.

        Args:
            theme: Theme name
            section_name: Section to generate

        Returns:
            Generated section text
        """
        return self.generate_review(theme, sections=[section_name])

    def save_review(self, review_text: str, output_path: str):
        """
        Save review to file.

        Args:
            review_text: Generated review text
            output_path: Output file path
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(review_text)

        logger.info(f"Review saved to: {output_path}")

    def _convert_to_latex(self, theme: str, review_parts: List[str], author: str) -> str:
        """
        Convert markdown review to LaTeX.

        Args:
            theme: Review theme
            review_parts: List of review section parts
            author: Author name

        Returns:
            LaTeX formatted review
        """
        # Combine review parts
        full_review = "".join(review_parts)

        # Extract sections
        sections_dict = {}
        current_section = None
        current_content = []

        for line in full_review.split('\n'):
            if line.startswith('# '):
                # Save previous section
                if current_section:
                    sections_dict[current_section] = '\n'.join(current_content)

                # Start new section
                current_section = line[2:].strip().lower().replace(' ', '_')
                current_content = []
            else:
                current_content.append(line)

        # Save last section
        if current_section:
            sections_dict[current_section] = '\n'.join(current_content)

        # Generate LaTeX
        title = f"Literature Review: {theme}"
        latex = LaTeXFormatter.create_complete_document(
            title=title,
            sections=sections_dict,
            citations=self.citation_manager.citations,
            author=author
        )

        return latex

    def generate_latex_review(
        self,
        theme: str,
        sections: Optional[List[str]] = None,
        min_papers: int = 20,
        author: str = "Literature Review Generator"
    ) -> str:
        """
        Generate a LaTeX-formatted literature review.

        Args:
            theme: Theme for the review
            sections: Sections to include
            min_papers: Minimum papers required
            author: Author name

        Returns:
            LaTeX formatted review
        """
        return self.generate_review(
            theme=theme,
            sections=sections,
            output_format="latex",
            min_papers=min_papers,
            author=author
        )

    def save_overleaf_project(self, review_latex: str, output_dir: str):
        """
        Save review as Overleaf project.

        Args:
            review_latex: LaTeX content
            output_dir: Output directory
        """
        OverleafProject.create_project_structure(review_latex, output_dir)

    def estimate_review_length(self, theme: str) -> Dict[str, int]:
        """
        Estimate the length of a generated review.

        Args:
            theme: Theme name

        Returns:
            Dictionary with estimated word/token counts
        """
        papers = self.query_engine.get_papers_by_theme(theme)

        # Rough estimates based on section templates and paper count
        estimates = {
            'abstract': 250,
            'introduction': 1500,
            'background': 1000,
            'taxonomy': 500 + (len(papers) * 20),
            'analysis': len(papers) * 200,  # ~200 words per paper
            'discussion': 2000,
            'conclusion': 500,
            'references': len(papers) * 50,
        }

        total_words = sum(estimates.values())
        total_tokens = int(total_words / 0.75)  # Rough conversion

        return {
            'sections': estimates,
            'total_words': total_words,
            'total_tokens': total_tokens,
            'estimated_pages': total_words / 500,  # ~500 words per page
        }
