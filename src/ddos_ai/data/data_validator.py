"""Data validation and schema integrity enforcement."""

from typing import List, Tuple
import pandas as pd
import numpy as np
import logging

from ddos_ai.core.constants import DEFAULT_FEATURE_COLUMNS, TARGET_COLUMN
from ddos_ai.core.exceptions import DataValidationError

logger = logging.getLogger(__name__)


class DataValidator:
    """Validates network flow dataframes against expected schema and bounds."""

    def __init__(self, required_features: List[str] = DEFAULT_FEATURE_COLUMNS, target: str = TARGET_COLUMN):
        self.required_features = required_features
        self.target = target

    def validate_schema(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """Checks for missing required features and target column."""
        # Normalize column names by stripping spaces
        clean_cols = [c.strip() for c in df.columns]
        missing = []

        if self.target not in clean_cols:
            missing.append(self.target)

        for col in self.required_features:
            if col not in clean_cols:
                missing.append(col)

        is_valid = len(missing) == 0
        if not is_valid:
            logger.warning(f"Data schema validation failed. Missing {len(missing)} columns: {missing[:5]}...")
        return is_valid, missing

    def check_infinite_values(self, df: pd.DataFrame) -> int:
        """Returns the total count of positive or negative infinity values in numerical columns."""
        numeric_df = df.select_dtypes(include=[np.number])
        inf_count = np.isinf(numeric_df.values).sum()
        if inf_count > 0:
            logger.info(f"Found {inf_count} infinite values in flow dataframe.")
        return int(inf_count)

    def check_null_values(self, df: pd.DataFrame) -> int:
        """Returns the total count of NaN/null values in dataframe."""
        null_count = df.isnull().sum().sum()
        if null_count > 0:
            logger.info(f"Found {null_count} null/missing values in flow dataframe.")
        return int(null_count)
