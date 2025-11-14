# Literature Review Generator

A sophisticated Python application for generating high-quality, ACM Computing Surveys-level literature reviews from academic papers. Designed to efficiently process 30-50 papers while maintaining context efficiency and producing comprehensive 20+ page reviews.

## Features

- **Efficient Knowledge Management**: SQLite-based knowledge base for persistent storage
- **Multi-level Summarization**: Brief and detailed summaries to optimize context usage
- **Theme-based Organization**: Automatic classification and grouping of papers
- **ACM Computing Surveys Quality**: Structured output following top-tier survey standards
- **Context-Aware**: Designed to work within 200k token limits
- **Modular Architecture**: Clean separation of concerns for maintainability
- **Incremental Processing**: Process papers one at a time, build knowledge progressively

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system design and implementation details.

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd literature-review-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### 1. Initialize the Knowledge Base

```bash
python src/main.py init
```

This creates the SQLite database with the proper schema.

### 2. Ingest Papers

```bash
# Ingest a single paper
python src/main.py ingest --file data/papers/paper1.pdf

# Ingest multiple papers from a directory
python src/main.py ingest --directory data/papers/

# Ingest with custom theme
python src/main.py ingest --file paper.pdf --theme "Machine Learning"
```

### 3. Query Knowledge Base

```bash
# List all papers
python src/main.py list

# Search by theme
python src/main.py search --theme "Deep Learning"

# Search by keyword
python src/main.py search --keyword "neural networks"

# View paper details
python src/main.py show --paper-id 1
```

### 4. Generate Literature Review

```bash
# Generate a full review
python src/main.py generate --theme "Deep Learning" --output data/outputs/review.md

# Generate specific sections
python src/main.py generate --theme "ML" --sections intro,taxonomy,analysis --output review.md

# Generate with custom parameters
python src/main.py generate \
  --theme "Computer Vision" \
  --min-papers 20 \
  --output review.md \
  --format markdown
```

## Usage Examples

### Complete Workflow

```bash
# 1. Initialize
python src/main.py init

# 2. Ingest papers
python src/main.py ingest --directory data/papers/

# 3. View themes
python src/main.py themes

# 4. Generate review
python src/main.py generate --theme "Natural Language Processing" --output nlp_review.md

# 5. View statistics
python src/main.py stats
```

### Working with Themes

```python
from src.knowledge_base.storage import KnowledgeBase
from src.retrieval.query_engine import QueryEngine

# Initialize
kb = KnowledgeBase("data/knowledge_base.db")
query_engine = QueryEngine(kb)

# Get papers by theme
papers = query_engine.get_papers_by_theme("Machine Learning")

# Get papers by year range
recent_papers = query_engine.get_papers_by_year_range(2020, 2024)

# Get papers by multiple criteria
papers = query_engine.query(
    themes=["Deep Learning", "Computer Vision"],
    year_min=2020,
    keywords=["attention mechanism"]
)
```

### Generating Custom Reviews

```python
from src.generation.review_generator import ReviewGenerator

# Initialize generator
generator = ReviewGenerator("data/knowledge_base.db")

# Generate review
review = generator.generate_review(
    theme="Deep Learning",
    sections=["introduction", "taxonomy", "analysis", "discussion", "conclusion"],
    min_papers=25,
    output_format="markdown"
)

# Save review
with open("data/outputs/custom_review.md", "w") as f:
    f.write(review)
```

## Project Structure

```
literature-review-app/
├── src/                      # Source code
│   ├── main.py              # CLI entry point
│   ├── config.py            # Configuration
│   ├── knowledge_base/      # Database operations
│   ├── processors/          # Paper processing
│   ├── retrieval/           # Query engine
│   └── generation/          # Review generation
├── data/                    # Data directory
│   ├── papers/             # Raw papers (PDFs)
│   ├── knowledge_base.db   # SQLite database
│   └── outputs/            # Generated reviews
├── tests/                   # Unit tests
├── config.yaml             # Configuration file
└── requirements.txt        # Dependencies
```

## Configuration

Edit `config.yaml` to customize:

```yaml
database:
  path: "data/knowledge_base.db"

processing:
  summary_brief_tokens: 250
  summary_detailed_tokens: 1000
  batch_size: 5

generation:
  default_format: "markdown"
  citation_style: "ACM"
  min_papers_per_theme: 10

context:
  max_tokens: 200000
  buffer_tokens: 10000
```

## Advanced Features

### Custom Summarization

Override the default summarizer with custom logic:

```python
from src.processors.summarizer import BaseSummarizer

class CustomSummarizer(BaseSummarizer):
    def summarize(self, text, max_tokens):
        # Your custom logic
        return summary

# Use in processor
processor.set_summarizer(CustomSummarizer())
```

### Export Formats

Generate reviews in multiple formats:

```bash
# Markdown (default)
python src/main.py generate --output review.md --format markdown

# LaTeX
python src/main.py generate --output review.tex --format latex

# HTML
python src/main.py generate --output review.html --format html
```

### Incremental Updates

Add new papers without regenerating the entire knowledge base:

```bash
# Add new papers
python src/main.py ingest --file new_paper.pdf

# Regenerate only affected sections
python src/main.py generate --theme "ML" --incremental --output review.md
```

## Context Management

The application is designed to work within a 200k token limit:

- **Brief summaries**: ~250 tokens per paper
- **Detailed summaries**: ~1000 tokens per paper
- **For 50 papers**: ~50,000 tokens total for detailed summaries
- **Remaining**: ~150,000 tokens for generation and processing

The system uses:
1. **Lazy loading**: Load paper details only when needed
2. **Hierarchical summaries**: Start brief, drill down as needed
3. **Database queries**: Use SQL instead of in-context search
4. **Section-wise generation**: Generate review section by section

## Quality Standards

Generated reviews aim for ACM Computing Surveys quality:

- **Comprehensive coverage**: All relevant papers included
- **Clear taxonomy**: Papers organized by themes and approaches
- **Critical analysis**: Strengths, limitations, comparisons
- **Proper citations**: All claims properly attributed
- **Future directions**: Identification of open problems
- **Professional structure**: Introduction, background, taxonomy, analysis, discussion, conclusion

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test module
python -m pytest tests/test_processors.py

# Run with coverage
python -m pytest --cov=src tests/
```

## Troubleshooting

### Common Issues

**Database locked error**:
```bash
# Reset the database
python src/main.py init --reset
```

**PDF parsing errors**:
```bash
# Try with text extraction only
python src/main.py ingest --file paper.pdf --text-only
```

**Context limit exceeded**:
```bash
# Reduce number of papers or use brief summaries only
python src/main.py generate --theme "ML" --summary-level brief
```

## Contributing

1. Follow the architecture guidelines in ARCHITECTURE.md
2. Write tests for new features
3. Update documentation
4. Follow PEP 8 style guide

## License

MIT License

## Citation

If you use this tool in your research, please cite:

```bibtex
@software{literature_review_generator,
  title={Literature Review Generator},
  author={Your Name},
  year={2024},
  url={https://github.com/yourusername/literature-review-app}
}
```

## Contact

For questions and support, please open an issue on GitHub.
