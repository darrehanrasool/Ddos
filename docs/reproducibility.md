# Reproducibility Guide & Benchmark Auditability

## 1. Deterministic Seeding Protocol
To guarantee exact numerical replication across hardware architectures, DDoS-AI enforces seed configuration across all random number generators via `src/ddos_ai/core/reproducibility.py`:

```python
from ddos_ai.core.reproducibility import set_seed

set_seed(42, deterministic_torch=True)
```
This executes:
1. `random.seed(seed)`
2. `np.random.seed(seed)`
3. `torch.manual_seed(seed)`
4. `torch.cuda.manual_seed_all(seed)` (if CUDA available)
5. `torch.backends.cudnn.deterministic = True`
6. `torch.backends.cudnn.benchmark = False`
7. Sets environment variable `PYTHONHASHSEED = str(seed)`

## 2. Environment Specifications
- Canonical reference runs recorded using Python 3.12 / 3.14 on macOS (Apple M-series) and Ubuntu 22.04 LTS (NVIDIA Ampere / Hopper).
- All dependencies locked with explicit semantic version constraints in `requirements.txt` and `pyproject.toml`.

## 3. Dataset Integrity Manifests
- Every raw dataset archive is verified against expected SHA-256 digests stored in `data/manifests/dataset_manifest.json`.
- Flow feature normalization parameters (medians, IQR scales) are serialized to `models/preprocessors/` ensuring deterministic evaluation on unseen test datasets.
