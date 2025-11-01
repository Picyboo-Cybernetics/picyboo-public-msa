"""Core orchestration primitives for the MSA reference prototype."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Tuple

from .metrics import coherence_score, conflict_rate


@dataclass
class KnowledgeBase:
    """Stores facts produced by subsystems with simple provenance tracking."""

    facts: Dict[str, Tuple[str, float]] = field(default_factory=dict)

    def update(self, key: str, value: str, confidence: float, source: str) -> None:
        self.facts[key] = (value, confidence)

    def get(self, key: str) -> Optional[Tuple[str, float]]:
        return self.facts.get(key)

    def items(self) -> Iterable[Tuple[str, Tuple[str, float]]]:
        return self.facts.items()


@dataclass
class ContextManager:
    """Maintains contextual segments and provides lightweight scoring."""

    active_context: str = "default"
    context_history: List[str] = field(default_factory=lambda: ["default"])

    def switch(self, context: str) -> None:
        if context != self.active_context:
            self.active_context = context
            self.context_history.append(context)

    def suggest_context(self, signal: str) -> str:
        if "memory" in signal.lower():
            return "reflect"
        if "percept" in signal.lower():
            return "sense"
        return "default"


@dataclass
class MetaCoordinator:
    """Coordinates subsystem outputs and updates the knowledge base."""

    context_manager: ContextManager
    knowledge_base: KnowledgeBase
    coherence_window: List[Tuple[str, str, float]] = field(default_factory=list)
    window_size: int = 5

    def register_outputs(self, subsystem: str, outputs: Dict[str, str], confidence: float) -> None:
        for key, value in outputs.items():
            self.knowledge_base.update(key, value, confidence, subsystem)
            self.coherence_window.append((subsystem, value, confidence))
            if len(self.coherence_window) > self.window_size:
                self.coherence_window.pop(0)

    def assess_coherence(self) -> Tuple[float, float]:
        if not self.coherence_window:
            return 1.0, 0.0
        coherence = coherence_score(self.coherence_window)
        conflicts = conflict_rate(self.coherence_window)
        return coherence, conflicts

    def resolve_conflicts(self) -> None:
        coherence, conflicts = self.assess_coherence()
        if conflicts == 0:
            return
        # down-weight low confidence entries and favour majority values
        value_counts: Dict[str, float] = {}
        for subsystem, value, confidence in self.coherence_window:
            value_counts[value] = value_counts.get(value, 0.0) + confidence
        canonical_value = max(value_counts.items(), key=lambda item: item[1])[0]
        for key, (value, conf) in list(self.knowledge_base.items()):
            if value != canonical_value and conf < 0.6:
                self.knowledge_base.update(key, canonical_value, 0.6, "meta")
        self.context_manager.switch("reconciliation")


@dataclass
class MetaSyntheticArchitecture:
    """High-level container that orchestrates all subsystems."""

    coordinator: MetaCoordinator
    perception: "PerceptionSubsystem"
    cognition: "CognitionSubsystem"
    memory: "MemorySubsystem"

    def process(self, signal: str) -> Dict[str, str]:
        context_hint = self.coordinator.context_manager.suggest_context(signal)
        self.coordinator.context_manager.switch(context_hint)

        percept = self.perception.process(signal)
        cognition = self.cognition.process(percept, self.coordinator.knowledge_base)
        memory_outputs = self.memory.process(cognition, self.coordinator.knowledge_base)

        for subsystem_name, outputs, confidence in [
            ("perception", percept, self.perception.confidence),
            ("cognition", cognition, self.cognition.confidence),
            ("memory", memory_outputs, self.memory.confidence),
        ]:
            self.coordinator.register_outputs(subsystem_name, outputs, confidence)

        self.coordinator.resolve_conflicts()
        return {
            "context": self.coordinator.context_manager.active_context,
            "knowledge": dict(self.coordinator.knowledge_base.facts),
        }


__all__ = [
    "KnowledgeBase",
    "ContextManager",
    "MetaCoordinator",
    "MetaSyntheticArchitecture",
]
