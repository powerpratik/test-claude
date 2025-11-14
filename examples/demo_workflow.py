#!/usr/bin/env python3
"""
Demo workflow showing the complete literature review generation process.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from config import get_config
from knowledge_base.storage import KnowledgeBase
from knowledge_base.models import Paper, Theme
from processors.paper_processor import PaperProcessor
from retrieval.query_engine import QueryEngine
from generation.review_generator import ReviewGenerator


def create_sample_papers(kb: KnowledgeBase) -> list:
    """Create sample papers for demonstration."""
    sample_papers = [
        {
            'title': 'Attention Is All You Need',
            'authors': 'Vaswani et al.',
            'year': 2017,
            'abstract': 'We propose the Transformer, a model architecture based solely on attention mechanisms.',
            'text': 'The dominant sequence transduction models are based on complex recurrent or convolutional neural networks. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely.'
        },
        {
            'title': 'BERT: Pre-training of Deep Bidirectional Transformers',
            'authors': 'Devlin et al.',
            'year': 2019,
            'abstract': 'We introduce BERT, which stands for Bidirectional Encoder Representations from Transformers.',
            'text': 'We introduce a new language representation model called BERT. Unlike recent language representation models, BERT is designed to pre-train deep bidirectional representations by jointly conditioning on both left and right context in all layers.'
        },
        {
            'title': 'GPT-3: Language Models are Few-Shot Learners',
            'authors': 'Brown et al.',
            'year': 2020,
            'abstract': 'We show that scaling up language models greatly improves task-agnostic, few-shot performance.',
            'text': 'Recent work has demonstrated substantial gains on many NLP tasks using pre-trained language models. We show that scaling up language models greatly improves task-agnostic, few-shot performance, reaching competitive results on many benchmarks.'
        },
        {
            'title': 'Deep Residual Learning for Image Recognition',
            'authors': 'He et al.',
            'year': 2016,
            'abstract': 'We present a residual learning framework to ease the training of networks that are substantially deeper.',
            'text': 'Deeper neural networks are more difficult to train. We present a residual learning framework to ease the training of networks that are substantially deeper than those used previously. We explicitly reformulate the layers as learning residual functions.'
        },
        {
            'title': 'EfficientNet: Rethinking Model Scaling',
            'authors': 'Tan & Le',
            'year': 2019,
            'abstract': 'We systematically study model scaling and identify that carefully balancing network depth, width, and resolution leads to better performance.',
            'text': 'Convolutional Neural Networks are commonly developed at a fixed resource budget, and then scaled up for better accuracy. In this paper, we systematically study model scaling and identify that carefully balancing network depth, width, and resolution can lead to better performance.'
        },
        {
            'title': 'MobileNets: Efficient Convolutional Neural Networks',
            'authors': 'Howard et al.',
            'year': 2017,
            'abstract': 'We present a class of efficient models called MobileNets for mobile and embedded vision applications.',
            'text': 'We present a class of efficient models called MobileNets for mobile and embedded vision applications. MobileNets are based on a streamlined architecture that uses depth-wise separable convolutions to build light weight deep neural networks.'
        },
        {
            'title': 'Vision Transformer: An Image is Worth 16x16 Words',
            'authors': 'Dosovitskiy et al.',
            'year': 2021,
            'abstract': 'While the Transformer architecture has become the de-facto standard for NLP, its applications to computer vision remain limited.',
            'text': 'While the Transformer architecture has become the de-facto standard for natural language processing tasks, its applications to computer vision remain limited. We show that pure transformers applied directly to sequences of image patches can perform very well on image classification tasks.'
        },
        {
            'title': 'Generative Adversarial Networks',
            'authors': 'Goodfellow et al.',
            'year': 2014,
            'abstract': 'We propose a new framework for estimating generative models via an adversarial process.',
            'text': 'We propose a new framework for estimating generative models via an adversarial process, in which we simultaneously train two models: a generative model G that captures the data distribution, and a discriminative model D that estimates the probability that a sample came from the training data.'
        },
    ]

    processor = PaperProcessor(kb, config={
        'summary_brief_tokens': 250,
        'summary_detailed_tokens': 1000,
    })

    added_papers = []

    for paper_data in sample_papers:
        # Determine themes based on content
        themes = []
        if 'transformer' in paper_data['title'].lower() or 'bert' in paper_data['title'].lower() or 'gpt' in paper_data['title'].lower():
            themes.append('Natural Language Processing')
            themes.append('Transformers')
        if 'image' in paper_data['title'].lower() or 'vision' in paper_data['title'].lower():
            themes.append('Computer Vision')
        if 'efficient' in paper_data['title'].lower() or 'mobile' in paper_data['title'].lower():
            themes.append('Model Efficiency')
        if 'gan' in paper_data['title'].lower() or 'generative' in paper_data['title'].lower():
            themes.append('Generative Models')

        # Create full text
        full_text = f"{paper_data['title']}\n\n{paper_data['authors']}\n\nAbstract:\n{paper_data['abstract']}\n\n{paper_data['text']}"

        paper = processor.process_text(
            text=full_text,
            title=paper_data['title'],
            themes=themes
        )

        added_papers.append(paper)
        print(f"✓ Added: {paper.title}")

    return added_papers


def main():
    """Run the demo workflow."""
    print("\n" + "="*80)
    print("Literature Review Generator - Demo Workflow")
    print("="*80 + "\n")

    # Step 1: Initialize
    print("Step 1: Initializing knowledge base...")
    config = get_config()

    # Use a demo database
    demo_db_path = Path("data/demo_knowledge_base.db")
    if demo_db_path.exists():
        demo_db_path.unlink()

    kb = KnowledgeBase(str(demo_db_path))
    kb.initialize_schema()
    print("✓ Knowledge base initialized\n")

    # Step 2: Add sample papers
    print("Step 2: Adding sample papers...")
    papers = create_sample_papers(kb)
    print(f"\n✓ Added {len(papers)} papers\n")

    # Step 3: Show statistics
    print("Step 3: Knowledge base statistics")
    stats = kb.get_statistics()
    print(f"  Total papers: {stats['total_papers']}")
    print(f"  Total themes: {stats['total_themes']}")
    print(f"  Total findings: {stats['total_findings']}")
    print()

    # Step 4: List themes
    print("Step 4: Available themes")
    themes = kb.get_all_themes()
    for theme in themes:
        print(f"  - {theme.name}: {theme.paper_count} papers")
    print()

    # Step 5: Query papers
    print("Step 5: Querying papers by theme")
    query_engine = QueryEngine(kb)
    nlp_papers = query_engine.get_papers_by_theme("Natural Language Processing")
    print(f"  Found {len(nlp_papers)} papers in 'Natural Language Processing'")
    for paper in nlp_papers:
        print(f"    - {paper.title} ({paper.year})")
    print()

    # Step 6: Generate review
    print("Step 6: Generating literature review...")
    generator = ReviewGenerator(kb)

    # Generate review for the theme with most papers
    target_theme = max(themes, key=lambda t: t.paper_count)
    print(f"  Theme: {target_theme.name}")
    print(f"  Papers: {target_theme.paper_count}")

    if target_theme.paper_count >= 3:  # Lower threshold for demo
        try:
            review = generator.generate_review(
                theme=target_theme.name,
                sections=['introduction', 'analysis', 'conclusion'],
                min_papers=3
            )

            output_path = Path("data/outputs/demo_review.md")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            generator.save_review(review, output_path)

            print(f"\n✓ Review generated successfully!")
            print(f"  Output: {output_path}")
            print(f"  Length: {len(review)} characters")
            print(f"  Citations: {generator.citation_manager.get_citation_count()}")
            print()

            # Show preview
            print("Preview (first 500 characters):")
            print("-" * 80)
            print(review[:500])
            print("...")
            print("-" * 80)

        except Exception as e:
            print(f"\n✗ Error generating review: {e}")
    else:
        print(f"  ⚠ Not enough papers ({target_theme.paper_count} < 3)")

    print("\n" + "="*80)
    print("Demo completed successfully!")
    print("="*80 + "\n")

    # Cleanup
    kb.close()


if __name__ == "__main__":
    main()
