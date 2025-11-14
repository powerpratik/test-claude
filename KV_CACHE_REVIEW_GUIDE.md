# Complete Guide: Literature Review for KV Cache Eviction in LLM Inference

## Your Use Case

**Topic**: KV Cache Eviction Algorithms for Large-Scale LLM Inference with Long Context

**Goal**: Generate a comprehensive 20+ page literature review surveying recent papers on:
- KV cache optimization techniques
- Eviction policies and strategies
- Memory management for long-context inference
- Performance tradeoffs and benchmarks

## Quick Start (5 Steps)

### Step 1: Run the Example Script

```bash
python examples/kv_cache_review_example.py
```

**What it does**:
- Creates database with 12 sample papers on KV cache topics
- Generates both Markdown and LaTeX reviews
- Creates Overleaf-ready project structure

**Output**:
```
data/outputs/kv_cache_review.md          # Markdown version
data/outputs/kv_cache_review.tex         # LaTeX source
data/outputs/overleaf_project/           # Overleaf-ready folder
```

### Step 2: Upload to Overleaf

1. Zip the Overleaf project:
   ```bash
   cd data/outputs
   zip -r kv_cache_review.zip overleaf_project/
   ```

2. Go to [Overleaf.com](https://www.overleaf.com)

3. Click **"New Project"** → **"Upload Project"**

4. Upload `kv_cache_review.zip`

5. Click **"Recompile"** → Your PDF is ready!

### Step 3: Customize with Real Papers

Replace sample papers with real ones from:
- **ACM Digital Library**: Recent SOSP, OSDI, MLSys papers
- **arXiv**: Search "KV cache LLM" or "long context inference"
- **Conference proceedings**: NeurIPS, ICML, ICLR

### Step 4: Add Your Papers

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path('src')))

from knowledge_base.storage import KnowledgeBase
from knowledge_base.models import Paper, Theme

# Initialize
kb = KnowledgeBase("data/kv_cache_review.db")

# Add a paper
paper = Paper(
    title="Your Paper Title",
    authors="Author et al.",
    year=2024,
    venue="Conference Name",
    abstract="Paper abstract...",
    brief_summary="Brief summary in 250 tokens...",
    detailed_summary="Detailed summary in 1000 tokens..."
)

paper_id = kb.add_paper(paper)

# Link to theme
theme = kb.get_theme_by_name("KV Cache Optimization")
if theme:
    kb.link_paper_theme(paper_id, theme.id)

kb.close()
```

### Step 5: Regenerate Review

```python
from generation.review_generator import ReviewGenerator

kb = KnowledgeBase("data/kv_cache_review.db")
generator = ReviewGenerator(kb)

# Generate LaTeX review
review_latex = generator.generate_latex_review(
    theme="KV Cache Optimization",
    min_papers=10,
    author="Your Name"  # ← Put your name here
)

# Save
generator.save_review(review_latex, "data/outputs/my_review.tex")
generator.save_overleaf_project(review_latex, "data/outputs/my_overleaf")

kb.close()
```

## Detailed Workflow for Your Topic

### Phase 1: Paper Collection (30-50 papers)

**Recommended papers to include**:

1. **KV Cache Eviction**:
   - H2O (Zhang et al., NeurIPS 2023)
   - StreamingLLM (Xiao et al., ICLR 2024)
   - Scissorhands (Liu et al., 2023)
   - Quest (Tang et al., ICML 2024)

2. **Memory Management**:
   - PagedAttention/vLLM (Kwon et al., SOSP 2023)
   - FastGen (Chen et al., MLSys 2024)
   - Infinite-LLM (Li et al., OSDI 2024)

3. **Compression Techniques**:
   - GEAR (Kang et al., 2024)
   - Model-adaptive compression (Wang et al., ICLR 2024)

4. **Long Context**:
   - Survey on long context (Chen et al., 2024)
   - Landmarks (Mohtashami et al., NeurIPS 2023)

5. **Serving Systems**:
   - Prompt Cache (Gim et al., MLSys 2023)

**How to find papers**:
```bash
# arXiv search
https://arxiv.org/search/?query=KV+cache+LLM&searchtype=all

