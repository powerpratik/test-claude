# Literature Review Application - Architecture

## Overview

A sophisticated literature review generation system designed to create ACM Computing Surveys quality reviews from 30-50 academic papers while maintaining efficient context management (< 200k tokens).

## Design Principles

1. **Separation of Concerns**: Distinct modules for storage, processing, retrieval, and generation
2. **Context Efficiency**: Never load full papers into context; work with structured summaries
3. **Persistent Knowledge**: SQLite database for structured data, filesystem for documents
4. **Incremental Processing**: Process papers individually, build knowledge base progressively
5. **Efficient Retrieval**: Query-based system to load only relevant information when needed
6. **Modularity**: Each component can be tested and extended independently

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                         │
│                      (main.py)                               │
└────────────┬────────────────────────────────────────────────┘
             │
             ├──────────────────┬──────────────┬──────────────┐
             │                  │              │              │
┌────────────▼────────┐  ┌──────▼──────┐  ┌───▼──────┐  ┌────▼─────┐
│  Paper Processor    │  │  Knowledge  │  │Retrieval │  │ Review   │
│    Module           │  │    Base     │  │  Engine  │  │Generator │
│                     │  │   Module    │  │          │  │          │
│ - PDF Parser        │  │             │  │- Query   │  │- Template│
│ - Text Extractor    │──│- SQLite DB  │──│  System  │──│  Engine  │
│ - Summarizer        │  │- Schema Mgmt│  │- Filters │  │- Section │
│ - Metadata Extract  │  │- CRUD Ops   │  │- Themes  │  │  Builder │
└─────────────────────┘  └─────────────┘  └──────────┘  └──────────┘
```

## Component Details

### 1. Knowledge Base Module (`knowledge_base/`)

**Purpose**: Persistent storage and management of paper data

**Components**:
- `storage.py`: Database operations (CRUD)
- `schema.py`: Data models and database schema
- `models.py`: Python classes representing entities

**Database Schema**:

```sql
Papers:
- id (PRIMARY KEY)
- title, authors, year, venue, doi
- abstract, full_text_path
- brief_summary (250 tokens)
- detailed_summary (1000 tokens)
- created_at, updated_at

Sections:
- id (PRIMARY KEY)
- paper_id (FOREIGN KEY)
- section_type (introduction, methodology, results, etc.)
- content, summary
- order_index

KeyFindings:
- id (PRIMARY KEY)
- paper_id (FOREIGN KEY)
- finding_text
- category (contribution, limitation, future_work)
- importance_score

Themes:
- id (PRIMARY KEY)
- name, description

PaperThemes (junction table):
- paper_id, theme_id
- relevance_score

Citations:
- id (PRIMARY KEY)
- source_paper_id, cited_paper_id
- context
```

**Context Management**:
- Brief summaries: ~250 tokens/paper (for overview)
- Detailed summaries: ~1000 tokens/paper (for deep dives)
- Total for 50 papers: 12,500 - 50,000 tokens (manageable)

### 2. Paper Processor Module (`processors/`)

**Purpose**: Extract, parse, and summarize papers

**Components**:
- `pdf_parser.py`: Extract text from PDFs
- `text_processor.py`: Clean and structure text
- `summarizer.py`: Generate multi-level summaries
- `metadata_extractor.py`: Extract paper metadata

**Processing Pipeline**:
1. Parse PDF/text → Extract raw content
2. Identify structure → Section headers, paragraphs
3. Extract metadata → Title, authors, year, abstract
4. Generate summaries → Brief (250 tok), Detailed (1000 tok)
5. Extract findings → Contributions, limitations, future work
6. Identify themes → Classify paper topics
7. Store in KB → Persist all structured data

**Summary Levels**:
- **Brief** (250 tokens): Abstract + key contributions
- **Detailed** (1000 tokens): Full overview including methodology, results
- **Section-specific**: Individual section summaries for targeted retrieval

### 3. Retrieval Engine (`retrieval/`)

**Purpose**: Efficiently query knowledge base

**Components**:
- `query_engine.py`: Main query interface
- `filters.py`: Filtering utilities
- `ranker.py`: Relevance ranking

**Query Types**:
- Theme-based: Get all papers in a theme
- Keyword search: Full-text search in summaries
- Year/venue filtering: Temporal analysis
- Citation network: Find related papers
- Methodology-based: Papers using specific methods

**Context Optimization**:
- Load only brief summaries initially
- Fetch detailed summaries for relevant papers only
- Retrieve specific sections when writing particular review sections

### 4. Review Generator (`generation/`)

**Purpose**: Generate high-quality literature reviews

**Components**:
- `review_generator.py`: Main generation orchestrator
- `templates.py`: ACM Computing Surveys structure templates
- `section_builders.py`: Individual section generators
- `citation_manager.py`: Citation formatting

**Review Structure** (ACM Computing Surveys style):

1. **Abstract** (200-250 words)
2. **Introduction** (2-3 pages)
   - Motivation and scope
   - Research questions
   - Organization of review
3. **Background** (1-2 pages)
   - Key concepts and definitions
   - Historical context
4. **Taxonomy/Classification** (2-3 pages)
   - Organize papers by themes
   - Visual taxonomy
5. **Detailed Analysis** (12-15 pages)
   - Theme-by-theme analysis
   - Compare and contrast approaches
   - Strengths and limitations
6. **Discussion** (2-3 pages)
   - Synthesis of findings
   - Open challenges
   - Future research directions
7. **Conclusion** (1 page)
8. **References**

**Generation Strategy**:
- Generate section by section
- Load relevant papers for each section
- Progressive refinement
- Maintain narrative coherence

### 5. Context Management Strategy

**Token Budget**: 200,000 tokens

**Allocation**:
- System prompts: ~10,000 tokens
- Knowledge base summaries: ~30,000 tokens (50 papers × 600 avg)
- Active working set: ~50,000 tokens (detailed info for 10-15 papers)
- Generation buffer: ~100,000 tokens (review text + refinement)
- Safety margin: ~10,000 tokens

**Techniques**:
1. **Lazy Loading**: Load paper details only when needed
2. **Batch Processing**: Process papers in groups, commit to DB
3. **Selective Retrieval**: Query for specific information
4. **Hierarchical Summaries**: Start with brief, drill down as needed
5. **Section-wise Generation**: Generate review section by section
6. **Database as Memory**: Use SQL queries instead of in-context search

## Data Flow

### Phase 1: Paper Ingestion
```
PDF Files → Parser → Text Extraction → Metadata Extraction
                                    ↓
                              Summarization
                                    ↓
                         Theme Classification
                                    ↓
                            Knowledge Base
