"""Stratified train, validation, and test data splitting."""

from pathlib import Path
from typing import Tuple
import pandas as pd
from sklearn.model_selection import train_test_split
import logging

from ddos_ai.core.constants import TARGET_COLUMN

logger = logging.getLogger(__name__)


class DataSplitter:
    """Executes leakage-free stratified splitting across train, validation, and test subsets."""

    def __init__(
        self,
        train_ratio: float = 0.70,
        val_ratio: float = 0.15,
        test_ratio: float = 0.15,
        random_state: int = 42,
        target_col: str = TARGET_COLUMN,
    ):
        self.train_ratio = train_ratio
        self.val_ratio = val_ratio
        self.test_ratio = test_ratio
        self.random_state = random_state
        self.target_col = target_col

        total = round(train_ratio + val_ratio + test_ratio, 4)
        if total != 1.0:
            raise ValueError(f"Split ratios must sum to 1.0 (got {total})")

    def split(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Performs two-stage stratified splitting with safe fallback for sparse classes."""
        stratify_col = None
        if self.target_col in df.columns:
            counts = df[self.target_col].value_counts()
            if (counts >= 2).all() and len(df) > 30:
                stratify_col = df[self.target_col]

        # Stage 1: Split train from temp (val + test)
        temp_ratio = self.val_ratio + self.test_ratio
        train_df, temp_df = train_test_split(
            df,
            test_size=temp_ratio,
            random_state=self.random_state,
            stratify=stratify_col,
            shuffle=True,
        )

        # Stage 2: Split temp into validation and test
        val_fraction_of_temp = self.val_ratio / temp_ratio
        temp_stratify = None
        if self.target_col in temp_df.columns:
            counts_temp = temp_df[self.target_col].value_counts()
            if (counts_temp >= 2).all() and len(temp_df) > 10:
                temp_stratify = temp_df[self.target_col]

        val_df, test_df = train_test_split(
            temp_df,
            test_size=(1.0 - val_fraction_of_temp),
            random_state=self.random_state,
            stratify=temp_stratify,
            shuffle=True,
        )

        logger.info(
            f"Dataset split complete: Train={len(train_df)} ({len(train_df)/len(df):.1%}), "
            f"Val={len(val_df)} ({len(val_df)/len(df):.1%}), Test={len(test_df)} ({len(test_df)/len(df):.1%})"
        )
        return train_df, val_df, test_df

    def save_splits(
        self,
        train_df: pd.DataFrame,
        val_df: pd.DataFrame,
        test_df: pd.DataFrame,
        output_dir: str = "data/splits",
    ) -> None:
        """Saves partitions to CSV files in respective split directories."""
        base_path = Path(output_dir)
        (base_path / "train").mkdir(parents=True, exist_ok=True)
        (base_path / "validation").mkdir(parents=True, exist_ok=True)
        (base_path / "test").mkdir(parents=True, exist_ok=True)

        train_path = base_path / "train" / "train_flows.csv"
        val_path = base_path / "validation" / "val_flows.csv"
        test_path = base_path / "test" / "test_flows.csv"

        train_df.to_csv(train_path, index=False)
        val_df.to_csv(val_path, index=False)
        test_df.to_csv(test_path, index=False)

        logger.info(f"Splits saved to {train_path}, {val_path}, {test_path}")
