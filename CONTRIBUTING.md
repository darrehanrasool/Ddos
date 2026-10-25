# Contributing to DDoS-AI

Thank you for your interest in contributing to **DDoS-AI**! We welcome contributions from researchers, software engineers, academic peers, and open-source contributors to advance state-of-the-art AI-driven network security and intrusion prevention.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Academic Licensing & IP](#academic-licensing--ip)
3. [How to Contribute](#how-to-contribute)
   - [Reporting Bugs](#reporting-bugs)
   - [Suggesting Features & Enhancements](#suggesting-features--enhancements)
   - [Improving Documentation](#improving-documentation)
   - [Code Contributions](#code-contributions)
4. [Development Environment Setup](#development-environment-setup)
5. [Running Tests](#running-tests)
6. [Code Style & Best Practices](#code-style--best-practices)
7. [Git Commit & Pull Request Guidelines](#git-commit--pull-request-guidelines)
8. [Contributor Recognition](#contributor-recognition)

---

## Code of Conduct

All contributors and community participants are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it to ensure a respectful, professional, and productive research environment for everyone.

---

## Academic Licensing & IP

By contributing code, documentation, models, or data to DDoS-AI, you agree that your contributions will be licensed under the project's [Strict Academic & Non-Commercial Research Evaluation License](LICENSE). 

- All software is strictly intended for defensive cybersecurity research, academic reproducibility, and non-commercial evaluation.
- Derivative commercial use, proprietary resale, or packaging into closed commercial products is strictly prohibited.

---

## How to Contribute

### Reporting Bugs

Before creating a bug report, please check existing issues to verify that the problem hasn't already been reported.

When opening an issue, please include:
- A clear, descriptive title.
- Environment details: Operating system (macOS / Ubuntu / Linux), Python version (`python --version`), and hardware acceleration backend (CPU, MPS, CUDA).
- Clear, minimal step-by-step instructions to reproduce the issue.
- The complete stack trace and console output.
- Expected vs. actual behavior.

> **Note**: For security-sensitive issues or vulnerability reports, please follow our [Security Policy](SECURITY.md) and do not open a public issue.

### Suggesting Features & Enhancements

We are always eager to explore new architectural ideas, multi-dataset harmonizations, and novel mitigation mechanisms:
- Open an issue describing the proposed feature or improvement.
- Explain the scientific rationale, threat model, or operational benefit.
- Discuss how it integrates with the existing dual-tier cascading pipeline (Histogram-binned tree screening tier + Deep Residual Neural Network tier).

### Improving Documentation

High-quality documentation is vital for academic reproducibility:
- Corrections or clarifications in markdown documents (`docs/`, `guide.md`, `README.md`).
- Enhancing docstrings, architecture diagrams, or mathematical formulations.
- Adding reproducible tutorial notebooks or execution scripts.

---

## Development Environment Setup

### 1. Prerequisites
- **Python**: Version 3.10, 3.11, 3.12, or 3.14.
- **Git**: Version 2.30 or newer.
- **Operating System**: macOS (Apple Silicon / Intel) or Linux (Ubuntu 22.04 / 24.04 recommended).

### 2. Clone the Repository
```bash
git clone https://github.com/darrehanrasool/Ddos.git
cd Ddos
```

### 3. Set Up Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
# Upgrade pip, setuptools, and wheel
pip install --upgrade pip setuptools wheel

# Install core runtime dependencies
pip install -r requirements.txt

# Install development and testing dependencies
pip install -r requirements-dev.txt
```

---

## Running Tests

All contributions must pass the entire test suite before a Pull Request can be merged.

### Run Full Test Suite
```bash
PYTHONPATH=src pytest tests/ -v
```

### Run Tests with Coverage
```bash
PYTHONPATH=src pytest tests/ --cov=src/ddos_ai --cov-report=term-missing
```

### Run Specific Test Categories
```bash
# Unit tests only
PYTHONPATH=src pytest tests/unit/ -v

# Integration tests only
PYTHONPATH=src pytest tests/integration/ -v
```

> **Cross-Platform Note**: Network emulation and interface tests must account for operating system differences (e.g., macOS BSD loopback is `lo0`, whereas Linux loopback is `lo`).

---

## Code Style & Best Practices

To maintain code readability and maintainability:

1. **PEP 8 Compliance**: Follow standard Python conventions.
2. **Formatting**: Format code using `black` with standard line length:
   ```bash
   black src/ tests/
   ```
3. **Type Annotations**:
   - Annotate all function signatures and class attributes.
   - For backward compatibility with Python 3.10 and 3.11, explicitly import typing symbols (e.g., `from typing import Any, Dict, List, Optional, Tuple, Union`).
4. **Defensive Programming**:
   - Validate input tensor shapes, feature vectors, and network telemetry.
   - Avoid silent failures; use structured logging via `ddos_ai.core.logger` rather than raw `print()` statements.
5. **No Heavy or Extraneous Dependencies**:
   - Avoid adding heavy third-party libraries unless strictly necessary for scientific performance.

---

## Git Commit & Pull Request Guidelines

### Commit Messages

We follow the [Conventional Commits](https://www.conventionalcommits.org/) convention:

```
<type>(<scope>): <short summary>

[optional body explaining context, why the change was made, and architectural impact]
```

**Allowed Types**:
- `feat`: A new feature or capability.
- `fix`: A bug fix or runtime patch.
- `docs`: Documentation changes, papers, or markdown updates.
- `test`: Adding or modifying tests.
- `refactor`: Code changes that neither fix bugs nor add features.
- `perf`: Performance optimizations (e.g., latency reduction, memory optimization).
- `ci`: Changes to CI/CD workflows (`.github/workflows/`).

### Pull Request (PR) Process

1. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-description
   ```
2. **Make Changes & Add Tests**:
   Ensure all existing tests pass and add new unit/integration tests for your changes.
3. **Run Formatting & Verification**:
   ```bash
   black src/ tests/
   PYTHONPATH=src pytest tests/
   ```
4. **Push Branch & Open PR**:
   Push your branch to GitHub and open a Pull Request against the `main` branch.
5. **PR Description Checklist**:
   - [ ] Clear explanation of changes and their purpose.
   - [ ] Reference to any related issue (e.g., `Closes #12`).
   - [ ] Confirmation that all tests pass locally (`pytest tests/`).
   - [ ] Confirmation that code adheres to formatting standards (`black`).
   - [ ] No proprietary, credential, or sensitive data committed.

---

## Contributor Recognition

All accepted contributors will be recognized in our release notes and contributor lists. If your contribution involves novel scientific methodology or benchmark evaluation, you may be invited to collaborate on academic publications and technical reports.

Thank you for contributing to the **DDoS-AI** project!