```

### Phase 2: Review Generation
```
User Query → Retrieve Themes → Query Papers by Theme
                                    ↓
                         Load Relevant Summaries
                                    ↓
                         Generate Section Draft
                                    ↓
                         Refine and Cite
                                    ↓
                         Output Review Section
```

## File Structure

```
literature-review-app/
├── src/
│   ├── __init__.py
│   ├── main.py                          # CLI entry point
│   ├── config.py                        # Configuration management
│   │
│   ├── knowledge_base/
│   │   ├── __init__.py
│   │   ├── storage.py                   # Database operations
│   │   ├── schema.py                    # Database schema
│   │   └── models.py                    # Data models
│   │
│   ├── processors/
│   │   ├── __init__.py
│   │   ├── pdf_parser.py                # PDF parsing
│   │   ├── text_processor.py            # Text cleaning
│   │   ├── summarizer.py                # Summary generation
│   │   └── metadata_extractor.py        # Metadata extraction
│   │
│   ├── retrieval/
│   │   ├── __init__.py
│   │   ├── query_engine.py              # Query interface
│   │   ├── filters.py                   # Filtering utilities
│   │   └── ranker.py                    # Relevance ranking
│   │
│   └── generation/
│       ├── __init__.py
│       ├── review_generator.py          # Main generator
│       ├── templates.py                 # Review templates
│       ├── section_builders.py          # Section generators
│       └── citation_manager.py          # Citation handling
│
├── data/
│   ├── papers/                          # Raw paper files
│   ├── knowledge_base.db                # SQLite database
│   └── outputs/                         # Generated reviews
│
├── tests/
│   ├── test_processors.py
│   ├── test_retrieval.py
│   └── test_generation.py
│
├── config.yaml                          # Application configuration
├── requirements.txt                     # Python dependencies
├── README.md                            # Usage documentation
├── ARCHITECTURE.md                      # This file
└── .gitignore
```

## Scalability and Performance

- **Database Indexing**: Index on themes, years, keywords for fast queries
- **Caching**: Cache frequently accessed summaries
- **Batch Processing**: Process multiple papers in parallel (when ingesting)
- **Incremental Updates**: Add papers without regenerating entire review
- **Memory Efficiency**: Stream large texts, don't load entirely into memory

## Quality Assurance

1. **Multi-level Summaries**: Preserve important details at different granularities
2. **Citation Tracking**: Maintain source information for all claims
3. **Theme Coherence**: Ensure papers are grouped logically
4. **Narrative Flow**: Template-based generation ensures structure
5. **Validation**: Check for completeness, citation accuracy, coherence

## Extension Points

- **Custom Summarizers**: Plugin architecture for different summarization approaches
- **Multiple Output Formats**: LaTeX, Markdown, HTML, PDF
- **Interactive Refinement**: User feedback to improve specific sections
- **Automated Paper Fetching**: Integration with ACM DL, arXiv APIs
- **Visualization**: Generate taxonomy diagrams, citation networks
- **Collaborative Features**: Multi-user reviews, version control

## Security and Privacy

- Local storage only (no external API calls for sensitive papers)
- Configurable data retention policies
- Access control for knowledge base (if needed)
- Audit trail for review generation decisions
