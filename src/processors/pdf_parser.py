"""
PDF parsing utilities for extracting text from academic papers.
"""

import re
from pathlib import Path
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)


class PDFParser:
    """Parse PDF files and extract text content."""

    def __init__(self):
        """Initialize PDF parser."""
        self.pypdf_available = False
        self.pdfplumber_available = False

        # Try to import PDF libraries
        try:
            import PyPDF2
            self.pypdf_available = True
            self.PyPDF2 = PyPDF2
        except ImportError:
            logger.warning("PyPDF2 not available")

        try:
            import pdfplumber
            self.pdfplumber_available = True
            self.pdfplumber = pdfplumber
        except ImportError:
            logger.warning("pdfplumber not available")

        if not (self.pypdf_available or self.pdfplumber_available):
            logger.warning("No PDF parsing libraries available. Install PyPDF2 or pdfplumber.")

    def extract_text(self, pdf_path: str) -> str:
        """
        Extract text from a PDF file.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text content
        """
        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        # Try pdfplumber first (better quality)
        if self.pdfplumber_available:
            try:
                return self._extract_with_pdfplumber(pdf_path)
            except Exception as e:
                logger.warning(f"pdfplumber extraction failed: {e}")

        # Fall back to PyPDF2
        if self.pypdf_available:
            try:
                return self._extract_with_pypdf2(pdf_path)
            except Exception as e:
                logger.warning(f"PyPDF2 extraction failed: {e}")

        raise RuntimeError("Could not extract text from PDF with available libraries")

    def _extract_with_pdfplumber(self, pdf_path: Path) -> str:
        """Extract text using pdfplumber."""
        text_parts = []

        with self.pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)

        return "\n\n".join(text_parts)

    def _extract_with_pypdf2(self, pdf_path: Path) -> str:
        """Extract text using PyPDF2."""
        text_parts = []

        with open(pdf_path, 'rb') as file:
            pdf_reader = self.PyPDF2.PdfReader(file)

            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)

        return "\n\n".join(text_parts)

    def extract_metadata(self, text: str) -> Dict[str, str]:
        """
        Extract basic metadata from paper text.

        Args:
            text: Full text of paper

        Returns:
            Dictionary with extracted metadata
        """
        metadata = {
            'title': '',
            'authors': '',
            'abstract': '',
            'year': None,
        }

        # Extract title (usually first non-empty line or largest text)
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if lines:
            metadata['title'] = lines[0]

        # Try to find abstract
        abstract_match = re.search(
            r'(?:ABSTRACT|Abstract)\s*[:\-]?\s*(.*?)(?=\n\s*\n|\d+\s+Introduction|1\s+Introduction)',
            text,
            re.DOTALL | re.IGNORECASE
        )
        if abstract_match:
            metadata['abstract'] = self._clean_text(abstract_match.group(1))

        # Try to find year
        year_match = re.search(r'\b(19|20)\d{2}\b', text[:2000])
        if year_match:
            metadata['year'] = int(year_match.group(0))

        # Try to find authors (often after title, before abstract)
        author_section = text[:1000]
        # Look for common author patterns
        author_match = re.search(
            r'(?:Authors?|By)[:\s]+(.*?)(?=\n\s*\n|Abstract|ABSTRACT)',
            author_section,
            re.DOTALL | re.IGNORECASE
        )
        if author_match:
            metadata['authors'] = self._clean_text(author_match.group(1))

        return metadata

    def _clean_text(self, text: str) -> str:
        """Clean extracted text."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove page numbers
        text = re.sub(r'\b\d+\b(?=\s*$)', '', text, flags=re.MULTILINE)
        return text.strip()

    def is_available(self) -> bool:
        """Check if PDF parsing is available."""
        return self.pypdf_available or self.pdfplumber_available


class TextExtractor:
    """Extract structured information from paper text."""

    @staticmethod
    def extract_sections(text: str) -> List[Dict[str, str]]:
        """
        Extract sections from paper text.

        Args:
            text: Full paper text

        Returns:
            List of sections with title and content
        """
        sections = []

        # Common section headers in academic papers
        section_patterns = [
            r'^\s*(\d+\.?\s+)?Abstract\s*$',
            r'^\s*(\d+\.?\s+)?Introduction\s*$',
            r'^\s*(\d+\.?\s+)?Related\s+Work\s*$',
            r'^\s*(\d+\.?\s+)?Background\s*$',
            r'^\s*(\d+\.?\s+)?Methodology\s*$',
            r'^\s*(\d+\.?\s+)?Methods?\s*$',
            r'^\s*(\d+\.?\s+)?Approach\s*$',
            r'^\s*(\d+\.?\s+)?Results?\s*$',
            r'^\s*(\d+\.?\s+)?Evaluation\s*$',
            r'^\s*(\d+\.?\s+)?Experiments?\s*$',
            r'^\s*(\d+\.?\s+)?Discussion\s*$',
            r'^\s*(\d+\.?\s+)?Conclusion\s*$',
            r'^\s*(\d+\.?\s+)?Future\s+Work\s*$',
            r'^\s*(\d+\.?\s+)?References?\s*$',
        ]

        # Create combined pattern
        combined_pattern = '|'.join(f'({p})' for p in section_patterns)

        # Find all section headers
        lines = text.split('\n')
        section_indices = []

        for i, line in enumerate(lines):
            if re.match(combined_pattern, line, re.IGNORECASE):
                section_indices.append((i, line.strip()))

        # Extract content between headers
        for i, (start_idx, header) in enumerate(section_indices):
            end_idx = section_indices[i + 1][0] if i + 1 < len(section_indices) else len(lines)

            content = '\n'.join(lines[start_idx + 1:end_idx])
            content = TextExtractor._clean_section_text(content)

            if content:
                sections.append({
                    'title': header,
                    'content': content
                })

        return sections

    @staticmethod
    def _clean_section_text(text: str) -> str:
        """Clean section text."""
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        return text.strip()

    @staticmethod
    def extract_references(text: str) -> List[str]:
        """
        Extract references from paper text.

        Args:
            text: Full paper text

        Returns:
            List of reference strings
        """
        references = []

        # Find references section
        ref_match = re.search(
            r'(?:REFERENCES|References)\s*\n(.*?)(?:\n\s*\n|\Z)',
            text,
            re.DOTALL | re.IGNORECASE
        )

        if ref_match:
            ref_text = ref_match.group(1)

            # Split by numbered references [1], [2], etc. or 1., 2., etc.
            ref_entries = re.split(r'\n\s*(?:\[\d+\]|\d+\.)', ref_text)

            for entry in ref_entries:
                entry = entry.strip()
                if len(entry) > 20:  # Minimum length for a valid reference
                    references.append(entry)

        return references
