"""
LaTeX formatter for generating Overleaf-compatible literature reviews.
"""

from typing import List, Dict, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from knowledge_base.models import Paper


class LaTeXFormatter:
    """Format literature reviews in LaTeX for Overleaf."""

    @staticmethod
    def format_document_header(title: str, author: str = "Literature Review Generator") -> str:
        """Generate LaTeX document header."""
        return r"""\documentclass[11pt,a4paper]{article}

% Packages
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{graphicx}
\usepackage{hyperref}
\usepackage{cite}
\usepackage{amsmath}
\usepackage{booktabs}
\usepackage{geometry}
\usepackage{setspace}
\usepackage{titlesec}

% Page geometry
\geometry{
    a4paper,
    left=1in,
    right=1in,
    top=1in,
    bottom=1in
}

% Hyperref setup
\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    citecolor=blue,
    urlcolor=blue
}

% Line spacing
\onehalfspacing

% Title and author
\title{""" + title + r"""}
\author{""" + author + r"""}
\date{\today}

\begin{document}

\maketitle
\tableofcontents
\newpage

"""

    @staticmethod
    def format_abstract(content: str) -> str:
        """Format abstract section."""
        return r"""\begin{abstract}
""" + LaTeXFormatter._escape_latex(content) + r"""
\end{abstract}

\newpage
"""

    @staticmethod
    def format_section(title: str, content: str, level: int = 1) -> str:
        """Format a section."""
        section_cmd = {
            1: r"\section",
            2: r"\subsection",
            3: r"\subsubsection"
        }.get(level, r"\paragraph")

        return f"{section_cmd}{{{LaTeXFormatter._escape_latex(title)}}}\n\n{LaTeXFormatter._escape_latex(content)}\n\n"

    @staticmethod
    def format_itemize(items: List[str]) -> str:
        """Format bullet list."""
        latex = r"\begin{itemize}" + "\n"
        for item in items:
            latex += f"    \\item {LaTeXFormatter._escape_latex(item)}\n"
        latex += r"\end{itemize}" + "\n"
        return latex

    @staticmethod
    def format_enumerate(items: List[str]) -> str:
        """Format numbered list."""
        latex = r"\begin{enumerate}" + "\n"
        for item in items:
            latex += f"    \\item {LaTeXFormatter._escape_latex(item)}\n"
        latex += r"\end{enumerate}" + "\n"
        return latex

    @staticmethod
    def format_table(headers: List[str], rows: List[List[str]], caption: str = "") -> str:
        """Format a table."""
        num_cols = len(headers)
        col_spec = "l" * num_cols

        latex = r"\begin{table}[htbp]" + "\n"
        latex += r"\centering" + "\n"
        latex += f"\\begin{{tabular}}{{{col_spec}}}\n"
        latex += r"\toprule" + "\n"

        # Headers
        latex += " & ".join(LaTeXFormatter._escape_latex(h) for h in headers) + r" \\" + "\n"
        latex += r"\midrule" + "\n"

        # Rows
        for row in rows:
            latex += " & ".join(LaTeXFormatter._escape_latex(str(cell)) for cell in row) + r" \\" + "\n"

        latex += r"\bottomrule" + "\n"
        latex += r"\end{tabular}" + "\n"

        if caption:
            latex += f"\\caption{{{LaTeXFormatter._escape_latex(caption)}}}\n"

        latex += r"\end{table}" + "\n"
        return latex

    @staticmethod
    def format_citation(citation_number: int) -> str:
        """Format inline citation."""
        return f"\\cite{{ref{citation_number}}}"

    @staticmethod
    def format_references(citations: Dict[int, Any]) -> str:
        """Format references section."""
        latex = r"\newpage" + "\n"
        latex += r"\bibliographystyle{plain}" + "\n"
        latex += r"\begin{thebibliography}{99}" + "\n\n"

        for num in sorted(citations.keys()):
            paper = citations[num]
            latex += f"\\bibitem{{ref{num}}}\n"

            # Author
            if paper.authors:
                latex += LaTeXFormatter._escape_latex(paper.authors) + ".\n"

            # Title
            latex += f"\\textit{{{LaTeXFormatter._escape_latex(paper.title)}}}.\n"

            # Venue and year
            if paper.venue:
                latex += LaTeXFormatter._escape_latex(paper.venue)
                if paper.year:
                    latex += f", {paper.year}.\n"
                else:
                    latex += ".\n"
            elif paper.year:
                latex += f"{paper.year}.\n"
            else:
                latex += "\n"

            # DOI if available
            if paper.doi:
                latex += f"DOI: \\url{{{paper.doi}}}.\n"

            latex += "\n"

        latex += r"\end{thebibliography}" + "\n"
        return latex

    @staticmethod
    def format_document_footer() -> str:
        """Generate document footer."""
        return r"""
\end{document}
"""

    @staticmethod
    def _escape_latex(text: str) -> str:
        """Escape special LaTeX characters."""
        if not text:
            return ""

        # Define replacements
        replacements = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\textasciicircum{}',
            '\\': r'\textbackslash{}',
        }

        result = str(text)
        for char, replacement in replacements.items():
            result = result.replace(char, replacement)

        return result

    @staticmethod
    def create_complete_document(
        title: str,
        sections: Dict[str, str],
        citations: Dict[int, Any],
        author: str = "Literature Review Generator"
    ) -> str:
        """
        Create a complete LaTeX document.

        Args:
            title: Document title
            sections: Dictionary of section_name -> content
            citations: Dictionary of citation_number -> Paper
            author: Author name

        Returns:
            Complete LaTeX document string
        """
        latex = LaTeXFormatter.format_document_header(title, author)

        # Add abstract if present
        if 'abstract' in sections:
            latex += LaTeXFormatter.format_abstract(sections['abstract'])
            sections = {k: v for k, v in sections.items() if k != 'abstract'}

        # Add all sections
        for section_name, content in sections.items():
            # Convert markdown-style headers to LaTeX
            content_latex = LaTeXFormatter._convert_markdown_to_latex(content)
            latex += content_latex + "\n"

        # Add references
        latex += LaTeXFormatter.format_references(citations)

        # Add footer
        latex += LaTeXFormatter.format_document_footer()

        return latex

    @staticmethod
    def _convert_markdown_to_latex(markdown_text: str) -> str:
        """Convert markdown-style formatting to LaTeX."""
        import re

        text = markdown_text

        # Headers
        text = re.sub(r'^# (.+)$', r'\\section{\1}', text, flags=re.MULTILINE)
        text = re.sub(r'^## (.+)$', r'\\subsection{\1}', text, flags=re.MULTILINE)
        text = re.sub(r'^### (.+)$', r'\\subsubsection{\1}', text, flags=re.MULTILINE)
        text = re.sub(r'^#### (.+)$', r'\\paragraph{\1}', text, flags=re.MULTILINE)

        # Bold
        text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)

        # Italic
        text = re.sub(r'\*(.+?)\*', r'\\textit{\1}', text)
        text = re.sub(r'_(.+?)_', r'\\textit{\1}', text)

        # Code (inline)
        text = re.sub(r'`(.+?)`', r'\\texttt{\1}', text)

        # Bullet lists
        text = re.sub(r'^- (.+)$', r'\\item \1', text, flags=re.MULTILINE)

        # Wrap consecutive \item lines in itemize
        lines = text.split('\n')
        in_list = False
        result_lines = []

        for line in lines:
            if line.strip().startswith(r'\item'):
                if not in_list:
                    result_lines.append(r'\begin{itemize}')
                    in_list = True
                result_lines.append(line)
            else:
                if in_list:
                    result_lines.append(r'\end{itemize}')
                    in_list = False
                result_lines.append(line)

        if in_list:
            result_lines.append(r'\end{itemize}')

        text = '\n'.join(result_lines)

        # Escape any remaining special characters
        # (but preserve LaTeX commands we just created)
        # This is tricky - we need to be selective

        return text


