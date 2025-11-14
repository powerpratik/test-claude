"""
Templates for literature review sections following ACM Computing Surveys format.
"""

from typing import List, Dict
from ..knowledge_base.models import Paper


class ReviewTemplates:
    """Templates for generating review sections."""

    @staticmethod
    def format_abstract(theme: str, paper_count: int, year_range: tuple) -> str:
        """Generate template for abstract section."""
        return f"""# Abstract

This literature review surveys the field of {theme}, analyzing {paper_count} significant papers published between {year_range[0]} and {year_range[1]}.

[SUMMARY OF MAIN THEMES AND TRENDS]

[KEY FINDINGS AND CONTRIBUTIONS]

[IDENTIFICATION OF GAPS AND FUTURE DIRECTIONS]

**Keywords**: {theme}, literature review, survey
"""

    @staticmethod
    def format_introduction(theme: str) -> str:
        """Generate template for introduction section."""
        return f"""# 1. Introduction

## 1.1 Motivation

[EXPLAIN THE IMPORTANCE AND RELEVANCE OF {theme.upper()}]

[DISCUSS CURRENT CHALLENGES AND WHY A SURVEY IS NEEDED]

## 1.2 Scope and Objectives

This survey aims to:

1. [OBJECTIVE 1: e.g., Provide comprehensive overview]
2. [OBJECTIVE 2: e.g., Classify existing approaches]
3. [OBJECTIVE 3: e.g., Identify trends and patterns]
4. [OBJECTIVE 4: e.g., Highlight open challenges]

## 1.3 Survey Methodology

[DESCRIBE PAPER SELECTION CRITERIA]

[MENTION NUMBER OF PAPERS AND TIME PERIOD]

[EXPLAIN CLASSIFICATION APPROACH]

## 1.4 Organization

The remainder of this survey is organized as follows:

- Section 2 provides background and key concepts
- Section 3 presents our taxonomy of approaches
- Section 4 provides detailed analysis of major categories
- Section 5 discusses findings, trends, and comparisons
- Section 6 identifies open challenges and future directions
- Section 7 concludes the survey
"""

    @staticmethod
    def format_background() -> str:
        """Generate template for background section."""
        return """# 2. Background

## 2.1 Key Concepts and Definitions

[DEFINE FUNDAMENTAL TERMS AND CONCEPTS]

[PROVIDE NECESSARY TECHNICAL BACKGROUND]

## 2.2 Historical Context

[TRACE THE EVOLUTION OF THE FIELD]

[HIGHLIGHT SEMINAL WORKS]

## 2.3 Related Surveys

[DISCUSS OTHER SURVEYS IN THIS AREA]

[EXPLAIN HOW THIS SURVEY DIFFERS OR UPDATES PREVIOUS WORK]
"""

    @staticmethod
    def format_taxonomy() -> str:
        """Generate template for taxonomy section."""
        return """# 3. Taxonomy

## 3.1 Classification Dimensions

[EXPLAIN THE DIMENSIONS USED FOR CLASSIFICATION]

[JUSTIFY THE CHOSEN TAXONOMY]

## 3.2 Overview of Categories

[PROVIDE HIGH-LEVEL OVERVIEW OF MAIN CATEGORIES]

[INCLUDE VISUAL TAXONOMY IF POSSIBLE]

### 3.2.1 Category 1: [NAME]

[BRIEF DESCRIPTION]
[KEY CHARACTERISTICS]

### 3.2.2 Category 2: [NAME]

[BRIEF DESCRIPTION]
[KEY CHARACTERISTICS]

[... ADDITIONAL CATEGORIES ...]
"""

    @staticmethod
    def format_analysis_section(category_name: str) -> str:
        """Generate template for detailed analysis section."""
        return f"""## 4.X {category_name}

### 4.X.1 Overview

[PROVIDE OVERVIEW OF APPROACHES IN THIS CATEGORY]

### 4.X.2 Key Papers and Contributions

[DISCUSS MAJOR PAPERS IN THIS CATEGORY]

#### Paper 1: [TITLE]

- **Authors**: [AUTHORS]
- **Year**: [YEAR]
- **Key Contribution**: [CONTRIBUTION]
- **Methodology**: [APPROACH]
- **Strengths**: [STRENGTHS]
- **Limitations**: [LIMITATIONS]

[... ADDITIONAL PAPERS ...]

### 4.X.3 Comparative Analysis

[COMPARE AND CONTRAST DIFFERENT APPROACHES]

[USE TABLES IF APPROPRIATE]

### 4.X.4 Summary

[SUMMARIZE KEY INSIGHTS FROM THIS CATEGORY]
"""

    @staticmethod
    def format_discussion() -> str:
        """Generate template for discussion section."""
        return """# 5. Discussion

## 5.1 Key Findings and Trends

### 5.1.1 Major Themes

[IDENTIFY OVERARCHING THEMES ACROSS PAPERS]

### 5.1.2 Evolution Over Time

[DISCUSS HOW THE FIELD HAS EVOLVED]

### 5.1.3 Methodological Trends

[IDENTIFY COMMON METHODOLOGIES AND THEIR EVOLUTION]

## 5.2 Comparative Analysis

### 5.2.1 Strengths and Weaknesses

[COMPARE DIFFERENT APPROACHES]

[DISCUSS TRADE-OFFS]

### 5.2.2 Application Domains

[DISCUSS WHERE DIFFERENT APPROACHES ARE MOST APPLICABLE]

## 5.3 Open Challenges

### 5.3.1 Technical Challenges

[IDENTIFY UNRESOLVED TECHNICAL PROBLEMS]

### 5.3.2 Practical Challenges

[DISCUSS DEPLOYMENT AND SCALABILITY ISSUES]

### 5.3.3 Research Gaps

[IDENTIFY AREAS NEEDING MORE RESEARCH]
"""

    @staticmethod
    def format_future_directions() -> str:
        """Generate template for future directions."""
        return """# 6. Future Research Directions

## 6.1 Short-term Opportunities

[DISCUSS IMMEDIATE RESEARCH OPPORTUNITIES]

## 6.2 Long-term Directions

[DISCUSS LONGER-TERM RESEARCH DIRECTIONS]

## 6.3 Emerging Trends

[IDENTIFY EMERGING TRENDS AND TECHNOLOGIES]

## 6.4 Recommended Research Agenda

1. [PRIORITY 1]
2. [PRIORITY 2]
3. [PRIORITY 3]
[...]
"""

    @staticmethod
    def format_conclusion() -> str:
        """Generate template for conclusion."""
        return """# 7. Conclusion

[SUMMARIZE THE MAIN CONTRIBUTIONS OF THE SURVEY]

[REITERATE KEY FINDINGS]

[EMPHASIZE IMPORTANCE OF FUTURE WORK]

[CONCLUDING STATEMENT]
"""

    @staticmethod
    def format_reference(paper: Paper, citation_number: int) -> str:
        """Format a paper as a reference."""
        year = paper.year if paper.year else "n.d."
        authors = paper.authors if paper.authors else "Unknown"

        return f"[{citation_number}] {authors}. {year}. {paper.title}. {paper.venue}."


