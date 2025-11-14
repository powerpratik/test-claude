"""
Summarization utilities for generating multi-level summaries.
"""

import re
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class Summarizer:
    """Generate summaries at different granularity levels."""

    def __init__(self, brief_token_limit: int = 250, detailed_token_limit: int = 1000):
        """
        Initialize summarizer.

        Args:
            brief_token_limit: Target token count for brief summaries
            detailed_token_limit: Target token count for detailed summaries
        """
        self.brief_token_limit = brief_token_limit
        self.detailed_token_limit = detailed_token_limit

    def generate_brief_summary(self, text: str, abstract: str = "") -> str:
        """
        Generate a brief summary (~250 tokens).

        Strategy: Use abstract if available, otherwise extract key sentences.

        Args:
            text: Full text
            abstract: Paper abstract (if available)

        Returns:
            Brief summary
        """
        if abstract and len(abstract) > 50:
            # Use abstract as brief summary
            summary = self._truncate_to_tokens(abstract, self.brief_token_limit)
            return summary

        # If no abstract, extract from introduction and conclusion
        intro_text = self._extract_section(text, ['introduction', 'abstract'])
        conclusion_text = self._extract_section(text, ['conclusion', 'summary'])

        combined = intro_text[:1000] + " " + conclusion_text[:1000]

        # Extract most important sentences
        sentences = self._extract_sentences(combined)
        key_sentences = sentences[:3]  # Take first 3 sentences

        summary = " ".join(key_sentences)
        return self._truncate_to_tokens(summary, self.brief_token_limit)

    def generate_detailed_summary(self, text: str, sections: List[Dict] = None) -> str:
        """
        Generate a detailed summary (~1000 tokens).

        Strategy: Extract key information from each major section.

        Args:
            text: Full text
            sections: Pre-extracted sections (if available)

        Returns:
            Detailed summary
        """
        summary_parts = []

        # Key sections to include
        section_names = [
            'abstract',
            'introduction',
            'methodology',
            'methods',
            'approach',
            'results',
            'evaluation',
            'conclusion'
        ]

        if sections:
            # Use pre-extracted sections
            for section in sections:
                section_title = section.get('title', '').lower()
                if any(name in section_title for name in section_names):
                    content = section.get('content', '')
                    summary = self._summarize_section(content, max_tokens=150)
                    if summary:
                        summary_parts.append(f"**{section['title']}**: {summary}")

        else:
            # Extract sections from text
            for section_name in section_names:
                section_text = self._extract_section(text, [section_name])
                if section_text:
                    summary = self._summarize_section(section_text, max_tokens=150)
                    if summary:
                        summary_parts.append(f"**{section_name.title()}**: {summary}")

        detailed = " ".join(summary_parts)
        return self._truncate_to_tokens(detailed, self.detailed_token_limit)

    def _extract_section(self, text: str, section_names: List[str]) -> str:
        """Extract text from a specific section."""
        text_lower = text.lower()

        for section_name in section_names:
            # Try to find section header
            patterns = [
                rf'(?:^|\n)\s*(?:\d+\.?\s+)?{section_name}\s*(?:\n|$)',
                rf'(?:^|\n)\s*{section_name}\s*[:\-]\s*',
            ]

            for pattern in patterns:
                match = re.search(pattern, text_lower)
                if match:
                    start_pos = match.end()

                    # Find end of section (next section header or end of text)
                    next_section = re.search(
                        r'(?:\n\s*(?:\d+\.?\s+)?[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s*(?:\n|$))',
                        text[start_pos:start_pos + 3000]
                    )

                    if next_section:
                        end_pos = start_pos + next_section.start()
                    else:
                        end_pos = start_pos + 2000

                    return text[start_pos:end_pos].strip()

        return ""

    def _summarize_section(self, text: str, max_tokens: int = 150) -> str:
        """Summarize a section by extracting key sentences."""
        sentences = self._extract_sentences(text)

        if not sentences:
            return ""

        # Take first 2-3 sentences as summary
        num_sentences = min(3, len(sentences))
        summary = " ".join(sentences[:num_sentences])

        return self._truncate_to_tokens(summary, max_tokens)

    def _extract_sentences(self, text: str) -> List[str]:
        """Extract sentences from text."""
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+\s+', text)

        # Clean and filter
        cleaned = []
        for sent in sentences:
            sent = sent.strip()
            # Filter out very short or likely non-sentences
            if len(sent) > 20 and len(sent.split()) > 3:
                cleaned.append(sent)

        return cleaned

    def _truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        """
        Truncate text to approximately max_tokens.

        Note: This uses word count as proxy for tokens (rough: 1 token ≈ 0.75 words)
        """
        words = text.split()
        max_words = int(max_tokens * 0.75)

        if len(words) <= max_words:
            return text

        # Truncate and add ellipsis
        truncated_words = words[:max_words]
        return " ".join(truncated_words) + "..."

    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count for text.

        Rough approximation: 1 token ≈ 0.75 words
        """
        words = len(text.split())
        return int(words / 0.75)


class KeyFindingExtractor:
    """Extract key findings from papers."""

    @staticmethod
    def extract_contributions(text: str) -> List[str]:
        """
        Extract main contributions from paper.

        Args:
            text: Full paper text

        Returns:
            List of contribution statements
        """
        contributions = []

        # Look for explicit contribution statements
        patterns = [
            r'(?:our|the)\s+(?:main\s+)?contributions?\s+(?:are|is|include)[:\s]+(.*?)(?:\.|$)',
            r'we\s+(?:present|propose|introduce|demonstrate)\s+(.*?)(?:\.|$)',
            r'this\s+paper\s+(?:presents|proposes|introduces)\s+(.*?)(?:\.|$)',
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                contrib = match.group(1).strip()
                if len(contrib) > 20:
                    contributions.append(contrib)

        # Look in abstract and introduction
        intro_text = KeyFindingExtractor._get_intro_section(text)
        if intro_text:
            # Extract bullet points or numbered lists
            list_items = re.findall(r'(?:^|\n)\s*[-•*]\s*(.*?)(?:\n|$)', intro_text)
            contributions.extend([item.strip() for item in list_items if len(item) > 20])

        return contributions[:5]  # Return top 5

    @staticmethod
    def extract_limitations(text: str) -> List[str]:
        """Extract limitations from paper."""
        limitations = []

        # Look for limitations section
        patterns = [
            r'(?:limitations?|weaknesses?)[:\s]+(.*?)(?:\n\s*\n|\d+\s+\w+|$)',
            r'(?:however|although|unfortunately)[,\s]+(.*?)(?:\.|$)',
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                limitation = match.group(1).strip()
                if len(limitation) > 20:
                    limitations.append(limitation)

        return limitations[:3]  # Return top 3

    @staticmethod
    def extract_future_work(text: str) -> List[str]:
        """Extract future work directions."""
        future_work = []

        # Look for future work section
        future_section = re.search(
            r'(?:future\s+work|future\s+directions?)[:\s]+(.*?)(?:\n\s*\n|\d+\s+\w+|$)',
            text.lower(),
            re.DOTALL
        )

        if future_section:
            section_text = future_section.group(1)
            sentences = re.split(r'[.!?]+\s+', section_text)

            for sent in sentences[:3]:
                sent = sent.strip()
                if len(sent) > 20:
                    future_work.append(sent)

        return future_work

    @staticmethod
    def _get_intro_section(text: str) -> str:
        """Get introduction section text."""
        match = re.search(
            r'(?:introduction|abstract)\s*[:\-]?\s*(.*?)(?:\n\s*\n\d+|\d+\s+\w+)',
            text.lower(),
            re.DOTALL
        )

        if match:
            return match.group(1)[:2000]

        return text[:2000]  # Fall back to first 2000 chars
