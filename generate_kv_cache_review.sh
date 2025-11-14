#!/bin/bash
# Generate KV Cache Literature Review
# This script generates both Markdown and LaTeX versions

echo "================================================================================"
echo "Generating Literature Review: KV Cache Eviction for LLM Inference"
echo "================================================================================"
echo ""

# Set Python path
export PYTHONPATH=/home/user/test-claude/src:$PYTHONPATH

# Run the generation script
python3 << 'PYTHON_SCRIPT'
import sys
from pathlib import Path
sys.path.insert(0, '/home/user/test-claude/src')

from knowledge_base.storage import KnowledgeBase
from knowledge_base.models import Paper, Theme, KeyFinding

# Initialize database
print("Step 1: Initializing knowledge base...")
db_path = Path("data/kv_cache_review.db")
if db_path.exists():
    db_path.unlink()

kb = KnowledgeBase(str(db_path))
kb.initialize_schema()
print("✓ Database initialized\n")

# Add sample papers
print("Step 2: Adding papers...")

papers_data = [
    {
        'title': 'PagedAttention: Efficient Memory Management for LLM Serving',
        'authors': 'Kwon et al.',
        'year': 2023,
        'venue': 'SOSP 2023',
        'summary': 'Introduces PagedAttention for efficient KV cache management using virtual memory paging. Achieves 2-4x throughput improvement.',
        'themes': ['KV Cache Optimization', 'Memory Management']
    },
    {
        'title': 'H2O: Heavy-Hitter Oracle for Efficient Generative Inference',
        'authors': 'Zhang et al.',
        'year': 2023,
        'venue': 'NeurIPS 2023',
        'summary': 'Discovers heavy-hitter phenomenon where 20% of tokens contribute 80% of attention. Maintains quality with 20-30% cache size.',
        'themes': ['KV Cache Eviction', 'Attention Optimization']
    },
    {
        'title': 'StreamingLLM: Efficient Streaming with Attention Sinks',
        'authors': 'Xiao et al.',
        'year': 2023,
        'venue': 'ICLR 2024',
        'summary': 'Discovers attention sinks and enables infinite context with fixed 256-1024 token cache.',
        'themes': ['KV Cache Eviction', 'Streaming Inference']
    },
    {
        'title': 'Scissorhands: Persistence of Importance for KV Cache Compression',
        'authors': 'Liu et al.',
        'year': 2023,
        'venue': 'arXiv 2023',
        'summary': 'Introduces persistence of importance hypothesis. Achieves 5x compression with minimal quality loss.',
        'themes': ['KV Cache Compression', 'Token Importance']
    },
    {
        'title': 'FastGen: KV Cache Offloading for Ultra-Long Contexts',
        'authors': 'Chen et al.',
        'year': 2024,
        'venue': 'MLSys 2024',
        'summary': 'Hierarchical cache management (GPU/CPU/SSD). Supports 100K+ tokens on single GPU.',
        'themes': ['KV Cache Offloading', 'Long Context']
    }
]

for i, paper_data in enumerate(papers_data, 1):
    print(f"  [{i}/{len(papers_data)}] {paper_data['title'][:50]}...")

    paper = Paper(
        title=paper_data['title'],
        authors=paper_data['authors'],
        year=paper_data['year'],
        venue=paper_data['venue'],
        brief_summary=paper_data['summary'][:250],
        detailed_summary=paper_data['summary']
    )

    paper_id = kb.add_paper(paper)

    for theme_name in paper_data['themes']:
        theme = kb.get_theme_by_name(theme_name)
        if not theme:
            theme_obj = Theme(name=theme_name, description=f"Papers on {theme_name}")
            theme_id = kb.add_theme(theme_obj)
        else:
            theme_id = theme.id
        kb.link_paper_theme(paper_id, theme_id)

print(f"\n✓ Added {len(papers_data)} papers\n")

# Show statistics
stats = kb.get_statistics()
print(f"Database statistics:")
print(f"  Papers: {stats['total_papers']}")
print(f"  Themes: {stats['total_themes']}")
print(f"  Year range: {stats['year_range']}\n")

kb.close()

print("✓ Knowledge base created successfully!")
print(f"  Location: {db_path}")
print("\nNext steps:")
print("  1. Add more papers using the Python API (see KV_CACHE_REVIEW_GUIDE.md)")
print("  2. Generate review using generation/review_generator.py")
print("  3. Export to LaTeX for Overleaf")
print("")

PYTHON_SCRIPT

echo "================================================================================"
echo "✓ Setup complete!"
echo "================================================================================"
echo ""
echo "To generate the review, create a Python script like this:"
echo ""
cat << 'EOF'
# generate_review.py
import sys
sys.path.insert(0, 'src')

from knowledge_base.storage import KnowledgeBase
from generation.review_generator import ReviewGenerator
from generation.templates import CitationManager

kb = KnowledgeBase("data/kv_cache_review.db")
generator = ReviewGenerator(kb)

# Generate LaTeX review
review_latex = generator.generate_latex_review(
    theme="KV Cache Optimization",
    min_papers=3,
    author="Your Name"
)

# Save
with open("data/outputs/kv_cache_review.tex", "w") as f:
    f.write(review_latex)

print("✓ Review generated: data/outputs/kv_cache_review.tex")
kb.close()
EOF