# ACM DL search
https://dl.acm.org/action/doSearch?AllField=KV+cache+language+model

# Google Scholar
scholar.google.com → "KV cache eviction large language models"
```

### Phase 2: Paper Processing

**Option A: Manual Entry** (Recommended for quality)

Create `add_my_papers.py`:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path('src')))

from knowledge_base.storage import KnowledgeBase
from knowledge_base.models import Paper, Theme, KeyFinding

kb = KnowledgeBase("data/my_kv_cache_review.db")
kb.initialize_schema()

# For each paper, add:
papers = [
    {
        'title': 'H2O: Heavy-Hitter Oracle for Efficient Generative Inference',
        'authors': 'Zhang, Sheng, et al.',
        'year': 2023,
        'venue': 'NeurIPS 2023',
        'themes': ['KV Cache Eviction', 'Attention Optimization'],
        'abstract': '...',
        'summary': '...',
        'key_findings': [
            'Discovered heavy-hitter phenomenon in attention patterns',
            'Achieves 20-30% cache size with maintained quality',
        ]
    },
    # Add more papers...
]

for paper_data in papers:
    paper = Paper(
        title=paper_data['title'],
        authors=paper_data['authors'],
        year=paper_data['year'],
        venue=paper_data['venue'],
        abstract=paper_data['abstract'],
        brief_summary=paper_data['summary'][:250],
        detailed_summary=paper_data['summary']
    )

    paper_id = kb.add_paper(paper)

    # Add themes
    for theme_name in paper_data['themes']:
        theme = kb.get_theme_by_name(theme_name)
        if not theme:
            theme_obj = Theme(name=theme_name)
            theme_id = kb.add_theme(theme_obj)
        else:
            theme_id = theme.id
        kb.link_paper_theme(paper_id, theme_id)

    # Add findings
    for finding_text in paper_data['key_findings']:
        finding = KeyFinding(
            paper_id=paper_id,
            finding_text=finding_text,
            category='contribution',
            importance_score=0.9
        )
        kb.add_finding(finding)

kb.close()
```

**Option B: PDF Processing** (If you have PDFs)

```python
from processors.paper_processor import PaperProcessor

kb = KnowledgeBase("data/my_kv_cache_review.db")
processor = PaperProcessor(kb)

# Process PDF
paper = processor.process_paper(
    "path/to/paper.pdf",
    themes=["KV Cache Optimization"]
)

kb.close()
```

### Phase 3: Generate Review

**Generate both Markdown and LaTeX**:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path('src')))

from knowledge_base.storage import KnowledgeBase
from generation.review_generator import ReviewGenerator

kb = KnowledgeBase("data/my_kv_cache_review.db")
generator = ReviewGenerator(kb)

# Markdown version
review_md = generator.generate_review(
    theme="KV Cache Optimization",
    output_format="markdown",
    min_papers=20
)
generator.save_review(review_md, "data/outputs/review.md")

# LaTeX version for Overleaf
review_latex = generator.generate_latex_review(
    theme="KV Cache Optimization",
    min_papers=20,
    author="Your Name"
)
generator.save_review(review_latex, "data/outputs/review.tex")

# Create Overleaf project
generator.save_overleaf_project(
    review_latex,
    "data/outputs/overleaf_kv_cache"
)

print(f"✓ Generated review with {generator.citation_manager.get_citation_count()} papers")

