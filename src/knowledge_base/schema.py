"""
Database schema definitions for the knowledge base.
"""

# SQL schema for creating tables

CREATE_PAPERS_TABLE = """
CREATE TABLE IF NOT EXISTS papers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    authors TEXT,
    year INTEGER,
    venue TEXT,
    doi TEXT,
    abstract TEXT,
    full_text_path TEXT,
    brief_summary TEXT,
    detailed_summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_SECTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id INTEGER NOT NULL,
    section_type TEXT NOT NULL,
    title TEXT,
    content TEXT,
    summary TEXT,
    order_index INTEGER DEFAULT 0,
    FOREIGN KEY (paper_id) REFERENCES papers(id) ON DELETE CASCADE
);
"""

CREATE_KEY_FINDINGS_TABLE = """
CREATE TABLE IF NOT EXISTS key_findings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id INTEGER NOT NULL,
    finding_text TEXT NOT NULL,
    category TEXT NOT NULL,
    importance_score REAL DEFAULT 0.5,
    FOREIGN KEY (paper_id) REFERENCES papers(id) ON DELETE CASCADE
);
"""

CREATE_THEMES_TABLE = """
CREATE TABLE IF NOT EXISTS themes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT
);
"""

CREATE_PAPER_THEMES_TABLE = """
CREATE TABLE IF NOT EXISTS paper_themes (
    paper_id INTEGER NOT NULL,
    theme_id INTEGER NOT NULL,
    relevance_score REAL DEFAULT 1.0,
    PRIMARY KEY (paper_id, theme_id),
    FOREIGN KEY (paper_id) REFERENCES papers(id) ON DELETE CASCADE,
    FOREIGN KEY (theme_id) REFERENCES themes(id) ON DELETE CASCADE
);
"""

CREATE_CITATIONS_TABLE = """
CREATE TABLE IF NOT EXISTS citations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_paper_id INTEGER NOT NULL,
    cited_paper_id INTEGER NOT NULL,
    context TEXT,
    FOREIGN KEY (source_paper_id) REFERENCES papers(id) ON DELETE CASCADE,
    FOREIGN KEY (cited_paper_id) REFERENCES papers(id) ON DELETE CASCADE
);
"""

# Indexes for performance

CREATE_INDEX_PAPERS_YEAR = """
CREATE INDEX IF NOT EXISTS idx_papers_year ON papers(year);
"""

CREATE_INDEX_PAPERS_TITLE = """
CREATE INDEX IF NOT EXISTS idx_papers_title ON papers(title);
"""

CREATE_INDEX_SECTIONS_PAPER_ID = """
CREATE INDEX IF NOT EXISTS idx_sections_paper_id ON sections(paper_id);
"""

CREATE_INDEX_SECTIONS_TYPE = """
CREATE INDEX IF NOT EXISTS idx_sections_type ON sections(section_type);
"""

CREATE_INDEX_FINDINGS_PAPER_ID = """
CREATE INDEX IF NOT EXISTS idx_findings_paper_id ON key_findings(paper_id);
"""

CREATE_INDEX_FINDINGS_CATEGORY = """
CREATE INDEX IF NOT EXISTS idx_findings_category ON key_findings(category);
"""

CREATE_INDEX_PAPER_THEMES_PAPER = """
CREATE INDEX IF NOT EXISTS idx_paper_themes_paper ON paper_themes(paper_id);
"""

CREATE_INDEX_PAPER_THEMES_THEME = """
CREATE INDEX IF NOT EXISTS idx_paper_themes_theme ON paper_themes(theme_id);
"""

CREATE_INDEX_CITATIONS_SOURCE = """
CREATE INDEX IF NOT EXISTS idx_citations_source ON citations(source_paper_id);
"""

CREATE_INDEX_CITATIONS_CITED = """
CREATE INDEX IF NOT EXISTS idx_citations_cited ON citations(cited_paper_id);
"""

# Full-text search tables (for SQLite FTS5)

CREATE_FTS_PAPERS = """
CREATE VIRTUAL TABLE IF NOT EXISTS papers_fts USING fts5(
    title,
    authors,
    abstract,
    brief_summary,
    detailed_summary,
    content='papers',
    content_rowid='id'
);
"""

CREATE_FTS_TRIGGER_INSERT = """
CREATE TRIGGER IF NOT EXISTS papers_fts_insert AFTER INSERT ON papers
BEGIN
    INSERT INTO papers_fts(rowid, title, authors, abstract, brief_summary, detailed_summary)
    VALUES (new.id, new.title, new.authors, new.abstract, new.brief_summary, new.detailed_summary);
END;
"""

CREATE_FTS_TRIGGER_UPDATE = """
CREATE TRIGGER IF NOT EXISTS papers_fts_update AFTER UPDATE ON papers
BEGIN
    UPDATE papers_fts SET
        title = new.title,
        authors = new.authors,
        abstract = new.abstract,
        brief_summary = new.brief_summary,
        detailed_summary = new.detailed_summary
    WHERE rowid = new.id;
END;
"""

CREATE_FTS_TRIGGER_DELETE = """
CREATE TRIGGER IF NOT EXISTS papers_fts_delete AFTER DELETE ON papers
BEGIN
    DELETE FROM papers_fts WHERE rowid = old.id;
END;
"""

# List of all schema creation statements

ALL_TABLES = [
    CREATE_PAPERS_TABLE,
    CREATE_SECTIONS_TABLE,
    CREATE_KEY_FINDINGS_TABLE,
    CREATE_THEMES_TABLE,
    CREATE_PAPER_THEMES_TABLE,
    CREATE_CITATIONS_TABLE,
]

ALL_INDEXES = [
    CREATE_INDEX_PAPERS_YEAR,
    CREATE_INDEX_PAPERS_TITLE,
    CREATE_INDEX_SECTIONS_PAPER_ID,
    CREATE_INDEX_SECTIONS_TYPE,
    CREATE_INDEX_FINDINGS_PAPER_ID,
    CREATE_INDEX_FINDINGS_CATEGORY,
    CREATE_INDEX_PAPER_THEMES_PAPER,
    CREATE_INDEX_PAPER_THEMES_THEME,
    CREATE_INDEX_CITATIONS_SOURCE,
    CREATE_INDEX_CITATIONS_CITED,
]

ALL_FTS = [
    CREATE_FTS_PAPERS,
    CREATE_FTS_TRIGGER_INSERT,
    CREATE_FTS_TRIGGER_UPDATE,
    CREATE_FTS_TRIGGER_DELETE,
]


def get_all_schema_statements():
    """Get all schema creation statements in order."""
    return ALL_TABLES + ALL_INDEXES + ALL_FTS
