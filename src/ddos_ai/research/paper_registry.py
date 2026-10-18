"""Paper registry loading downloaded paper catalogs."""

import json
from pathlib import Path
from typing import Dict, List, Optional
from ddos_ai.research.paper_metadata import PaperMetadata


class PaperRegistry:
    """Catalog of downloaded and indexed research papers."""

    def __init__(self, catalog_path: str = "papers/metadata/papers_metadata.json"):
        self.catalog_path = Path(catalog_path)
        self.papers: Dict[str, PaperMetadata] = {}
        self._load()

    def _load(self):
        if not self.catalog_path.exists():
            return
        with open(self.catalog_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data.get("papers", []):
                meta = PaperMetadata(
                    paper_id=item.get("id", ""),
                    title=item.get("title", ""),
                    authors=item.get("authors", []),
                    year=item.get("year", 2026),
                    venue=item.get("venue", "arXiv"),
                    dataset=item.get("dataset", ""),
                    architecture=item.get("architecture", ""),
                    accuracy=item.get("best_accuracy", 0.0),
                    f1_score=item.get("best_f1", 0.0),
                    pdf_path=item.get("pdf_path", ""),
                    arxiv_id=item.get("arxiv_id"),
                    doi=item.get("doi"),
                    key_contribution=item.get("key_contribution", ""),
                )
                self.papers[meta.paper_id] = meta

    def get_paper(self, paper_id: str) -> Optional[PaperMetadata]:
        return self.papers.get(paper_id)

    def list_papers(self) -> List[PaperMetadata]:
        return list(self.papers.values())
