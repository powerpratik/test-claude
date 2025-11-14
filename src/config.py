"""
Configuration management for Literature Review Generator.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class Config:
    """Configuration manager for the application."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration.

        Args:
            config_path: Path to config.yaml file. If None, uses default location.
        """
        if config_path is None:
            # Default to config.yaml in project root
            self.config_path = Path(__file__).parent.parent / "config.yaml"
        else:
            self.config_path = Path(config_path)

        self._config = self._load_config()
        self._setup_directories()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def _setup_directories(self):
        """Ensure required directories exist."""
        base_dir = self.config_path.parent

        # Create data directories
        data_dir = base_dir / "data"
        (data_dir / "papers").mkdir(parents=True, exist_ok=True)
        (data_dir / "outputs").mkdir(parents=True, exist_ok=True)

        # Create logs directory
        logs_dir = base_dir / "logs"
        logs_dir.mkdir(parents=True, exist_ok=True)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation.

        Args:
            key: Configuration key (e.g., 'database.path')
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self._config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value

    @property
    def database_path(self) -> Path:
        """Get absolute path to database."""
        db_path = self.get('database.path', 'data/knowledge_base.db')
        base_dir = self.config_path.parent
        return base_dir / db_path

    @property
    def papers_dir(self) -> Path:
        """Get path to papers directory."""
        base_dir = self.config_path.parent
        return base_dir / "data" / "papers"

    @property
    def outputs_dir(self) -> Path:
        """Get path to outputs directory."""
        base_dir = self.config_path.parent
        return base_dir / "data" / "outputs"

    @property
    def summary_brief_tokens(self) -> int:
        """Get brief summary token limit."""
        return self.get('processing.summary_brief_tokens', 250)

    @property
    def summary_detailed_tokens(self) -> int:
        """Get detailed summary token limit."""
        return self.get('processing.summary_detailed_tokens', 1000)

    @property
    def max_context_tokens(self) -> int:
        """Get maximum context tokens."""
        return self.get('context.max_tokens', 200000)

    @property
    def min_papers_for_review(self) -> int:
        """Get minimum papers required for review."""
        return self.get('generation.min_papers_for_review', 20)

    def __repr__(self) -> str:
        return f"Config(config_path='{self.config_path}')"


# Global configuration instance
_config_instance: Optional[Config] = None


def get_config(config_path: Optional[str] = None) -> Config:
    """
    Get global configuration instance.

    Args:
        config_path: Optional path to config file

    Returns:
        Config instance
    """
    global _config_instance

    if _config_instance is None:
        _config_instance = Config(config_path)

    return _config_instance


def reload_config(config_path: Optional[str] = None):
    """
    Reload configuration from file.

    Args:
        config_path: Optional path to config file
    """
    global _config_instance
    _config_instance = Config(config_path)
