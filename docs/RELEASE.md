# Release provenance and validation

Prepared October 21, 2026 from the original research implementation.
The control-analysis worktree also held
uncommitted control code; comparison confirmed that the extraction, matching and record
modules had already reached the main branch unchanged. This release uses the main
branch's later analysis implementation, including per-direction bootstrap intervals
and the held-out mean-difference analysis. Full original file hashes are recorded in
`SOURCE_MANIFEST.json`.

Packaging changes:

- Extracted the control/statistics pipeline and its required matching, tokenization,
  measurement and transcript-reconstruction helpers.
- Retained token-alignment and classification functions while removing their imports
  of unrelated experiment runners. Function bodies are preserved.
- Removed cluster-dependent import side effects and made scratch paths configurable.
- Added extraction switches for offline caches, attention implementation and device map.
  The attention default now follows Transformers; original kernel selection remains
  available explicitly. These changes do not affect reanalysis of saved activations.
- Forwarded model revision/cache options to configuration loading.
- Gave the original noise experiment a path-based CLI and added a small CLI for its
  existing held-out baseline estimator.
- Added dependency metadata, MIT licensing, preserved notices, source hashes, archived
  aggregate statistics and a data-driven plotting script.

Validation uses Python 3.13.7 and `requirements-tested.txt`. All 15 original selected
tests pass, including tiny-model activation pooling, exact ties, sign symmetry,
strict matching, problem-clustered bootstrap intervals, leave-one-problem-out fitting,
and a synthetic-cache end-to-end analysis.

The 256- and 2,000-direction analyses were also rerun on all six original cache shards
(824 observations). Their aggregate outputs are committed under `published/validated-*`.
The held-out final-answer AUROC is 0.928571. The noise experiment reproduces an in-sample
direction AUROC of 0.938 before noise and 0.914 at the post's noise setting, with random
direction 2.5/97.5 percentiles of 0.407/0.588. See `published/held-out.json` and
`published/noise-check.txt`.

The raw cache is copied locally under ignored `artifacts/` for validation and is not
in the release. No GPU jobs, model generation, or original data collection were rerun.
Tests and cached analyses establish code behavior and numerical reproduction from
existing inputs, not an independent replication of data collection.

Both wheel and source distributions build successfully with `uv build`.
