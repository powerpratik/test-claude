"""Knowledge Base module for persistent storage and retrieval."""

# Lazy imports to avoid circular dependencies
def __getattr__(name):
    if name == 'KnowledgeBase':
        from .storage import KnowledgeBase
        return KnowledgeBase
    elif name == 'Paper':
        from .models import Paper
        return Paper
    elif name == 'Section':
        from .models import Section
        return Section
    elif name == 'KeyFinding':
        from .models import KeyFinding
        return KeyFinding
    elif name == 'Theme':
        from .models import Theme
        return Theme
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ['KnowledgeBase', 'Paper', 'Section', 'KeyFinding', 'Theme']
