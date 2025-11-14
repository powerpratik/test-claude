# Quick Start Guide

Get started with the Literature Review Generator in 5 minutes!

## Prerequisites

```bash
# Python 3.8 or higher
python --version

# Install dependencies
pip install -r requirements.txt
```

## Installation

```bash
# 1. Navigate to project directory
cd /path/to/literature-review-app

# 2. Install dependencies
pip install pyyaml

# Optional: Install PDF support
pip install PyPDF2 pdfplumber
```

## Usage via Python Scripts

Since the application is designed as a library, you can use it programmatically:

### Example 1: Basic Usage

```python
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path('src')))

from knowledge_base.storage import KnowledgeBase
from knowledge_base.models import Paper, Theme

# Initialize database
kb = KnowledgeBase("data/knowledge_base.db")
kb.initialize_schema()

# Add a paper
paper = Paper(
    title="Deep Learning for NLP",
    authors="Smith et al.",
    year=2023,
    abstract="This paper explores deep learning for NLP tasks...",
    brief_summary="A comprehensive study of DL for NLP.",
    detailed_summary="This work presents novel approaches to NLP using deep learning..."
)

paper_id = kb.add_paper(paper)
print(f"Paper added with ID: {paper_id}")

# Add theme and link
theme = Theme(name="Deep Learning", description="DL papers")
theme_id = kb.add_theme(theme)
kb.link_paper_theme(paper_id, theme_id)

# Query papers
papers = kb.get_papers_by_theme(theme_id)
print(f"Found {len(papers)} papers in theme")

kb.close()
```

### Example 2: Complete Workflow

Create a file `my_review.py`:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path('src')))

from knowledge_base.storage import KnowledgeBase
from knowledge_base.models import Paper, Theme, KeyFinding, FindingCategory

# Initialize
db_path = "data/my_review.db"
kb = KnowledgeBase(db_path)
kb.initialize_schema()

# Add multiple papers
papers_data = [
    {
        'title': 'Attention Is All You Need',
        'authors': 'Vaswani et al.',
        'year': 2017,
        'theme': 'Transformers'
    },
    {
        'title': 'BERT: Pre-training of Deep Bidirectional Transformers',
        'authors': 'Devlin et al.',
        'year': 2019,
        'theme': 'Transformers'
    },
    {
        'title': 'GPT-3: Language Models are Few-Shot Learners',
        'authors': 'Brown et al.',
        'year': 2020,
        'theme': 'Transformers'
    }
]

# Add papers
for paper_data in papers_data:
    paper = Paper(
        title=paper_data['title'],
        authors=paper_data['authors'],
        year=paper_data['year'],
        brief_summary=f"A paper about {paper_data['theme']}.",
        detailed_summary=f"This influential paper contributes to {paper_data['theme']}."
    )

    paper_id = kb.add_paper(paper)

    # Add theme
    theme = kb.get_theme_by_name(paper_data['theme'])
    if not theme:
        theme_obj = Theme(name=paper_data['theme'])
        theme_id = kb.add_theme(theme_obj)
    else:
        theme_id = theme.id

    kb.link_paper_theme(paper_id, theme_id)

    print(f"✓ Added: {paper.title}")

# Show statistics
stats = kb.get_statistics()
print(f"\nDatabase Statistics:")
print(f"  Papers: {stats['total_papers']}")
print(f"  Themes: {stats['total_themes']}")

kb.close()
print("\nDone!")
```

Run it:
```bash
python my_review.py
```

## Verifying Installation

Run the test suite:

```bash
python test_basic.py
```

Expected output:
```
Testing Literature Review Generator...

1. Testing imports...
   ✓ Knowledge base imports successful

2. Testing database creation...
   ✓ Database initialized successfully

...

✓ All tests passed successfully!
```

## Next Steps

1. **Collect Papers**: Gather PDF or text files of academic papers
2. **Process Papers**: Use the `PaperProcessor` class to extract and summarize
3. **Query Knowledge Base**: Use `QueryEngine` to retrieve relevant papers
4. **Generate Review**: Use `ReviewGenerator` to create literature reviews

## Sample Workflow Script

Create `generate_review.py`:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path('src')))

from knowledge_base.storage import KnowledgeBase

# Your workflow here...
# See examples/ directory for more detailed examples

print("Literature Review Generator - Ready!")
print("See USAGE.md for detailed documentation")
```

## Troubleshooting

### Import Errors

If you see import errors, make sure you're adding `src` to your Python path:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'src'))
```

### Database Issues

If the database is locked or corrupted:

```python
# Delete and reinitialize
import os
if os.path.exists("data/knowledge_base.db"):
    os.remove("data/knowledge_base.db")

# Then reinitialize...
```

## Documentation

- **README.md**: Project overview
- **ARCHITECTURE.md**: System design and architecture
- **USAGE.md**: Comprehensive usage guide
- **examples/**: Example scripts and sample papers

## Support

For issues or questions:
1. Check the documentation files
2. Review example scripts in `examples/`
3. Run `python test_basic.py` to verify installation

## Features

✓ Multi-level summarization (brief and detailed)
✓ Theme-based organization
✓ Efficient context management (handles 30-50 papers)
✓ SQLite-based persistent storage
✓ ACM Computing Surveys quality templates
✓ Citation management
✓ Full-text search capabilities

Happy researching! 📚