kb.close()
```

### Phase 4: Compile to PDF

**Option 1: Overleaf (Easiest)**
1. Zip and upload (see Step 2 above)
2. Click "Recompile"
3. Download PDF

**Option 2: Local LaTeX**
```bash
cd data/outputs
pdflatex review.tex
pdflatex review.tex  # Run twice for references
# Output: review.pdf
```

**Option 3: Docker**
```bash
docker run --rm -v $(pwd):/data tianon/latex pdflatex /data/review.tex
```

## Review Structure (ACM Style)

Your generated review will have:

1. **Abstract** (250 words)
   - Scope and coverage
   - Key findings
   - Main themes

2. **Introduction** (2-3 pages)
   - Motivation for KV cache research
   - Challenges in long-context inference
   - Survey organization

3. **Background** (1-2 pages)
   - Attention mechanism basics
   - KV cache fundamentals
   - Memory bottlenecks

4. **Taxonomy** (2-3 pages)
   - Classification of approaches:
     * Eviction-based methods
     * Compression-based methods
     * Offloading-based methods
     * Hybrid approaches

5. **Detailed Analysis** (12-15 pages)
   - **Section 4.1**: Eviction Policies
     * H2O, StreamingLLM, Quest
     * Static vs dynamic policies
   - **Section 4.2**: Compression Techniques
     * Quantization, sparsification
     * GEAR, model-adaptive
   - **Section 4.3**: System-level Optimizations
     * PagedAttention, distributed cache
   - **Section 4.4**: Comparative Analysis
     * Performance tradeoffs
     * Benchmark results

6. **Discussion** (2-3 pages)
   - Trends and patterns
   - Tradeoffs (memory vs quality vs latency)
   - Open challenges

7. **Future Directions** (1-2 pages)
   - Ultra-long contexts (1M+ tokens)
   - Hardware-aware optimization
   - Learned eviction policies

8. **Conclusion** (1 page)

9. **References**
   - All 30-50 papers cited

## Customization Tips

### Adjust Token Limits

Edit `config.yaml`:
```yaml
processing:
  summary_brief_tokens: 300  # Increase for more detail
  summary_detailed_tokens: 1200

generation:
  min_papers_for_review: 25  # Require more papers
```

### Focus on Specific Themes

```python
# Generate review for specific sub-theme
review = generator.generate_review(
    theme="KV Cache Eviction",  # More specific
    min_papers=15
)
```

### Add Custom Sections

```python
review = generator.generate_review(
    theme="KV Cache Optimization",
    sections=['abstract', 'introduction', 'taxonomy',
              'analysis', 'benchmarks', 'discussion', 'conclusion']
)
```

### Modify LaTeX Style

Edit `src/generation/latex_formatter.py`:
- Change document class
- Add packages
- Modify formatting

## Expected Output Quality

**For your KV cache topic, expect**:
- **20-25 pages** with 30 papers
- **30-40 pages** with 50 papers
- **30-50 citations**
- **ACM Computing Surveys quality**

**Sections include**:
- Comprehensive taxonomy
- Detailed paper analysis
- Comparison tables
- Performance tradeoffs
- Open challenges
- Future directions

## Common Issues & Solutions

### Issue 1: Not Enough Papers
```python
# Lower threshold
review = generator.generate_review(..., min_papers=10)
```

### Issue 2: LaTeX Compilation Errors
- Check for special characters in paper titles
- Ensure all citations are valid
- Try compiling twice for references

### Issue 3: Review Too Short
- Add more papers
- Use detailed summaries
- Include all sections

### Issue 4: Theme Not Found
```bash
# List available themes
python -c "
import sys; sys.path.insert(0, 'src')
from knowledge_base.storage import KnowledgeBase
kb = KnowledgeBase('data/kv_cache_review.db')
themes = kb.get_all_themes()
for t in themes: print(f'{t.name}: {t.paper_count} papers')
"
```

## Next Steps

1. ✅ Run the example: `python examples/kv_cache_review_example.py`
2. ✅ Upload to Overleaf and compile
3. ✅ Review the generated content
4. ✅ Collect your actual papers
5. ✅ Add them to the database
6. ✅ Regenerate with real papers
7. ✅ Refine and customize
8. ✅ Export final PDF

## Resources

- **Example Database**: `data/kv_cache_review.db` (12 sample papers)
- **Example Script**: `examples/kv_cache_review_example.py`
- **Documentation**: `USAGE.md`, `ARCHITECTURE.md`
- **Templates**: `src/generation/templates.py`
- **LaTeX Formatter**: `src/generation/latex_formatter.py`

## Contact & Support

For issues:
1. Check documentation files
2. Review example scripts
3. Run `python test_basic.py` to verify installation

**Happy reviewing! Your KV cache literature review is just a few commands away! 🚀**
