"""Cryptographic hashing utilities."""

import hashlib
from pathlib import Path
from typing import Union


def compute_file_sha256(path: Union[str, Path]) -> str:
    """Computes hexadecimal SHA-256 hash of a file."""
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha.update(chunk)
    return sha.hexdigest()
