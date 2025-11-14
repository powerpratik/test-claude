"""
Database storage operations for the knowledge base.
"""

import sqlite3
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
import logging

from .schema import get_all_schema_statements
from .models import Paper, Section, KeyFinding, Theme, PaperTheme, Citation

logger = logging.getLogger(__name__)


class KnowledgeBase:
    """Main interface for knowledge base operations."""

    def __init__(self, db_path: str):
        """
        Initialize knowledge base.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn: Optional[sqlite3.Connection] = None
        self._connect()

    def _connect(self):
        """Establish database connection."""
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Access columns by name
        self.conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign keys

    def initialize_schema(self):
        """Create all tables and indexes."""
        cursor = self.conn.cursor()

        try:
            for statement in get_all_schema_statements():
                cursor.execute(statement)

            self.conn.commit()
            logger.info("Database schema initialized successfully")

        except sqlite3.Error as e:
            self.conn.rollback()
            logger.error(f"Error initializing schema: {e}")
            raise

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()

    # Paper operations

    def add_paper(self, paper: Paper) -> int:
        """
        Add a new paper to the database.

        Args:
            paper: Paper object to add

        Returns:
            ID of the inserted paper
        """
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO papers (
                    title, authors, year, venue, doi, abstract,
                    full_text_path, brief_summary, detailed_summary
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                paper.title, paper.authors, paper.year, paper.venue,
                paper.doi, paper.abstract, paper.full_text_path,
                paper.brief_summary, paper.detailed_summary
            ))

            self.conn.commit()
            paper_id = cursor.lastrowid
            logger.info(f"Added paper: {paper.title} (ID: {paper_id})")
            return paper_id

        except sqlite3.Error as e:
            self.conn.rollback()
            logger.error(f"Error adding paper: {e}")
            raise

    def get_paper(self, paper_id: int) -> Optional[Paper]:
        """
        Get a paper by ID.

        Args:
            paper_id: Paper ID

        Returns:
            Paper object or None if not found
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM papers WHERE id = ?", (paper_id,))
        row = cursor.fetchone()

        if row:
            return self._row_to_paper(row)
        return None

    def get_all_papers(self, limit: Optional[int] = None) -> List[Paper]:
        """
        Get all papers.

        Args:
            limit: Maximum number of papers to return

        Returns:
            List of Paper objects
        """
        cursor = self.conn.cursor()
        query = "SELECT * FROM papers ORDER BY year DESC, title"

        if limit:
            query += f" LIMIT {limit}"

        cursor.execute(query)
        return [self._row_to_paper(row) for row in cursor.fetchall()]

    def update_paper(self, paper: Paper):
        """
        Update an existing paper.

        Args:
            paper: Paper object with updated data
        """
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
                UPDATE papers SET
                    title = ?,
                    authors = ?,
                    year = ?,
                    venue = ?,
                    doi = ?,
                    abstract = ?,
                    full_text_path = ?,
                    brief_summary = ?,
                    detailed_summary = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (
                paper.title, paper.authors, paper.year, paper.venue,
                paper.doi, paper.abstract, paper.full_text_path,
                paper.brief_summary, paper.detailed_summary, paper.id
            ))

            self.conn.commit()
            logger.info(f"Updated paper ID: {paper.id}")

        except sqlite3.Error as e:
            self.conn.rollback()
            logger.error(f"Error updating paper: {e}")
            raise

    def delete_paper(self, paper_id: int):
        """
        Delete a paper and all related data.

        Args:
            paper_id: Paper ID
        """
        cursor = self.conn.cursor()

        try:
            cursor.execute("DELETE FROM papers WHERE id = ?", (paper_id,))
            self.conn.commit()
            logger.info(f"Deleted paper ID: {paper_id}")

        except sqlite3.Error as e:
            self.conn.rollback()
            logger.error(f"Error deleting paper: {e}")
            raise

    def search_papers(self, query: str, limit: int = 50) -> List[Paper]:
        """
        Full-text search for papers.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of matching papers
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT p.* FROM papers p
            JOIN papers_fts fts ON p.id = fts.rowid
            WHERE papers_fts MATCH ?
            ORDER BY rank
            LIMIT ?
        """, (query, limit))

        return [self._row_to_paper(row) for row in cursor.fetchall()]

    # Section operations

    def add_section(self, section: Section) -> int:
        """Add a section to a paper."""
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO sections (
                    paper_id, section_type, title, content, summary, order_index
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                section.paper_id, section.section_type, section.title,
                section.content, section.summary, section.order_index
            ))

            self.conn.commit()
            return cursor.lastrowid

        except sqlite3.Error as e:
            self.conn.rollback()
            logger.error(f"Error adding section: {e}")
            raise

    def get_paper_sections(self, paper_id: int) -> List[Section]:
        """Get all sections for a paper."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM sections
            WHERE paper_id = ?
            ORDER BY order_index
        """, (paper_id,))

        return [self._row_to_section(row) for row in cursor.fetchall()]

    # Key findings operations

    def add_finding(self, finding: KeyFinding) -> int:
        """Add a key finding."""
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO key_findings (
                    paper_id, finding_text, category, importance_score
                )
                VALUES (?, ?, ?, ?)
            """, (
                finding.paper_id, finding.finding_text,
                finding.category, finding.importance_score
            ))

            self.conn.commit()
            return cursor.lastrowid

        except sqlite3.Error as e:
            self.conn.rollback()
            logger.error(f"Error adding finding: {e}")
            raise

    def get_paper_findings(self, paper_id: int) -> List[KeyFinding]:
        """Get all findings for a paper."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM key_findings
            WHERE paper_id = ?
            ORDER BY importance_score DESC
        """, (paper_id,))

        return [self._row_to_finding(row) for row in cursor.fetchall()]

    # Theme operations

    def add_theme(self, theme: Theme) -> int:
        """Add a new theme."""
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO themes (name, description)
                VALUES (?, ?)
            """, (theme.name, theme.description))

            self.conn.commit()
            return cursor.lastrowid

        except sqlite3.IntegrityError:
            # Theme already exists, get its ID
            cursor.execute("SELECT id FROM themes WHERE name = ?", (theme.name,))
            return cursor.fetchone()[0]

        except sqlite3.Error as e:
            self.conn.rollback()
            logger.error(f"Error adding theme: {e}")
            raise

    def get_theme(self, theme_id: int) -> Optional[Theme]:
        """Get a theme by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM themes WHERE id = ?", (theme_id,))
        row = cursor.fetchone()

        if row:
            return self._row_to_theme(row)
        return None

    def get_theme_by_name(self, name: str) -> Optional[Theme]:
        """Get a theme by name."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM themes WHERE name = ?", (name,))
        row = cursor.fetchone()

        if row:
            return self._row_to_theme(row)
        return None

    def get_all_themes(self) -> List[Theme]:
        """Get all themes with paper counts."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT t.id, t.name, t.description, COUNT(pt.paper_id) as paper_count
            FROM themes t
            LEFT JOIN paper_themes pt ON t.id = pt.theme_id
            GROUP BY t.id
            ORDER BY paper_count DESC, t.name
        """)

        themes = []
        for row in cursor.fetchall():
            theme = Theme(
                id=row['id'],
                name=row['name'],
                description=row['description'],
                paper_count=row['paper_count']
            )
            themes.append(theme)

        return themes

    def link_paper_theme(self, paper_id: int, theme_id: int, relevance_score: float = 1.0):
        """Link a paper to a theme."""
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
                INSERT OR REPLACE INTO paper_themes (paper_id, theme_id, relevance_score)
                VALUES (?, ?, ?)
            """, (paper_id, theme_id, relevance_score))

            self.conn.commit()

        except sqlite3.Error as e:
            self.conn.rollback()
            logger.error(f"Error linking paper to theme: {e}")
            raise

    def get_papers_by_theme(self, theme_id: int) -> List[Paper]:
        """Get all papers for a theme."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT p.* FROM papers p
            JOIN paper_themes pt ON p.id = pt.paper_id
            WHERE pt.theme_id = ?
            ORDER BY pt.relevance_score DESC, p.year DESC
        """, (theme_id,))

        return [self._row_to_paper(row) for row in cursor.fetchall()]

    def get_paper_themes(self, paper_id: int) -> List[Theme]:
        """Get all themes for a paper."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT t.* FROM themes t
            JOIN paper_themes pt ON t.id = pt.theme_id
            WHERE pt.paper_id = ?
        """, (paper_id,))

        return [self._row_to_theme(row) for row in cursor.fetchall()]

    # Citation operations

    def add_citation(self, citation: Citation) -> int:
        """Add a citation relationship."""
        cursor = self.conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO citations (source_paper_id, cited_paper_id, context)
                VALUES (?, ?, ?)
            """, (citation.source_paper_id, citation.cited_paper_id, citation.context))

            self.conn.commit()
            return cursor.lastrowid

        except sqlite3.Error as e:
            self.conn.rollback()
            logger.error(f"Error adding citation: {e}")
            raise

    # Statistics and utilities

    def get_statistics(self) -> Dict[str, int]:
        """Get database statistics."""
        cursor = self.conn.cursor()

        stats = {}

        cursor.execute("SELECT COUNT(*) as count FROM papers")
        stats['total_papers'] = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM themes")
        stats['total_themes'] = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM sections")
        stats['total_sections'] = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM key_findings")
        stats['total_findings'] = cursor.fetchone()['count']

        cursor.execute("SELECT MIN(year) as min_year, MAX(year) as max_year FROM papers WHERE year IS NOT NULL")
        row = cursor.fetchone()
        stats['year_range'] = f"{row['min_year']}-{row['max_year']}" if row['min_year'] else "N/A"

        return stats

    # Helper methods

    def _row_to_paper(self, row: sqlite3.Row) -> Paper:
        """Convert database row to Paper object."""
        return Paper(
            id=row['id'],
            title=row['title'],
            authors=row['authors'],
            year=row['year'],
            venue=row['venue'],
            doi=row['doi'],
            abstract=row['abstract'],
            full_text_path=row['full_text_path'],
            brief_summary=row['brief_summary'],
            detailed_summary=row['detailed_summary'],
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None,
            updated_at=datetime.fromisoformat(row['updated_at']) if row['updated_at'] else None,
        )

    def _row_to_section(self, row: sqlite3.Row) -> Section:
        """Convert database row to Section object."""
        return Section(
            id=row['id'],
            paper_id=row['paper_id'],
            section_type=row['section_type'],
            title=row['title'],
            content=row['content'],
            summary=row['summary'],
            order_index=row['order_index'],
        )

    def _row_to_finding(self, row: sqlite3.Row) -> KeyFinding:
        """Convert database row to KeyFinding object."""
        return KeyFinding(
            id=row['id'],
            paper_id=row['paper_id'],
            finding_text=row['finding_text'],
            category=row['category'],
            importance_score=row['importance_score'],
        )

    def _row_to_theme(self, row: sqlite3.Row) -> Theme:
        """Convert database row to Theme object."""
        return Theme(
            id=row['id'],
            name=row['name'],
            description=row['description'],
        )

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def __repr__(self) -> str:
        return f"KnowledgeBase(db_path='{self.db_path}')"
