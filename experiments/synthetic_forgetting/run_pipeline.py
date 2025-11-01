"""Command-line utility to run the synthetic forgetting benchmark."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from msa_reference.simulation import run_experiment


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Synthetic continual-learning benchmark")
    parser.add_argument("--contexts", type=int, default=6, help="Number of contexts to simulate")
    parser.add_argument("--seed", type=int, default=7, help="Random seed")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "results" / "latest_run.json",
        help="Where to store the JSON report",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_experiment(num_contexts=args.contexts, seed=args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "contexts": args.contexts,
        "seed": args.seed,
        "baseline_forgetting": result.baseline_forgetting,
        "msa_forgetting": result.msa_forgetting,
        "coherence_improvement": result.coherence_improvement,
        "conflict_reduction": result.conflict_reduction,
    }
    args.output.write_text(json.dumps(payload, indent=2))
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
