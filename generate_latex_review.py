#!/usr/bin/env python3
"""
Generate LaTeX literature review for Overleaf.

This script generates a complete LaTeX review that can be uploaded to Overleaf.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, 'src')

from knowledge_base.storage import KnowledgeBase
from generation.review_generator import ReviewGenerator

def main():
    print("\n" + "="*80)
    print("Generating LaTeX Literature Review for Overleaf")
    print("="*80 + "\n")

    # Check if database exists
    db_path = Path("data/kv_cache_review.db")
    if not db_path.exists():
        print("✗ Database not found!")
        print("  Run: bash generate_kv_cache_review.sh")
        return

    # Initialize
    print("Step 1: Loading knowledge base...")
    kb = KnowledgeBase(str(db_path))

    # Check paper count
    stats = kb.get_statistics()
    print(f"  Found {stats['total_papers']} papers\n")

    if stats['total_papers'] < 3:
        print("✗ Not enough papers (need at least 3)")
        kb.close()
        return

    # Generate review
    print("Step 2: Generating LaTeX review...")
    generator = ReviewGenerator(kb)

    try:
        # Generate LaTeX
        review_latex = generator.generate_latex_review(
            theme="KV Cache Optimization",
            sections=['abstract', 'introduction', 'analysis', 'conclusion'],
            min_papers=3,
            author="Literature Review Generator"  # Change to your name
        )

        # Create output directory
        output_dir = Path("data/outputs")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Save LaTeX file
        latex_path = output_dir / "kv_cache_review.tex"
        with open(latex_path, 'w', encoding='utf-8') as f:
            f.write(review_latex)

        print(f"✓ LaTeX file saved: {latex_path}")
        print(f"  Size: {len(review_latex)} characters")
        print(f"  Citations: {generator.citation_manager.get_citation_count()}\n")

        # Create Overleaf project
        print("Step 3: Creating Overleaf project...")
        overleaf_dir = output_dir / "overleaf_project"
        generator.save_overleaf_project(review_latex, str(overleaf_dir))
        print()

        # Instructions
        print("="*80)
        print("✓ LaTeX Review Generated Successfully!")
        print("="*80)
        print(f"\nFiles created:")
        print(f"  1. LaTeX source: {latex_path}")
        print(f"  2. Overleaf project: {overleaf_dir}/")
        print(f"\nTo use in Overleaf:")
        print(f"  1. Zip the project folder:")
        print(f"     cd {output_dir}")
        print(f"     zip -r kv_cache_review.zip overleaf_project/")
        print(f"  2. Go to Overleaf.com")
        print(f"  3. Click 'New Project' → 'Upload Project'")
        print(f"  4. Upload kv_cache_review.zip")
        print(f"  5. Click 'Recompile' to generate PDF")
        print(f"\nTo compile locally:")
        print(f"  cd {output_dir}")
        print(f"  pdflatex kv_cache_review.tex")
        print(f"  pdflatex kv_cache_review.tex  # Run twice for references")
        print("\n" + "="*80 + "\n")

    except Exception as e:
        print(f"✗ Error generating review: {e}")
        import traceback
        traceback.print_exc()

    finally:
        kb.close()


if __name__ == "__main__":
    main()
