"""File system helper functions."""

from pathlib import Path
from typing import Union
import pandas as pd


def ensure_dir(path: Union[str, Path]) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def safe_read_csv(path: Union[str, Path], **kwargs) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")
    return pd.read_csv(p, **kwargs)


def safe_write_csv(df: pd.DataFrame, path: Union[str, Path], **kwargs) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(p, index=False, **kwargs)
    return p
