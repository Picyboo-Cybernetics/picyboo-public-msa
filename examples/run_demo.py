"""CLI entry point to run the synthetic MSA experiment."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure the repository root is on the Python path when the script is executed
# directly via `python examples/run_demo.py`.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from msa_reference.simulation import run_experiment


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the MSA synthetic experiment demo")
    parser.add_argument("--contexts", type=int, default=6, help="Number of contexts to simulate")
    parser.add_argument("--seed", type=int, default=13, help="Random seed for reproducibility")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_experiment(num_contexts=args.contexts, seed=args.seed)
    print("Baseline forgetting rate: {:.2f}".format(result.baseline_forgetting))
    print("MSA forgetting rate: {:.2f}".format(result.msa_forgetting))
    print("Coherence improvement: {:.2f}".format(result.coherence_improvement))
    print("Conflict reduction: {:.2f}".format(result.conflict_reduction))


if __name__ == "__main__":
    main()
