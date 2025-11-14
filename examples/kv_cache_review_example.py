#!/usr/bin/env python3
"""
Complete example: Literature review for KV Cache Eviction in LLM Inference

This script demonstrates how to create a comprehensive literature review
on "KV Cache Eviction Algorithms for Large-Scale LLM Inference with Long Context"

Use case: Survey papers on KV cache optimization, eviction strategies,
and memory management for long-context LLM inference.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from knowledge_base.storage import KnowledgeBase
from knowledge_base.models import Paper, Theme, KeyFinding, FindingCategory
from processors.paper_processor import PaperProcessor
from retrieval.query_engine import QueryEngine
from generation.review_generator import ReviewGenerator


def create_sample_papers_kv_cache(kb: KnowledgeBase, processor: PaperProcessor):
    """
    Create sample papers on KV cache eviction.

    In real usage, you would:
    1. Collect actual papers from ACM DL, arXiv, conferences
    2. Process PDFs using processor.process_paper()
    3. Or manually add paper metadata
    """

    papers_data = [
        {
            'title': 'Efficient Memory Management for Large Language Model Serving with PagedAttention',
            'authors': 'Kwon et al.',
            'year': 2023,
            'venue': 'SOSP 2023',
            'abstract': 'Efficient memory management is critical for serving large language models. We introduce PagedAttention, an attention algorithm inspired by virtual memory and paging in operating systems.',
            'summary': 'This paper introduces PagedAttention for efficient KV cache management. Key contributions include treating KV cache like virtual memory with paging, achieving near-zero waste in memory fragmentation, and enabling flexible sharing of KV cache between sequences. Demonstrates 2-4x throughput improvement.',
            'findings': [
                ('Memory fragmentation is a major bottleneck in LLM serving, wasting up to 80% of memory', 'contribution'),
                ('PagedAttention eliminates memory waste through non-contiguous memory allocation', 'contribution'),
                ('System achieves 2-4x throughput improvement over baseline', 'result'),
            ],
            'themes': ['KV Cache Optimization', 'LLM Serving', 'Memory Management']
        },
        {
            'title': 'H2O: Heavy-Hitter Oracle for Efficient Generative Inference of Large Language Models',
            'authors': 'Zhang et al.',
            'year': 2023,
            'venue': 'NeurIPS 2023',
            'abstract': 'We observe that a small portion of tokens contribute most of the attention scores. We propose H2O, a KV cache eviction policy that retains heavy hitter tokens.',
            'summary': 'H2O identifies that ~20% of tokens account for ~80% of attention mass (heavy hitters). Proposes eviction policy that keeps recent tokens and heavy hitters, evicting others. Achieves similar quality with 20-30% KV cache size, enabling 3x longer contexts.',
            'findings': [
                ('Discovered heavy-hitter phenomenon: 20% tokens contribute 80% attention', 'contribution'),
                ('H2O eviction policy maintains quality with 20-30% cache size', 'result'),
                ('Enables 3x longer context windows with same memory budget', 'result'),
                ('Performance degrades on tasks requiring random access patterns', 'limitation'),
            ],
            'themes': ['KV Cache Eviction', 'Attention Optimization', 'Long Context']
        },
        {
            'title': 'StreamingLLM: Efficient Streaming Language Models with Attention Sinks',
            'authors': 'Xiao et al.',
            'year': 2023,
            'venue': 'ICLR 2024',
            'abstract': 'We discover attention sinks - initial tokens that accumulate excessive attention. We develop StreamingLLM that maintains performance in streaming settings.',
            'summary': 'Discovers attention sink phenomenon where initial tokens receive disproportionate attention. StreamingLLM retains attention sink tokens and recent context, enabling infinite sequence length. Achieves stable perplexity with fixed cache size of 256-1024 tokens regardless of sequence length.',
            'findings': [
                ('Attention sinks explain why naive window attention fails', 'contribution'),
                ('StreamingLLM enables infinite context with fixed memory', 'contribution'),
                ('Stable perplexity with just 256-1024 token cache', 'result'),
                ('Does not work well for retrieval tasks requiring global context', 'limitation'),
            ],
            'themes': ['KV Cache Eviction', 'Streaming Inference', 'Long Context']
        },
        {
            'title': 'Scissorhands: Exploiting the Persistence of Importance Hypothesis for LLM KV Cache Compression',
            'authors': 'Liu et al.',
            'year': 2023,
            'venue': 'arXiv 2023',
            'abstract': 'We discover that important tokens identified early remain important throughout generation. We propose Scissorhands for dynamic KV cache pruning.',
            'summary': 'Introduces "persistence of importance" hypothesis: tokens important in early layers remain important in later layers. Scissorhands uses this to identify and retain important tokens early. Achieves 5x compression with minimal quality loss. Dynamic pruning adapts to different generation stages.',
            'findings': [
                ('Important tokens persist across layers (persistence of importance)', 'contribution'),
                ('Scissorhands achieves 5x KV cache compression', 'result'),
                ('Dynamic pruning adapts to generation phase', 'methodology'),
                ('Requires calibration data for importance estimation', 'limitation'),
            ],
            'themes': ['KV Cache Compression', 'Token Importance', 'Inference Optimization']
        },
        {
            'title': 'FastGen: Improving LLM Performance with KV Cache Offloading',
            'authors': 'Chen et al.',
            'year': 2024,
            'venue': 'MLSys 2024',
            'abstract': 'We propose offloading KV cache to CPU memory and SSD for ultra-long contexts. Demonstrates 100K+ token support on single GPU.',
            'summary': 'FastGen uses hierarchical cache management: GPU memory for hot cache, CPU RAM for warm cache, SSD for cold cache. Implements prefetching and intelligent eviction. Supports 100K+ tokens on single A100 GPU. Tradeoff: 2-3x slower but enables otherwise impossible contexts.',
            'findings': [
                ('Hierarchical caching (GPU/CPU/SSD) enables ultra-long contexts', 'contribution'),
                ('Achieves 100K+ tokens on single GPU', 'result'),
                ('2-3x latency overhead from offloading', 'limitation'),
                ('Prefetching reduces impact of slow storage', 'methodology'),
            ],
            'themes': ['KV Cache Offloading', 'Long Context', 'Memory Hierarchy']
        },
        {
            'title': 'Model Tells You What to Discard: Adaptive KV Cache Compression for LLMs',
            'authors': 'Wang et al.',
            'year': 2024,
            'venue': 'ICLR 2024',
            'abstract': 'We propose model-adaptive KV cache compression that uses the model itself to decide what to evict.',
            'summary': 'Introduces learnable eviction module that predicts token importance. Trained end-to-end with language model. Adapts eviction strategy per layer and per task. Outperforms static policies across diverse tasks. Additional training overhead but superior quality-compression tradeoff.',
            'findings': [
                ('Learnable eviction policies outperform heuristics', 'contribution'),
                ('Per-layer and per-task adaptation crucial for performance', 'contribution'),
                ('Better quality-compression tradeoff than static methods', 'result'),
                ('Requires model modification and additional training', 'limitation'),
            ],
            'themes': ['Adaptive Eviction', 'KV Cache Compression', 'Learning-based Methods']
        },
        {
            'title': 'Infinite-LLM: Efficient LLM Service for Long Context with DistAttention and Distributed KV Cache',
            'authors': 'Li et al.',
            'year': 2024,
            'venue': 'OSDI 2024',
            'abstract': 'We propose distributed KV cache across multiple GPUs for extreme-length contexts. Introduces DistAttention for efficient distributed attention computation.',
            'summary': 'Infinite-LLM distributes KV cache across multiple GPUs using DistAttention. Handles million-token contexts by partitioning cache. Implements cache-aware scheduling and load balancing. Achieves near-linear scaling up to 8 GPUs. Demonstrates 1M token context processing.',
            'findings': [
                ('DistAttention enables distributed KV cache computation', 'contribution'),
                ('Near-linear scaling up to 8 GPUs', 'result'),
                ('Successfully processes 1M token contexts', 'result'),
                ('Network bandwidth becomes bottleneck beyond 8 GPUs', 'limitation'),
            ],
            'themes': ['Distributed Systems', 'KV Cache Management', 'Extreme Long Context']
        },
        {
            'title': 'Prompt Cache: Modular Attention Reuse for Low-Latency Inference',
            'authors': 'Gim et al.',
            'year': 2023,
            'venue': 'MLSys 2023',
            'abstract': 'We propose reusing KV cache across requests with shared prompt prefixes. Enables significant latency reduction for common prefixes.',
            'summary': 'Prompt Cache identifies that many requests share prompt prefixes (e.g., system prompts, few-shot examples). Implements KV cache reuse mechanism. Achieves 8x speedup for shared 1000-token prefixes. Particularly effective for chatbot and API scenarios with common system prompts.',
            'findings': [
                ('Many requests share common prompt prefixes', 'contribution'),
                ('KV cache reuse provides 8x speedup for shared prefixes', 'result'),
                ('Especially effective for chat and API applications', 'result'),
                ('Requires request routing to maximize sharing', 'limitation'),
            ],
            'themes': ['KV Cache Reuse', 'Prompt Optimization', 'Serving Systems']
        },
        {
            'title': 'GEAR: An Efficient KV Cache Compression Recipefor Near-Lossless Generative Inference of LLM',
            'authors': 'Kang et al.',
            'year': 2024,
            'venue': 'arXiv 2024',
            'abstract': 'We propose GEAR, combining quantization and sparsification for KV cache compression. Achieves 8-16x compression with negligible quality loss.',
            'summary': 'GEAR combines multiple compression techniques: low-bit quantization (INT4), structured sparsity, and adaptive rank reduction. Achieves 8-16x compression ratio. Near-lossless quality on most benchmarks. Implements hardware-efficient kernels for compressed cache access.',
            'findings': [
                ('Multi-faceted compression (quantization + sparsity + rank reduction) achieves best results', 'contribution'),
                ('8-16x compression with <1% quality degradation', 'result'),
                ('Custom kernels essential for realizing speedup', 'methodology'),
                ('Compression overhead impacts short sequences', 'limitation'),
            ],
            'themes': ['KV Cache Compression', 'Quantization', 'Sparsification']
        },
        {
            'title': 'Quest: Query-Aware Sparsity for Efficient Long-Context LLM Inference',
            'authors': 'Tang et al.',
            'year': 2024,
            'venue': 'ICML 2024',
            'abstract': 'We propose query-aware eviction that adapts to the current query at each decoding step. Different queries need different historical context.',
            'summary': 'Quest observes that different queries require different historical context. Implements query-aware attention pruning that adapts per decoding step. Uses lightweight attention score prediction. Outperforms static methods on tasks requiring selective attention. 3-5x cache reduction with maintained quality.',
            'findings': [
                ('Different queries benefit from different cache retention strategies', 'contribution'),
                ('Query-aware eviction outperforms static policies', 'result'),
                ('3-5x cache reduction with quality preservation', 'result'),
                ('Prediction overhead increases latency by 10-15%', 'limitation'),
            ],
            'themes': ['Query-Aware Eviction', 'Dynamic Optimization', 'Attention Pruning']
        },
        {
            'title': 'Landmarks: Efficient Attention for Long Contexts via Landmark Tokens',
            'authors': 'Mohtashami and Jaggi',
            'year': 2023,
            'venue': 'NeurIPS 2023',
            'abstract': 'We introduce landmark tokens that summarize context blocks. Attention operates on landmarks for distant context and full tokens for recent context.',
            'summary': 'Landmarks proposes hierarchical attention: full attention for recent K tokens, landmark-based attention for older tokens. Landmarks summarize fixed-size blocks. Achieves sub-linear memory complexity O(√n) instead of O(n). Works well for document understanding tasks.',
            'findings': [
                ('Hierarchical attention with landmarks reduces memory to O(√n)', 'contribution'),
                ('Effective for document-level tasks', 'result'),
                ('Requires special landmark token training', 'limitation'),
                ('May lose fine-grained information from distant context', 'limitation'),
            ],
            'themes': ['Hierarchical Attention', 'Token Compression', 'Long Context']
        },
        {
            'title': 'A Survey on Long Context Modeling for Large Language Models',
            'authors': 'Chen et al.',
            'year': 2024,
            'venue': 'arXiv 2024',
            'abstract': 'Comprehensive survey of techniques for handling long contexts in LLMs, including KV cache optimization, sparse attention, and compression methods.',
            'summary': 'Comprehensive survey covering: (1) KV cache management techniques, (2) Sparse attention patterns, (3) Memory-efficient architectures, (4) Compression methods. Provides taxonomy and empirical comparisons. Identifies key tradeoffs: memory vs quality vs latency. Highlights open challenges in scaling to million-token contexts.',
            'findings': [
                ('No single method dominates all scenarios - tradeoffs exist', 'contribution'),
                ('Combination of techniques often works best', 'contribution'),
                ('Million-token contexts remain challenging despite recent progress', 'limitation'),
                ('Need for standardized benchmarks for long-context evaluation', 'future_work'),
            ],
            'themes': ['Survey Paper', 'Long Context', 'KV Cache Overview']
        }
    ]

    print(f"\nAdding {len(papers_data)} papers on KV cache eviction and long-context LLM inference...\n")

    added_papers = []

    for i, paper_data in enumerate(papers_data, 1):
        print(f"[{i}/{len(papers_data)}] Processing: {paper_data['title'][:60]}...")

        # Create paper
        paper = Paper(
            title=paper_data['title'],
            authors=paper_data['authors'],
            year=paper_data['year'],
            venue=paper_data['venue'],
            abstract=paper_data['abstract'],
            brief_summary=paper_data['summary'][:250],
            detailed_summary=paper_data['summary']
        )

        # Add to database
        paper_id = kb.add_paper(paper)
        paper.id = paper_id

        # Add themes
        for theme_name in paper_data['themes']:
            theme = kb.get_theme_by_name(theme_name)
            if not theme:
                theme_obj = Theme(name=theme_name, description=f"Papers on {theme_name}")
                theme_id = kb.add_theme(theme_obj)
            else:
                theme_id = theme.id

            kb.link_paper_theme(paper_id, theme_id)

        # Add findings
        for finding_text, category in paper_data['findings']:
            finding = KeyFinding(
                paper_id=paper_id,
                finding_text=finding_text,
                category=category,
                importance_score=0.9 if category == 'contribution' else 0.7
            )
            kb.add_finding(finding)

        added_papers.append(paper)
        print(f"  ✓ Added (ID: {paper_id})")

    print(f"\n✓ Successfully added {len(added_papers)} papers\n")
    return added_papers


def main():
    """Generate literature review on KV cache eviction."""

    print("\n" + "="*80)
    print("Literature Review: KV Cache Eviction for Long-Context LLM Inference")
    print("="*80 + "\n")

    # Step 1: Initialize knowledge base
    print("Step 1: Initializing knowledge base...")
    db_path = Path("data/kv_cache_review.db")

    # Remove existing database for clean start
    if db_path.exists():
        db_path.unlink()

    kb = KnowledgeBase(str(db_path))
    kb.initialize_schema()
    print("✓ Knowledge base initialized\n")

    # Step 2: Add papers
    print("Step 2: Adding papers to knowledge base...")
    processor = PaperProcessor(kb, config={
        'summary_brief_tokens': 250,
        'summary_detailed_tokens': 1000,
    })

    papers = create_sample_papers_kv_cache(kb, processor)

    # Step 3: View statistics
    print("Step 3: Knowledge base statistics")
    stats = kb.get_statistics()
    print(f"  Papers: {stats['total_papers']}")
    print(f"  Themes: {stats['total_themes']}")
    print(f"  Findings: {stats['total_findings']}")
    print(f"  Year range: {stats['year_range']}\n")

    # Step 4: Show themes
    print("Step 4: Available themes")
    themes = kb.get_all_themes()
    for theme in themes:
        print(f"  - {theme.name}: {theme.paper_count} papers")
    print()

    # Step 5: Generate Markdown review
    print("Step 5: Generating Markdown literature review...")
    generator = ReviewGenerator(kb)

    review_md = generator.generate_review(
        theme="KV Cache Optimization",
        sections=['abstract', 'introduction', 'taxonomy', 'analysis', 'discussion', 'conclusion'],
        output_format="markdown",
        min_papers=5
    )

    # Save Markdown
    md_output_path = Path("data/outputs/kv_cache_review.md")
    md_output_path.parent.mkdir(parents=True, exist_ok=True)
    generator.save_review(review_md, md_output_path)

    print(f"✓ Markdown review saved to: {md_output_path}")
    print(f"  Length: {len(review_md)} characters")
    print(f"  Citations: {generator.citation_manager.get_citation_count()}\n")

    # Step 6: Generate LaTeX review
    print("Step 6: Generating LaTeX/Overleaf literature review...")

    # Reset citation manager for new review
    generator.citation_manager = CitationManager()

    review_latex = generator.generate_latex_review(
        theme="KV Cache Optimization",
        sections=['abstract', 'introduction', 'taxonomy', 'analysis', 'discussion', 'conclusion'],
        min_papers=5,
        author="Your Name"  # Change this to your name
    )

    # Save LaTeX
    latex_output_path = Path("data/outputs/kv_cache_review.tex")
    generator.save_review(review_latex, latex_output_path)

    print(f"✓ LaTeX review saved to: {latex_output_path}")
    print(f"  Length: {len(review_latex)} characters")
    print(f"  Citations: {generator.citation_manager.get_citation_count()}\n")

    # Step 7: Create Overleaf project
    print("Step 7: Creating Overleaf project structure...")
    overleaf_dir = Path("data/outputs/overleaf_project")
    generator.save_overleaf_project(review_latex, str(overleaf_dir))
    print()

    # Step 8: Summary
    print("="*80)
    print("✓ Literature Review Generated Successfully!")
    print("="*80)
    print(f"\nOutputs:")
    print(f"  1. Markdown: {md_output_path}")
    print(f"  2. LaTeX: {latex_output_path}")
    print(f"  3. Overleaf Project: {overleaf_dir}/")
    print(f"\nTo use in Overleaf:")
    print(f"  1. Zip the folder: {overleaf_dir}")
    print(f"  2. Go to Overleaf.com")
    print(f"  3. Click 'New Project' → 'Upload Project'")
    print(f"  4. Upload the zip file")
    print(f"  5. Compile with pdflatex")
    print(f"\nTo compile locally:")
    print(f"  cd {latex_output_path.parent}")
    print(f"  pdflatex kv_cache_review.tex")
    print(f"  pdflatex kv_cache_review.tex  # Run twice for references")
    print("\n" + "="*80 + "\n")

    # Cleanup
    kb.close()


if __name__ == "__main__":
    main()
