"""
Data models for the knowledge base.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum


class SectionType(Enum):
    """Types of paper sections."""
    ABSTRACT = "abstract"
    INTRODUCTION = "introduction"
    RELATED_WORK = "related_work"
    METHODOLOGY = "methodology"
    RESULTS = "results"
    DISCUSSION = "discussion"
    CONCLUSION = "conclusion"
    FUTURE_WORK = "future_work"
    OTHER = "other"


class FindingCategory(Enum):
    """Categories of key findings."""
    CONTRIBUTION = "contribution"
    LIMITATION = "limitation"
    FUTURE_WORK = "future_work"
    METHODOLOGY = "methodology"
    RESULT = "result"


@dataclass
class Paper:
    """Represents an academic paper."""
    id: Optional[int] = None
    title: str = ""
    authors: str = ""
    year: Optional[int] = None
    venue: str = ""
    doi: str = ""
    abstract: str = ""
    full_text_path: str = ""
    brief_summary: str = ""
    detailed_summary: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # Related data (not stored directly in papers table)
    sections: List['Section'] = field(default_factory=list)
    findings: List['KeyFinding'] = field(default_factory=list)
    themes: List['Theme'] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'authors': self.authors,
            'year': self.year,
            'venue': self.venue,
            'doi': self.doi,
            'abstract': self.abstract,
            'full_text_path': self.full_text_path,
            'brief_summary': self.brief_summary,
            'detailed_summary': self.detailed_summary,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Paper':
        """Create from dictionary."""
        paper = cls()
        for key, value in data.items():
            if hasattr(paper, key):
                if key in ['created_at', 'updated_at'] and isinstance(value, str):
                    setattr(paper, key, datetime.fromisoformat(value))
                else:
                    setattr(paper, key, value)
        return paper

    def __repr__(self) -> str:
        return f"Paper(id={self.id}, title='{self.title[:50]}...', year={self.year})"


@dataclass
class Section:
    """Represents a section of a paper."""
    id: Optional[int] = None
    paper_id: Optional[int] = None
    section_type: str = SectionType.OTHER.value
    title: str = ""
    content: str = ""
    summary: str = ""
    order_index: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'paper_id': self.paper_id,
            'section_type': self.section_type,
            'title': self.title,
            'content': self.content,
            'summary': self.summary,
            'order_index': self.order_index,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Section':
        """Create from dictionary."""
        section = cls()
        for key, value in data.items():
            if hasattr(section, key):
                setattr(section, key, value)
        return section

    def __repr__(self) -> str:
        return f"Section(id={self.id}, paper_id={self.paper_id}, type={self.section_type})"


@dataclass
class KeyFinding:
    """Represents a key finding from a paper."""
    id: Optional[int] = None
    paper_id: Optional[int] = None
    finding_text: str = ""
    category: str = FindingCategory.CONTRIBUTION.value
    importance_score: float = 0.5

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'paper_id': self.paper_id,
            'finding_text': self.finding_text,
            'category': self.category,
            'importance_score': self.importance_score,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'KeyFinding':
        """Create from dictionary."""
        finding = cls()
        for key, value in data.items():
            if hasattr(finding, key):
                setattr(finding, key, value)
        return finding

    def __repr__(self) -> str:
        return f"KeyFinding(id={self.id}, category={self.category}, score={self.importance_score})"


@dataclass
class Theme:
    """Represents a research theme or topic."""
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    paper_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'paper_count': self.paper_count,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Theme':
        """Create from dictionary."""
        theme = cls()
        for key, value in data.items():
            if hasattr(theme, key):
                setattr(theme, key, value)
        return theme

    def __repr__(self) -> str:
        return f"Theme(id={self.id}, name='{self.name}', papers={self.paper_count})"


@dataclass
class PaperTheme:
    """Represents the relationship between a paper and a theme."""
    paper_id: int
    theme_id: int
    relevance_score: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'paper_id': self.paper_id,
            'theme_id': self.theme_id,
            'relevance_score': self.relevance_score,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PaperTheme':
        """Create from dictionary."""
        return cls(
            paper_id=data['paper_id'],
            theme_id=data['theme_id'],
            relevance_score=data.get('relevance_score', 1.0)
        )


@dataclass
class Citation:
    """Represents a citation relationship between papers."""
    id: Optional[int] = None
    source_paper_id: int = 0
    cited_paper_id: int = 0
    context: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'source_paper_id': self.source_paper_id,
            'cited_paper_id': self.cited_paper_id,
            'context': self.context,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Citation':
        """Create from dictionary."""
        citation = cls()
        for key, value in data.items():
            if hasattr(citation, key):
                setattr(citation, key, value)
        return citation

    def __repr__(self) -> str:
        return f"Citation(source={self.source_paper_id}, cited={self.cited_paper_id})"