class OverleafProject:
    """Generate Overleaf-compatible project structure."""

    @staticmethod
    def create_project_structure(review_latex: str, output_dir: str):
        """
        Create an Overleaf project structure.

        Args:
            review_latex: LaTeX content
            output_dir: Output directory path
        """
        from pathlib import Path

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Write main.tex
        main_tex_path = output_path / "main.tex"
        with open(main_tex_path, 'w', encoding='utf-8') as f:
            f.write(review_latex)

        # Create README for Overleaf
        readme_path = output_path / "README.txt"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write("""Literature Review - Overleaf Project

This project contains a literature review generated by the Literature Review Generator.

Files:
- main.tex: Main LaTeX document

To use in Overleaf:
1. Create a new project in Overleaf
2. Upload main.tex
3. Compile using pdflatex or xelatex

Alternatively:
- Zip this folder and upload to Overleaf as a new project

To compile locally:
pdflatex main.tex
pdflatex main.tex  # Run twice for references

Generated with Literature Review Generator
""")

        print(f"✓ Overleaf project created at: {output_path}")
        print(f"  - main.tex (LaTeX source)")
        print(f"  - README.txt (instructions)")
        print(f"\nTo use in Overleaf:")
        print(f"  1. Zip the folder: {output_path}")
        print(f"  2. Upload to Overleaf as new project")
        print(f"  3. Compile with pdflatex")
