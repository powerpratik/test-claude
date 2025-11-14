"""Paper processing module for extraction and summarization."""

# Lazy imports to avoid circular dependencies
def __getattr__(name):
    if name == 'PaperProcessor':
        from .paper_processor import PaperProcessor
        return PaperProcessor
    elif name == 'Summarizer':
        from .summarizer import Summarizer
        return Summarizer
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ['PaperProcessor', 'Summarizer']
