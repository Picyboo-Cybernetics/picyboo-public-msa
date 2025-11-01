"""Example subsystem implementations used in the MSA reference prototype."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from .core import KnowledgeBase


@dataclass
class BaseSubsystem:
    name: str
    confidence: float = 0.7

    def process(self, *_args, **_kwargs) -> Dict[str, str]:
        raise NotImplementedError


@dataclass
class PerceptionSubsystem(BaseSubsystem):
    """Extracts salient tokens from the incoming signal."""

    def process(self, signal: str, *_args, **_kwargs) -> Dict[str, str]:
        signal = signal.lower()
        tokens = {
            "dominant_modality": "visual" if "see" in signal else "textual",
            "salient_entity": "memory" if "memory" in signal else "observation",
        }
        if "anomaly" in signal:
            tokens["alert_state"] = "high"
            self.confidence = 0.9
        else:
            self.confidence = 0.6
        return tokens


@dataclass
class CognitionSubsystem(BaseSubsystem):
    """Produces interpretations conditioned on the knowledge base."""

    confidence: float = 0.75

    def process(self, percepts: Dict[str, str], kb: KnowledgeBase) -> Dict[str, str]:
        interpretation = {
            "situation": f"Assessing {percepts.get('salient_entity', 'signal')}",
            "recommended_context": "reflect" if percepts.get("salient_entity") == "memory" else "default",
        }
        if kb.get("last_resolution"):
            interpretation["leveraging_memory"] = "true"
            self.confidence = 0.8
        else:
            self.confidence = 0.7
        return interpretation


@dataclass
class MemorySubsystem(BaseSubsystem):
    """Updates episodic traces and emits reminders to the coordinator."""

    confidence: float = 0.8

    def process(self, cognition: Dict[str, str], kb: KnowledgeBase) -> Dict[str, str]:
        episode = cognition.get("situation", "undetermined")
        kb.update("last_episode", episode, 0.7, self.name)
        reminder = {
            "last_resolution": cognition.get("recommended_context", "default"),
            "stability": "improving" if kb.get("coherence_trend") else "unknown",
        }
        self.confidence = 0.85 if reminder["stability"] == "improving" else 0.6
        return reminder


__all__ = [
    "BaseSubsystem",
    "PerceptionSubsystem",
    "CognitionSubsystem",
    "MemorySubsystem",
]
