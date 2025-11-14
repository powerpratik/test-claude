#!/usr/bin/env python3
"""
Main CLI interface for Literature Review Generator.
"""

import sys
import argparse
import logging
from pathlib import Path
from typing import List, Optional

from config import get_config
from knowledge_base.storage import KnowledgeBase
from processors.paper_processor import PaperProcessor
from retrieval.query_engine import QueryEngine
from generation.review_generator import ReviewGenerator


def setup_logging(level: str = "INFO"):
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('logs/app.log')
        ]
    )


class LiteratureReviewCLI:
    """Command-line interface for literature review application."""

    def __init__(self):
        """Initialize CLI."""
        self.config = get_config()
        self.kb = None

    def _init_kb(self):
        """Initialize knowledge base connection."""
        if self.kb is None:
            self.kb = KnowledgeBase(str(self.config.database_path))

    def cmd_init(self, args):
        """Initialize the knowledge base."""
        print(f"Initializing knowledge base at: {self.config.database_path}")

        if self.config.database_path.exists() and not args.reset:
            print("Database already exists. Use --reset to reinitialize.")
            return

        if args.reset and self.config.database_path.exists():
            print("Resetting existing database...")
            self.config.database_path.unlink()

        self._init_kb()
        self.kb.initialize_schema()
        print("✓ Knowledge base initialized successfully")

    def cmd_ingest(self, args):
        """Ingest papers into the knowledge base."""
        self._init_kb()

        processor = PaperProcessor(
            self.kb,
            config={
                'summary_brief_tokens': self.config.summary_brief_tokens,
                'summary_detailed_tokens': self.config.summary_detailed_tokens,
            }
        )

        themes = args.theme.split(',') if args.theme else None

        if args.file:
            # Ingest single file
            print(f"Ingesting paper: {args.file}")
            try:
                paper = processor.process_paper(args.file, themes=themes)
                print(f"✓ Successfully ingested: {paper.title}")
            except Exception as e:
                print(f"✗ Error ingesting paper: {e}")
                logging.exception("Error during paper ingestion")

        elif args.directory:
            # Ingest all files in directory
            directory = Path(args.directory)
            if not directory.exists():
                print(f"✗ Directory not found: {directory}")
                return

            files = list(directory.glob("*.pdf")) + list(directory.glob("*.txt"))
            print(f"Found {len(files)} files to ingest")

            for i, file_path in enumerate(files, 1):
                print(f"\n[{i}/{len(files)}] Processing: {file_path.name}")
                try:
                    paper = processor.process_paper(str(file_path), themes=themes)
                    print(f"  ✓ {paper.title}")
                except Exception as e:
                    print(f"  ✗ Error: {e}")
                    logging.exception(f"Error processing {file_path}")

            print(f"\n✓ Ingestion complete: {len(files)} files processed")

    def cmd_list(self, args):
        """List papers in the knowledge base."""
        self._init_kb()

        papers = self.kb.get_all_papers(limit=args.limit)

        if not papers:
            print("No papers found in knowledge base.")
            return

        print(f"\nFound {len(papers)} papers:\n")
        print(f"{'ID':<5} {'Year':<6} {'Title':<60} {'Authors':<30}")
        print("-" * 105)

        for paper in papers:
            title = paper.title[:57] + "..." if len(paper.title) > 60 else paper.title
            authors = paper.authors[:27] + "..." if len(paper.authors) > 30 else paper.authors
            year = paper.year if paper.year else "N/A"

            print(f"{paper.id:<5} {year:<6} {title:<60} {authors:<30}")

    def cmd_show(self, args):
        """Show details of a specific paper."""
        self._init_kb()

        paper = self.kb.get_paper(args.paper_id)
        if not paper:
            print(f"✗ Paper not found: {args.paper_id}")
            return

        print(f"\n{'='*80}")
        print(f"Paper ID: {paper.id}")
        print(f"{'='*80}\n")
        print(f"Title: {paper.title}")
        print(f"Authors: {paper.authors}")
        print(f"Year: {paper.year}")
        print(f"Venue: {paper.venue}")
        print(f"\nAbstract:\n{paper.abstract}\n")
        print(f"\nBrief Summary:\n{paper.brief_summary}\n")

        # Show themes
        themes = self.kb.get_paper_themes(paper.id)
        if themes:
            print(f"Themes: {', '.join(t.name for t in themes)}")

        # Show findings
        findings = self.kb.get_paper_findings(paper.id)
        if findings:
            print(f"\nKey Findings ({len(findings)}):")
            for finding in findings:
                print(f"  [{finding.category}] {finding.finding_text[:100]}...")

    def cmd_themes(self, args):
        """List all themes."""
        self._init_kb()

        themes = self.kb.get_all_themes()

        if not themes:
            print("No themes found.")
            return

        print(f"\nFound {len(themes)} themes:\n")
        print(f"{'ID':<5} {'Name':<40} {'Papers':<10}")
        print("-" * 55)

        for theme in themes:
            print(f"{theme.id:<5} {theme.name:<40} {theme.paper_count:<10}")

    def cmd_search(self, args):
        """Search for papers."""
        self._init_kb()
        query_engine = QueryEngine(self.kb)

        if args.theme:
            papers = query_engine.get_papers_by_theme(args.theme)
            print(f"\nPapers in theme '{args.theme}': {len(papers)}\n")

        elif args.keyword:
            papers = query_engine.search_by_keyword(args.keyword)
            print(f"\nPapers matching '{args.keyword}': {len(papers)}\n")

        else:
            print("✗ Please specify --theme or --keyword")
            return

        for paper in papers[:args.limit]:
            print(f"[{paper.id}] {paper.title} ({paper.year})")

    def cmd_generate(self, args):
        """Generate a literature review."""
        self._init_kb()

        print(f"\nGenerating literature review for theme: {args.theme}")

        generator = ReviewGenerator(
            self.kb,
            config={
                'min_papers_for_review': self.config.min_papers_for_review,
            }
        )

        # Parse sections
        sections = None
        if args.sections:
            sections = [s.strip() for s in args.sections.split(',')]

        try:
            # Estimate length first
            estimates = generator.estimate_review_length(args.theme)
            print(f"\nEstimated review length:")
            print(f"  Words: ~{estimates['total_words']:,}")
            print(f"  Pages: ~{estimates['estimated_pages']:.1f}")
            print(f"  Tokens: ~{estimates['total_tokens']:,}")
            print()

            # Generate review
            print("Generating review...")
            review = generator.generate_review(
                theme=args.theme,
                sections=sections,
                output_format=args.format,
                min_papers=args.min_papers
            )

            # Save to file
            output_path = Path(args.output)
            generator.save_review(review, output_path)

            print(f"\n✓ Review generated successfully!")
            print(f"  Output: {output_path}")
            print(f"  Citations: {generator.citation_manager.get_citation_count()}")

        except ValueError as e:
            print(f"\n✗ Error: {e}")
        except Exception as e:
            print(f"\n✗ Error generating review: {e}")
            logging.exception("Error during review generation")

    def cmd_stats(self, args):
        """Show database statistics."""
        self._init_kb()

        stats = self.kb.get_statistics()

        print("\n" + "="*50)
        print("Knowledge Base Statistics")
        print("="*50)
        print(f"Total Papers:      {stats['total_papers']}")
        print(f"Total Themes:      {stats['total_themes']}")
        print(f"Total Sections:    {stats['total_sections']}")
        print(f"Total Findings:    {stats['total_findings']}")
        print(f"Year Range:        {stats['year_range']}")
        print("="*50 + "\n")

    def run(self, argv: Optional[List[str]] = None):
        """Run the CLI application."""
        parser = argparse.ArgumentParser(
            description="Literature Review Generator - Generate high-quality literature reviews",
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

        parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

        subparsers = parser.add_subparsers(dest='command', help='Command to execute')

        # Init command
        parser_init = subparsers.add_parser('init', help='Initialize knowledge base')
        parser_init.add_argument('--reset', action='store_true', help='Reset existing database')

        # Ingest command
        parser_ingest = subparsers.add_parser('ingest', help='Ingest papers')
        parser_ingest.add_argument('--file', '-f', help='Path to paper file (PDF or text)')
        parser_ingest.add_argument('--directory', '-d', help='Directory containing papers')
        parser_ingest.add_argument('--theme', '-t', help='Theme(s) for the paper (comma-separated)')

        # List command
        parser_list = subparsers.add_parser('list', help='List papers')
        parser_list.add_argument('--limit', '-l', type=int, default=50, help='Maximum papers to show')

        # Show command
        parser_show = subparsers.add_parser('show', help='Show paper details')
        parser_show.add_argument('paper_id', type=int, help='Paper ID')

        # Themes command
        subparsers.add_parser('themes', help='List all themes')

        # Search command
        parser_search = subparsers.add_parser('search', help='Search papers')
        parser_search.add_argument('--theme', '-t', help='Search by theme')
        parser_search.add_argument('--keyword', '-k', help='Search by keyword')
        parser_search.add_argument('--limit', '-l', type=int, default=20, help='Maximum results')

        # Generate command
        parser_generate = subparsers.add_parser('generate', help='Generate literature review')
        parser_generate.add_argument('--theme', '-t', required=True, help='Theme for review')
        parser_generate.add_argument('--output', '-o', required=True, help='Output file path')
        parser_generate.add_argument('--sections', '-s', help='Sections to generate (comma-separated)')
        parser_generate.add_argument('--format', '-f', default='markdown', help='Output format')
        parser_generate.add_argument('--min-papers', type=int, default=20, help='Minimum papers required')

        # Stats command
        subparsers.add_parser('stats', help='Show database statistics')

        # Parse arguments
        args = parser.parse_args(argv)

        # Setup logging
        log_level = "DEBUG" if args.verbose else "INFO"
        setup_logging(log_level)

        # Execute command
        if not args.command:
            parser.print_help()
            return

        command_method = getattr(self, f'cmd_{args.command}', None)
        if command_method:
            try:
                command_method(args)
            except KeyboardInterrupt:
                print("\n\n✗ Interrupted by user")
                sys.exit(1)
            except Exception as e:
                print(f"\n✗ Error: {e}")
                logging.exception("Unhandled exception")
                sys.exit(1)
        else:
            print(f"Unknown command: {args.command}")
            parser.print_help()


def main():
    """Main entry point."""
    # Ensure logs directory exists
    Path("logs").mkdir(exist_ok=True)

    cli = LiteratureReviewCLI()
    cli.run()


if __name__ == "__main__":
    main()