class CitationManager:
    """Manage citations in the review."""

    def __init__(self):
        """Initialize citation manager."""
        self.citations: Dict[int, Paper] = {}
        self.next_number = 1

    def add_citation(self, paper: Paper) -> int:
        """
        Add a citation and return its number.

        Args:
            paper: Paper to cite

        Returns:
            Citation number
        """
        # Check if already cited
        for num, cited_paper in self.citations.items():
            if cited_paper.id == paper.id:
                return num

        # Add new citation
        citation_num = self.next_number
        self.citations[citation_num] = paper
        self.next_number += 1

        return citation_num

    def format_citation(self, citation_number: int) -> str:
        """Format inline citation."""
        return f"[{citation_number}]"

    def generate_references_section(self) -> str:
        """Generate the references section."""
        lines = ["# References\n"]

        for num in sorted(self.citations.keys()):
            paper = self.citations[num]
            ref = ReviewTemplates.format_reference(paper, num)
            lines.append(ref)

        return "\n".join(lines)

    def get_citation_count(self) -> int:
        """Get total number of citations."""
        return len(self.citations)


class TableFormatter:
    """Format comparison tables."""

    @staticmethod
    def create_comparison_table(papers: List[Paper], columns: List[str]) -> str:
        """
        Create a markdown comparison table.

        Args:
            papers: Papers to compare
            columns: Column headers

        Returns:
            Markdown table string
        """
        if not papers:
            return ""

        # Create header
        header = "| Paper | " + " | ".join(columns) + " |"
        separator = "|" + "|".join(["---"] * (len(columns) + 1)) + "|"

        lines = [header, separator]

        # Add rows
        for paper in papers:
            title_short = paper.title[:50] + "..." if len(paper.title) > 50 else paper.title
            row = f"| {title_short} |"

            # Placeholder for column values (to be filled in with actual data)
            for col in columns:
                row += " [VALUE] |"

            lines.append(row)

        return "\n".join(lines)

    @staticmethod
    def create_year_distribution_table(year_dist: Dict[int, int]) -> str:
        """Create table showing paper distribution by year."""
        lines = [
            "| Year | Number of Papers |",
            "|------|------------------|"
        ]

        for year in sorted(year_dist.keys()):
            count = year_dist[year]
            lines.append(f"| {year} | {count} |")

        return "\n".join(lines)
