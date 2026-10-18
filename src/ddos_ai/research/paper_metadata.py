"""Paper metadata model container."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class PaperMetadata:
    """Metadata schema for peer-reviewed and preprint research papers."""
    paper_id: str
    title: str
    authors: List[str]
    year: int
    venue: str
    dataset: str
    architecture: str
    accuracy: float
    f1_score: float
    pdf_path: str
    arxiv_id: Optional[str] = None
    doi: Optional[str] = None
    key_contribution: str = ""
