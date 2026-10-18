"""Evaluation subsystem for metrics computation, statistical analysis, and model comparison."""

from ddos_ai.evaluation.metrics import compute_comprehensive_metrics
from ddos_ai.evaluation.evaluation import Evaluator
from ddos_ai.evaluation.statistical_analysis import mcnemar_test, wilcoxon_signed_rank_test
from ddos_ai.evaluation.model_comparison import compare_models

__all__ = [
    "compute_comprehensive_metrics",
    "Evaluator",
    "mcnemar_test",
    "wilcoxon_signed_rank_test",
    "compare_models",
]
