"""
Main paper processor for extracting and processing academic papers.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional

from .pdf_parser import PDFParser, TextExtractor
from .summarizer import Summarizer, KeyFindingExtractor
from ..knowledge_base.models import Paper, Section, KeyFinding, SectionType, FindingCategory
from ..knowledge_base.storage import KnowledgeBase

logger = logging.getLogger(__name__)


class PaperProcessor:
    """Main processor for ingesting and processing papers."""

    def __init__(self, knowledge_base: KnowledgeBase, config: Optional[Dict] = None):
        """
        Initialize paper processor.

        Args:
            knowledge_base: KnowledgeBase instance
            config: Optional configuration dictionary
        """
        self.kb = knowledge_base
        self.config = config or {}

        # Initialize components
        self.pdf_parser = PDFParser()
        self.text_extractor = TextExtractor()
        self.summarizer = Summarizer(
            brief_token_limit=self.config.get('summary_brief_tokens', 250),
            detailed_token_limit=self.config.get('summary_detailed_tokens', 1000)
        )
        self.finding_extractor = KeyFindingExtractor()

    def process_paper(self, file_path: str, themes: Optional[List[str]] = None) -> Paper:
        """
        Process a paper file and add to knowledge base.

        Args:
            file_path: Path to paper file (PDF or text)
            themes: Optional list of theme names to associate with paper

        Returns:
            Processed Paper object
        """
        file_path = Path(file_path)
        logger.info(f"Processing paper: {file_path.name}")

        # Extract text
        if file_path.suffix.lower() == '.pdf':
            if not self.pdf_parser.is_available():
                raise RuntimeError("PDF parsing not available. Install PyPDF2 or pdfplumber.")
            text = self.pdf_parser.extract_text(file_path)
        else:
            # Assume text file
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()

        # Extract metadata
        metadata = self._extract_metadata(text, file_path)

        # Extract sections
        sections = self._extract_sections(text)

        # Generate summaries
        abstract = metadata.get('abstract', '')
        brief_summary = self.summarizer.generate_brief_summary(text, abstract)
        detailed_summary = self.summarizer.generate_detailed_summary(text, sections)

        # Create paper object
        paper = Paper(
            title=metadata['title'],
            authors=metadata.get('authors', ''),
            year=metadata.get('year'),
            venue=metadata.get('venue', ''),
            doi=metadata.get('doi', ''),
            abstract=abstract,
            full_text_path=str(file_path.absolute()),
            brief_summary=brief_summary,
            detailed_summary=detailed_summary,
        )

        # Add to database
        paper_id = self.kb.add_paper(paper)
        paper.id = paper_id

        logger.info(f"Added paper to KB with ID: {paper_id}")

        # Add sections
        for i, section_data in enumerate(sections):
            section = Section(
                paper_id=paper_id,
                section_type=self._classify_section_type(section_data['title']),
                title=section_data['title'],
                content=section_data['content'][:10000],  # Limit content size
                summary=self.summarizer._summarize_section(section_data['content'], max_tokens=200),
                order_index=i
            )
            self.kb.add_section(section)

        logger.info(f"Added {len(sections)} sections")

        # Extract and add key findings
        findings = self._extract_findings(text, paper_id)
        for finding in findings:
            self.kb.add_finding(finding)

        logger.info(f"Added {len(findings)} key findings")

        # Associate with themes
        if themes:
            for theme_name in themes:
                theme = self.kb.get_theme_by_name(theme_name)
                if not theme:
                    from ..knowledge_base.models import Theme
                    theme_obj = Theme(name=theme_name, description=f"Papers related to {theme_name}")
                    theme_id = self.kb.add_theme(theme_obj)
                else:
                    theme_id = theme.id

                self.kb.link_paper_theme(paper_id, theme_id)
                logger.info(f"Linked paper to theme: {theme_name}")

        # Auto-classify themes if enabled
        if self.config.get('auto_classify_themes', True):
            auto_themes = self._auto_classify_themes(text, metadata)
            for theme_name in auto_themes:
                if themes and theme_name in themes:
                    continue  # Skip if already added

                theme = self.kb.get_theme_by_name(theme_name)
                if not theme:
                    from ..knowledge_base.models import Theme
                    theme_obj = Theme(name=theme_name, description=f"Papers related to {theme_name}")
                    theme_id = self.kb.add_theme(theme_obj)
                else:
                    theme_id = theme.id

                self.kb.link_paper_theme(paper_id, theme_id, relevance_score=0.7)

        logger.info(f"Successfully processed paper: {paper.title}")
        return paper

    def process_text(self, text: str, title: str, themes: Optional[List[str]] = None) -> Paper:
        """
        Process paper from text content.

        Args:
            text: Paper text content
            title: Paper title
            themes: Optional list of themes

        Returns:
            Processed Paper object
        """
        logger.info(f"Processing text paper: {title}")

        # Extract metadata
        metadata = self._extract_metadata(text)
        metadata['title'] = title  # Override with provided title

        # Extract sections
        sections = self._extract_sections(text)

        # Generate summaries
        abstract = metadata.get('abstract', '')
        brief_summary = self.summarizer.generate_brief_summary(text, abstract)
        detailed_summary = self.summarizer.generate_detailed_summary(text, sections)

        # Create and add paper
        paper = Paper(
            title=metadata['title'],
            authors=metadata.get('authors', ''),
            year=metadata.get('year'),
            venue=metadata.get('venue', ''),
            abstract=abstract,
            brief_summary=brief_summary,
            detailed_summary=detailed_summary,
        )

        paper_id = self.kb.add_paper(paper)
        paper.id = paper_id

        # Add sections
        for i, section_data in enumerate(sections):
            section = Section(
                paper_id=paper_id,
                section_type=self._classify_section_type(section_data['title']),
                title=section_data['title'],
                content=section_data['content'][:10000],
                summary=self.summarizer._summarize_section(section_data['content'], max_tokens=200),
                order_index=i
            )
            self.kb.add_section(section)

        # Extract findings
        findings = self._extract_findings(text, paper_id)
        for finding in findings:
            self.kb.add_finding(finding)

        # Associate themes
        if themes:
            for theme_name in themes:
                theme = self.kb.get_theme_by_name(theme_name)
                if not theme:
                    from ..knowledge_base.models import Theme
                    theme_obj = Theme(name=theme_name)
                    theme_id = self.kb.add_theme(theme_obj)
                else:
                    theme_id = theme.id

                self.kb.link_paper_theme(paper_id, theme_id)

        return paper

    def _extract_metadata(self, text: str, file_path: Optional[Path] = None) -> Dict:
        """Extract metadata from text."""
        if file_path and file_path.suffix.lower() == '.pdf':
            metadata = self.pdf_parser.extract_metadata(text)
        else:
            metadata = {'title': '', 'authors': '', 'abstract': '', 'year': None}

            # Try to extract from text
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            if lines:
                metadata['title'] = lines[0][:200]  # First line as title

        return metadata

    def _extract_sections(self, text: str) -> List[Dict]:
        """Extract sections from text."""
        return self.text_extractor.extract_sections(text)

    def _extract_findings(self, text: str, paper_id: int) -> List[KeyFinding]:
        """Extract key findings from text."""
        findings = []

        # Extract contributions
        contributions = self.finding_extractor.extract_contributions(text)
        for contrib in contributions:
            finding = KeyFinding(
                paper_id=paper_id,
                finding_text=contrib[:500],
                category=FindingCategory.CONTRIBUTION.value,
                importance_score=0.9
            )
            findings.append(finding)

        # Extract limitations
        limitations = self.finding_extractor.extract_limitations(text)
        for limitation in limitations:
            finding = KeyFinding(
                paper_id=paper_id,
                finding_text=limitation[:500],
                category=FindingCategory.LIMITATION.value,
                importance_score=0.7
            )
            findings.append(finding)

        # Extract future work
        future_work = self.finding_extractor.extract_future_work(text)
        for fw in future_work:
            finding = KeyFinding(
                paper_id=paper_id,
                finding_text=fw[:500],
                category=FindingCategory.FUTURE_WORK.value,
                importance_score=0.6
            )
            findings.append(finding)

        return findings

    def _classify_section_type(self, section_title: str) -> str:
        """Classify section type from title."""
        title_lower = section_title.lower()

        if 'abstract' in title_lower:
            return SectionType.ABSTRACT.value
        elif 'introduction' in title_lower:
            return SectionType.INTRODUCTION.value
        elif 'related' in title_lower or 'prior' in title_lower:
            return SectionType.RELATED_WORK.value
        elif 'method' in title_lower or 'approach' in title_lower:
            return SectionType.METHODOLOGY.value
        elif 'result' in title_lower or 'evaluation' in title_lower or 'experiment' in title_lower:
            return SectionType.RESULTS.value
        elif 'discussion' in title_lower:
            return SectionType.DISCUSSION.value
        elif 'conclusion' in title_lower:
            return SectionType.CONCLUSION.value
        elif 'future' in title_lower:
            return SectionType.FUTURE_WORK.value
        else:
            return SectionType.OTHER.value

    def _auto_classify_themes(self, text: str, metadata: Dict) -> List[str]:
        """Auto-classify paper into themes based on content."""
        themes = []
        text_lower = text.lower()

        # Keyword-based classification
        theme_keywords = {
            'Machine Learning': ['machine learning', 'supervised learning', 'unsupervised learning', 'ml'],
            'Deep Learning': ['deep learning', 'neural network', 'cnn', 'rnn', 'lstm', 'transformer'],
            'Natural Language Processing': ['nlp', 'natural language', 'text processing', 'language model'],
            'Computer Vision': ['computer vision', 'image processing', 'object detection', 'segmentation'],
            'Reinforcement Learning': ['reinforcement learning', 'rl', 'policy', 'reward'],
            'Data Mining': ['data mining', 'knowledge discovery', 'pattern mining'],
            'Distributed Systems': ['distributed', 'parallel', 'cluster', 'scalability'],
            'Security and Privacy': ['security', 'privacy', 'encryption', 'authentication'],
        }

        for theme_name, keywords in theme_keywords.items():
            # Check if any keywords appear in text
            if any(keyword in text_lower for keyword in keywords):
                themes.append(theme_name)

        return themes[:3]  # Return top 3 themes
