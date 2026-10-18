"""Configuration loading, validation, and access module."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml
import logging

from ddos_ai.core.exceptions import ConfigurationError

logger = logging.getLogger(__name__)


@dataclass
class Config:
    """Master configuration container for DDoS-AI."""
    project: Dict[str, Any] = field(default_factory=dict)
    data: Dict[str, Any] = field(default_factory=dict)
    models: Dict[str, Any] = field(default_factory=dict)
    training: Dict[str, Any] = field(default_factory=dict)
    hardware: Dict[str, Any] = field(default_factory=dict)
    visualization: Dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default: Any = None) -> Any:
        parts = key.split(".")
        current = self.__dict__
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            elif hasattr(current, part):
                current = getattr(current, part)
            else:
                return default
            if current is None:
                return default
        return current


def load_yaml(file_path: Path) -> Dict[str, Any]:
    """Loads a single YAML configuration file."""
    if not file_path.exists():
        logger.warning(f"Config file not found at {file_path}, using empty dictionary.")
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = yaml.safe_load(f)
            return content or {}
    except Exception as e:
        raise ConfigurationError(f"Failed to parse YAML file {file_path}: {e}") from e


def load_config(config_dir: str = "configs") -> Config:
    """Loads and aggregates all YAML configuration files from the config directory.

    Args:
        config_dir: Path to directory containing project.yaml, data.yaml, etc.

    Returns:
        Consolidated Config object.
    """
    base_dir = Path(config_dir)
    return Config(
        project=load_yaml(base_dir / "project.yaml"),
        data=load_yaml(base_dir / "data.yaml"),
        models=load_yaml(base_dir / "models.yaml"),
        training=load_yaml(base_dir / "training.yaml"),
        hardware=load_yaml(base_dir / "hardware.yaml"),
        visualization=load_yaml(base_dir / "visualization.yaml"),
    )
