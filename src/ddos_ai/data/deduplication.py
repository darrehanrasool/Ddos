"""Flow deduplication utility."""

import pandas as pd
import logging
from typing import Tuple

logger = logging.getLogger(__name__)


def remove_duplicate_flows(df: pd.DataFrame, subset_cols=None) -> Tuple[pd.DataFrame, int]:
    """Identifies and drops identical network flow duplicates.

    Args:
        df: Input DataFrame.
        subset_cols: Optional column list to check for duplicates.

    Returns:
        Tuple of (deduplicated DataFrame, count of removed duplicates).
    """
    initial_count = len(df)
    df_dedup = df.drop_duplicates(subset=subset_cols, keep="first")
    removed_count = initial_count - len(df_dedup)

    if removed_count > 0:
        logger.info(f"Removed {removed_count} duplicate flow records ({removed_count / initial_count:.2%}).")
    return df_dedup, removed_count
