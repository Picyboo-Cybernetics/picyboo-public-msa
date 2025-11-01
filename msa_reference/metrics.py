"""Lightweight coherence and conflict scoring utilities."""

from math import sqrt
from typing import Iterable, Tuple

Observation = Tuple[str, str, float]


def coherence_score(observations: Iterable[Observation]) -> float:
    """Estimate coherence as normalised agreement between observations."""

    values = {}
    total_conf = 0.0
    for _, value, confidence in observations:
        values[value] = values.get(value, 0.0) + confidence
        total_conf += confidence
    if not values or total_conf == 0:
        return 1.0
    max_conf = max(values.values())
    return max_conf / total_conf


def conflict_rate(observations: Iterable[Observation]) -> float:
    """Measure diversity of reported values as a proxy for conflict."""

    counts = {}
    for _, value, _ in observations:
        counts[value] = counts.get(value, 0) + 1
    if not counts:
        return 0.0
    if len(counts) == 1:
        return 0.0
    total = sum(counts.values())
    # Gini-style impurity
    impurity = 1.0 - sum((c / total) ** 2 for c in counts.values())
    return sqrt(impurity)


__all__ = ["coherence_score", "conflict_rate"]
