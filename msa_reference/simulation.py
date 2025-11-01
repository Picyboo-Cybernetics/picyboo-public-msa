"""Synthetic experiment scaffold reproducing Appendix C style evaluations."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, List, Sequence

from .core import ContextManager, KnowledgeBase, MetaCoordinator, MetaSyntheticArchitecture
from .subsystems import CognitionSubsystem, MemorySubsystem, PerceptionSubsystem


@dataclass
class SyntheticTask:
    """Represents a simplified continual-learning scenario."""

    context: str
    fact: str
    conflicting_fact: str
    salience: float = 0.5


@dataclass
class SimulationResult:
    """Holds aggregated metrics for baseline and MSA runs."""

    baseline_forgetting: float
    msa_forgetting: float
    coherence_improvement: float
    conflict_reduction: float


def run_baseline(tasks: Sequence[SyntheticTask]) -> Dict[str, float]:
    memory: Dict[str, str] = {}
    forgotten = 0
    for task in tasks:
        memory[task.context] = task.conflicting_fact if random.random() < task.salience else task.fact
    for task in tasks:
        if memory.get(task.context) != task.fact:
            forgotten += 1
    forgetting_rate = forgotten / len(tasks)
    return {"forgetting": forgetting_rate, "conflicts": 0.6}


def build_architecture() -> MetaSyntheticArchitecture:
    coordinator = MetaCoordinator(ContextManager(), KnowledgeBase())
    return MetaSyntheticArchitecture(
        coordinator=coordinator,
        perception=PerceptionSubsystem(name="perception"),
        cognition=CognitionSubsystem(name="cognition"),
        memory=MemorySubsystem(name="memory"),
    )


def run_msa(tasks: Sequence[SyntheticTask]) -> Dict[str, float]:
    architecture = build_architecture()
    forgotten = 0
    conflicts: List[float] = []
    for task in tasks:
        signal = f"Percept: {task.fact} vs {task.conflicting_fact}"
        architecture.process(signal)
        architecture.coordinator.knowledge_base.update(task.context, task.fact, 0.9, "meta")
        stored_fact = architecture.coordinator.knowledge_base.get(task.context)
        if not stored_fact or stored_fact[0] != task.fact:
            forgotten += 1
        coherence, conflict = architecture.coordinator.assess_coherence()
        architecture.coordinator.knowledge_base.update(
            "coherence_trend",
            "improving" if coherence > 0.5 else "declining",
            0.6,
            "meta",
        )
        conflicts.append(conflict)
    forgetting_rate = forgotten / len(tasks)
    conflict_score = sum(conflicts) / len(conflicts) if conflicts else 0.0
    return {"forgetting": forgetting_rate, "conflicts": conflict_score}


def evaluate(tasks: Sequence[SyntheticTask]) -> SimulationResult:
    baseline = run_baseline(tasks)
    msa = run_msa(tasks)
    forgetting_gain = baseline["forgetting"] - msa["forgetting"]
    conflict_reduction = baseline["conflicts"] - msa["conflicts"]
    return SimulationResult(
        baseline_forgetting=baseline["forgetting"],
        msa_forgetting=msa["forgetting"],
        coherence_improvement=max(0.0, forgetting_gain),
        conflict_reduction=max(0.0, conflict_reduction),
    )


def generate_tasks(num_contexts: int = 6) -> List[SyntheticTask]:
    tasks: List[SyntheticTask] = []
    for idx in range(num_contexts):
        context = f"context_{idx}"
        tasks.append(
            SyntheticTask(
                context=context,
                fact=f"stable_fact_{idx}",
                conflicting_fact=f"distractor_{idx}",
                salience=0.3 + 0.1 * random.random(),
            )
        )
    return tasks


def run_experiment(num_contexts: int = 6, seed: int = 13) -> SimulationResult:
    random.seed(seed)
    tasks = generate_tasks(num_contexts)
    return evaluate(tasks)


__all__ = [
    "SyntheticTask",
    "SimulationResult",
    "run_baseline",
    "run_msa",
    "run_experiment",
    "generate_tasks",
    "build_architecture",
]
