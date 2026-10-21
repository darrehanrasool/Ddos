"""Data quality profiling and auditing report generator."""

from dataclasses import dataclass, field
from typing import Dict, Any, List
import pandas as pd
import numpy as np


@dataclass
class QualityProfile:
    """Statistical summary of dataset quality."""
    total_records: int
    total_features: int
    duplicate_rows: int
    missing_cells: int
    infinite_cells: int
    zero_variance_features: List[str] = field(default_factory=list)
    class_distribution: Dict[str, int] = field(default_factory=dict)
    memory_usage_mb: float = 0.0


class DataQualityAuditor:
    """Performs deep quality audits over network flow data."""

    @staticmethod
    def audit(df: pd.DataFrame, target_col: str = "Label") -> QualityProfile:
        total_rows = len(df)
        total_features = len(df.columns)
        duplicates = int(df.duplicated().sum())

        numeric_df = df.select_dtypes(include=[np.number])
        missing = int(df.isnull().sum().sum())
        inf_count = int(np.isinf(numeric_df.values).sum()) if not numeric_df.empty else 0

        # Find zero variance features
        zero_var = [col for col in numeric_df.columns if numeric_df[col].std() == 0]

        class_dist = {}
        detected_target = target_col
        if detected_target not in df.columns:
            for cand in ["Label", "label", "attack_type", "type", "category", "attack_class", "class"]:
                if cand in df.columns:
                    detected_target = cand
                    break

        if detected_target in df.columns:
            class_dist = df[detected_target].value_counts().to_dict()

        mem_mb = round(df.memory_usage(deep=True).sum() / (1024**2), 2)

        return QualityProfile(
            total_records=total_rows,
            total_features=total_features,
            duplicate_rows=duplicates,
            missing_cells=missing,
            infinite_cells=inf_count,
            zero_variance_features=zero_var,
            class_distribution=class_dist,
            memory_usage_mb=mem_mb,
        )
