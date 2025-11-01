"""Reference prototype for the Meta Synthetic Architecture (MSA).

This package provides a minimal, didactic implementation of the
components described in Appendix B of the MSA whitepaper.  It is not
optimised for performance, but instead aims to make the architecture
concrete for researchers and practitioners who want to explore the
coordination patterns proposed in the paper.
"""

from .core import (  # noqa: F401
    MetaSyntheticArchitecture,
    MetaCoordinator,
    ContextManager,
    KnowledgeBase,
)
from .subsystems import (  # noqa: F401
    PerceptionSubsystem,
    CognitionSubsystem,
    MemorySubsystem,
)
from .metrics import (  # noqa: F401
    coherence_score,
    conflict_rate,
)

__all__ = [
    "MetaSyntheticArchitecture",
    "MetaCoordinator",
    "ContextManager",
    "KnowledgeBase",
    "PerceptionSubsystem",
    "CognitionSubsystem",
    "MemorySubsystem",
    "coherence_score",
    "conflict_rate",
]
