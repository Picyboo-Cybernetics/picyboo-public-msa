# Experimentation Overview

This directory contains lightweight scaffolding to replicate the evaluation
plan outlined in Appendix C of the MSA whitepaper.  The goal is to give
researchers and collaborators a concrete starting point for testing the
Meta Synthetic Architecture against simple continual-learning baselines.

## Structure

- `synthetic_forgetting/`: executable scripts and configuration for a toy
  continual-learning benchmark that contrasts a baseline learner with the
  MSA reference prototype.
- `results/`: (generated) location for experiment outputs.
- `notebooks/`: suggested place for interactive analysis.  Notebooks are not
  committed by default, but `.ipynb` files can be stored here when needed.

## Running the synthetic forgetting benchmark

```
python experiments/synthetic_forgetting/run_pipeline.py --contexts 8 --seed 42
```

The script will output aggregate forgetting rates and coherence metrics for
both the baseline and the MSA-enabled system.  Results are saved as JSON in
`experiments/results/latest_run.json` for downstream analysis.

## Extending the experiments

1. Replace the synthetic task generator in `msa_reference.simulation` with a
   loader that streams data from a real continual-learning benchmark (e.g.,
   Split-MNIST, CLRS tasks, RL environments).
2. Augment the `MetaSyntheticArchitecture` with richer coherence metrics or
   task-specific adapters.
3. Add visualisations by exporting the JSON results to notebooks in the
   `notebooks/` directory.

These steps align with Section 11 of the whitepaper, which calls for
iterative refinement across theoretical, empirical, and architectural tracks.
