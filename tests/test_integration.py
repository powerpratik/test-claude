"""
Integration tests for the literature review application.
"""

import pytest
import tempfile
import shutil
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from knowledge_base.storage import KnowledgeBase
from knowledge_base.models import Paper, Theme
from processors.paper_processor import PaperProcessor
from retrieval.query_engine import QueryEngine
from generation.review_generator import ReviewGenerator


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    temp_dir = tempfile.mkdtemp()
    db_path = Path(temp_dir) / "test.db"

    kb = KnowledgeBase(str(db_path))
    kb.initialize_schema()

    yield kb

    # Cleanup
    kb.close()
    shutil.rmtree(temp_dir)


def test_knowledge_base_initialization(temp_db):
    """Test knowledge base initialization."""
    stats = temp_db.get_statistics()
    assert stats['total_papers'] == 0
    assert stats['total_themes'] == 0


def test_paper_addition(temp_db):
    """Test adding a paper to the knowledge base."""
    paper = Paper(
        title="Test Paper on Deep Learning",
        authors="John Doe, Jane Smith",
        year=2023,
        abstract="This is a test abstract about deep learning.",
        brief_summary="A paper about deep learning.",
        detailed_summary="This paper explores various aspects of deep learning."
    )

    paper_id = temp_db.add_paper(paper)
    assert paper_id > 0

    retrieved = temp_db.get_paper(paper_id)
    assert retrieved is not None
    assert retrieved.title == paper.title


def test_theme_operations(temp_db):
    """Test theme operations."""
    # Add theme
    theme = Theme(name="Deep Learning", description="Papers about deep learning")
    theme_id = temp_db.add_theme(theme)
    assert theme_id > 0

    # Add paper
    paper = Paper(title="DL Paper", brief_summary="Summary")
    paper_id = temp_db.add_paper(paper)

    # Link paper to theme
    temp_db.link_paper_theme(paper_id, theme_id)

    # Retrieve papers by theme
    papers = temp_db.get_papers_by_theme(theme_id)
    assert len(papers) == 1
    assert papers[0].title == "DL Paper"


def test_paper_processor(temp_db):
    """Test paper processor with sample text."""
    sample_text = """
Deep Learning for Computer Vision

John Doe, Jane Smith

Abstract: This paper presents a comprehensive study of deep learning
techniques applied to computer vision tasks. We demonstrate state-of-the-art
results on multiple benchmarks.

1. Introduction

Computer vision has seen remarkable advances in recent years due to deep
learning. Our work builds on these advances.

2. Methodology

We propose a novel convolutional neural network architecture that achieves
better performance than existing methods.

3. Results

Our experiments show 95% accuracy on the ImageNet dataset, outperforming
previous state-of-the-art by 3%.

4. Conclusion

This work demonstrates the effectiveness of deep learning for computer vision.
Future work will explore other domains.
    """

    processor = PaperProcessor(temp_db, config={})
    paper = processor.process_text(
        text=sample_text,
        title="Deep Learning for Computer Vision",
        themes=["Deep Learning", "Computer Vision"]
    )

    assert paper.id is not None
    assert paper.title == "Deep Learning for Computer Vision"
    assert len(paper.brief_summary) > 0
    assert len(paper.detailed_summary) > 0


def test_query_engine(temp_db):
    """Test query engine functionality."""
    # Add test papers
    for i in range(5):
        paper = Paper(
            title=f"Paper {i} on Machine Learning",
            year=2020 + i,
            brief_summary=f"Summary of paper {i}"
        )
        paper_id = temp_db.add_paper(paper)

        # Add theme
        theme = Theme(name="Machine Learning")
        theme_id = temp_db.add_theme(theme)
        temp_db.link_paper_theme(paper_id, theme_id)

    # Test query engine
    query_engine = QueryEngine(temp_db)
    papers = query_engine.get_papers_by_theme("Machine Learning")

    assert len(papers) == 5


def test_review_generator(temp_db):
    """Test review generator."""
    # Add sufficient papers
    theme_name = "Test Theme"
    theme = Theme(name=theme_name, description="Test theme")
    theme_id = temp_db.add_theme(theme)

    for i in range(25):  # Add 25 papers
        paper = Paper(
            title=f"Test Paper {i}",
            authors=f"Author {i}",
            year=2020 + (i % 4),
            abstract=f"Abstract for paper {i}",
            brief_summary=f"This paper discusses topic {i} in detail.",
            detailed_summary=f"A comprehensive study of topic {i} with novel contributions."
        )
        paper_id = temp_db.add_paper(paper)
        temp_db.link_paper_theme(paper_id, theme_id)

    # Generate review
    generator = ReviewGenerator(temp_db)
    review = generator.generate_review(
        theme=theme_name,
        sections=['introduction', 'conclusion'],
        min_papers=20
    )

    assert len(review) > 0
    assert theme_name in review
    assert "Introduction" in review
    assert "Conclusion" in review


def test_context_estimation(temp_db):
    """Test context usage estimation."""
    # Add papers with known summary lengths
    theme = Theme(name="Test")
    theme_id = temp_db.add_theme(theme)

    for i in range(10):
        paper = Paper(
            title=f"Paper {i}",
            brief_summary="This is a brief summary. " * 30,  # ~30 words
            detailed_summary="This is a detailed summary. " * 150  # ~150 words
        )
        paper_id = temp_db.add_paper(paper)
        temp_db.link_paper_theme(paper_id, theme_id)

    query_engine = QueryEngine(temp_db)
    papers = query_engine.get_papers_by_theme("Test")

    # Estimate context usage
    brief_tokens = query_engine.estimate_context_usage(papers, level='brief')
    detailed_tokens = query_engine.estimate_context_usage(papers, level='detailed')

    assert brief_tokens < detailed_tokens
    assert brief_tokens > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
