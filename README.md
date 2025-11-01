# Meta Synthetic Architecture (MSA) Reference Repository

This repository accompanies the *Meta Synthetic Architecture* whitepaper
and now includes a lightweight reference implementation, experiment
scaffolding, and supplementary documentation that make the proposal more
accessible to collaborators.

## Repository Contents

- `docs/halenta-meta-synthetic-architecture-(MSA)-2025-10-12-v1.3.pdf` – the
  original whitepaper.
- `docs/primer.md` – implementation-focused summary of the MSA concepts.
- `docs/research_landscape.md` – overview of adjacent research areas and
  suggested collaboration paths.
- `msa_reference/` – Python package implementing the meta-coordination loop
  from Appendix B (context manager, meta coordinator, knowledge base, example
  subsystems, and a synthetic experiment harness).
- `experiments/` – scripts to run the synthetic forgetting benchmark described
  in Appendix C, producing JSON reports for baseline vs. MSA comparisons.
- `examples/run_demo.py` – quick-start CLI that executes the synthetic
  experiment and prints headline metrics.

## Getting Started

1. Create a Python 3.9+ environment.
2. Install the repository in editable mode (optional but convenient):

   ```bash
   pip install -e .
   ```

   The project has no external dependencies beyond the Python standard library.

3. Run the demo experiment:

   ```bash
   python examples/run_demo.py --contexts 8 --seed 42
   ```

   The script reports forgetting rates, coherence improvements, and conflict
   reductions for the baseline and MSA runs.

4. Explore the experiment pipeline:

   ```bash
   python experiments/synthetic_forgetting/run_pipeline.py --contexts 8 --seed 42
   ```

   Results are written to `experiments/results/latest_run.json` for further
   analysis (e.g., in a notebook).

## Extending the Prototype

- Swap out the synthetic task generator in `msa_reference.simulation` with
  loaders for real benchmarks to validate the architecture on complex domains.
- Enrich the knowledge base to store structured artefacts (graphs, vectors,
  embeddings) and adapt the coherence metrics accordingly.
- Instrument the `MetaCoordinator` to emit telemetry for dashboards,
  supporting the auditing and escalation hooks discussed in Section 11 of the
  whitepaper.

## License

The repository is distributed under the terms of the MIT License.  See
[`LICENSE`](LICENSE) for details.
