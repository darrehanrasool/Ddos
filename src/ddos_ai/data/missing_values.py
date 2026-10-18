"""Missing value imputation strategies for network traffic flows."""

from typing import Dict, Any, Optional
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


class MissingValueHandler:
    """Handles missing values (NaN) and infinities in network flow features."""

    def __init__(self, strategy: str = "median"):
        self.strategy = strategy
        self.imputation_values_: Dict[str, float] = {}

    def fit(self, df: pd.DataFrame) -> "MissingValueHandler":
        """Computes imputation values across numerical columns from training set."""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            clean_series = df[col].replace([np.inf, -np.inf], np.nan).dropna()
            if len(clean_series) > 0:
                if self.strategy == "mean":
                    val = float(clean_series.mean())
                elif self.strategy == "zero":
                    val = 0.0
                else:  # default: median
                    val = float(clean_series.median())
            else:
                val = 0.0
            self.imputation_values_[col] = val
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applies imputation values and replaces infinities with max valid bounds."""
        df_out = df.copy()
        numeric_cols = df_out.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            fill_val = self.imputation_values_.get(col, 0.0)
            # Replace infinity with NaN then fill with learned median/mean
            df_out[col] = df_out[col].replace([np.inf, -np.inf], np.nan).fillna(fill_val)

        return df_out

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.fit(df).transform(df)
