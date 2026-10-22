# Release scope and checks

Includes activation extraction, random-direction controls, clustered bootstrap
intervals, held-out and noise baselines, and a public 824-observation bundle.
The exact 824 extraction-input transcripts are included separately and verified against
all six cache manifests. Full episode directories and base-model weights remain
separate; see [DATA.md](DATA.md).
The optional historical-run importer retains prompt reconstruction and strict matching,
with its required text templates, but no generation runner or execution sandbox.

Validation uses Python 3.13 and `requirements-tested.txt`: CPU tests for pooling,
matching, ties, sign symmetry, token alignment and prompt reconstruction; cached
256/2,000-direction reanalysis matching the archived statistics; held-out and noise
checks. Both distributions build. This verifies reanalysis of fixed observations,
not independent data collection or hacking-label adjudication. The package is
`axis_rh`; it can coexist with `soo_experiments`. Original/released file hashes are
recorded in `SOURCE_MANIFEST.json`.
