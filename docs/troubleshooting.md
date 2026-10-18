# Troubleshooting & Common Issues Guide

## 1. Memory Issues (Out-of-Memory / OOM)
- **Symptom**: `RuntimeError: CUDA out of memory` or system RAM exhaustion during large CSV loading.
- **Resolution**:
  1. Reduce `training.batch_size` in `configs/training.yaml` from 512 to 128 or 64.
  2. Enable chunked processing in `scripts/prepare_data.py` (via `--chunksize 50000`).
  3. Set `ACCELERATOR=mps` or `ACCELERATOR=cpu` in `.env` if GPU VRAM is constrained.

## 2. Missing Values or Infinite Floats in Flow Data
- **Symptom**: `ValueError: Input contains NaN, infinity or a value too large for dtype('float64')`.
- **Cause**: CICFlowMeter computes `Flow Bytes/s = bytes / duration`. When duration is 0, division by zero creates `+inf`.
- **Resolution**: `src/ddos_ai/data/preprocessing.py` automatically detects and clips $\pm\infty$ to the 99.9th percentile value before running scalers.

## 3. Dataset Download Failures
- **Symptom**: Connection timeout or SSL verification failure when attempting to download full benchmark datasets from academic servers.
- **Resolution**:
  1. Use `--mode sample` to run automated verification on deterministic synthetic flow captures.
  2. For full dataset downloads, pass custom academic mirror URLs via `--mirror-url` or use Kaggle CLI integration.

## 4. PyTorch MPS (Apple Silicon) Compatibility
- **Symptom**: `UserWarning: The operator 'aten::...' is not currently implemented for the MPS device`.
- **Resolution**: Set `export PYTORCH_ENABLE_MPS_FALLBACK=1` in your environment or set `preferred_device: "cpu"` in `configs/hardware.yaml`.
