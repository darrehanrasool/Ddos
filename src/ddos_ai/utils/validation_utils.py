"""Array and tensor numerical sanity validation."""

import numpy as np


def check_finite_array(arr: np.ndarray, name: str = "Array") -> bool:
    """Verifies that an array does not contain NaN or infinite values."""
    if not np.all(np.isfinite(arr)):
        nan_count = int(np.isnan(arr).sum())
        inf_count = int(np.isinf(arr).sum())
        raise ValueError(f"{name} contains invalid values! NaNs: {nan_count}, Infs: {inf_count}")
    return True
