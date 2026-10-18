"""Data preprocessing, scaling, and categorical label encoding."""

import pickle
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler, StandardScaler, MinMaxScaler, LabelEncoder
import logging

from ddos_ai.core.constants import TARGET_COLUMN
from ddos_ai.data.missing_values import MissingValueHandler

logger = logging.getLogger(__name__)


class Preprocessor:
    """End-to-end data preprocessor ensuring leakage-free feature scaling and label encoding."""

    def __init__(
        self,
        scaler_type: str = "robust",
        handle_missing: str = "median",
        target_col: str = TARGET_COLUMN,
    ):
        self.scaler_type = scaler_type
        self.handle_missing = handle_missing
        self.target_col = target_col

        if scaler_type == "standard":
            self.scaler = StandardScaler()
        elif scaler_type == "minmax":
            self.scaler = MinMaxScaler()
        else:
            self.scaler = RobustScaler()

        self.missing_handler = MissingValueHandler(strategy=handle_missing)
        self.label_encoder = LabelEncoder()
        self.feature_columns_: List[str] = []
        self.is_fitted: bool = False

    def clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Strips whitespace and standardizes column names."""
        df_out = df.copy()
        df_out.columns = [c.strip() for c in df_out.columns]
        return df_out

    def fit(self, df: pd.DataFrame) -> "Preprocessor":
        """Fits missing value imputers and numerical scalers exclusively on training data."""
        df_clean = self.clean_column_names(df)

        # Fit missing values
        self.missing_handler.fit(df_clean)
        df_imputed = self.missing_handler.transform(df_clean)

        # Separate feature columns from target
        self.feature_columns_ = [
            c for c in df_imputed.select_dtypes(include=[np.number]).columns
            if c != self.target_col
        ]

        if self.feature_columns_:
            self.scaler.fit(df_imputed[self.feature_columns_])

        # Fit label encoder
        if self.target_col in df_clean.columns:
            labels = df_clean[self.target_col].astype(str)
            self.label_encoder.fit(labels)

        self.is_fitted = True
        logger.info(f"Preprocessor fitted across {len(self.feature_columns_)} numerical features.")
        return self

    def transform(self, df: pd.DataFrame) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """Transforms input DataFrame into scaled feature matrix X and encoded target vector y."""
        if not self.is_fitted:
            raise RuntimeError("Preprocessor must be fitted before calling transform().")

        df_clean = self.clean_column_names(df)
        df_imputed = self.missing_handler.transform(df_clean)

        X = self.scaler.transform(df_imputed[self.feature_columns_])

        y = None
        if self.target_col in df_clean.columns:
            labels = df_clean[self.target_col].astype(str)
            # Handle any unseen labels during testing safely
            unseen = set(labels) - set(self.label_encoder.classes_)
            if unseen:
                logger.warning(f"Unseen labels detected: {unseen}. Mapping to standard class.")
                labels = labels.apply(lambda x: x if x in self.label_encoder.classes_ else self.label_encoder.classes_[0])
            y = self.label_encoder.transform(labels)

        return X, y

    def fit_transform(self, df: pd.DataFrame) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        return self.fit(df).transform(df)

    def save(self, output_path: Union[str, Path]) -> None:
        """Serializes fitted preprocessor to disk."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(self, f)
        logger.info(f"Preprocessor serialized to {path}")

    @staticmethod
    def load(input_path: Union[str, Path]) -> "Preprocessor":
        """Loads fitted preprocessor from disk."""
        with open(input_path, "rb") as f:
            return pickle.load(f)
