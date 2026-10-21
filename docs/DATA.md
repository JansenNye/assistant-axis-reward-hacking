# Observation data

The [public MIT-licensed bundle](https://huggingface.co/datasets/Arkonyx/assistant-axis-reward-hacking)
contains 824 GPT-OSS-120B observations, six activation-cache shards and the Assistant
Axis tensor (27 MB compressed). It retains verdicts, matching strata and token counts;
generated code is removed. Full conversations and base-model weights are not included.
Koby Lewis developed the extraction/reward-hacking setup; Jansen Nye ran the controls.

From the repository root:

```bash
hf download Arkonyx/assistant-axis-reward-hacking --repo-type dataset \
  --revision 3bd85dd4126fef62dd8607c18805805588d4d5d4 \
  assistant-axis-observations.tar.gz SHA256SUMS \
  --local-dir outputs/observation-download
(cd outputs/observation-download && sha256sum -c SHA256SUMS)
tar -xzf outputs/observation-download/assistant-axis-observations.tar.gz
```

Everything extracts under `artifacts/`. The pinned revision and archive SHA-256 are
in [`published/observation-artifact.json`](../published/observation-artifact.json).
`artifacts/OBSERVATION_MANIFEST.json` lists file hashes relative to the repository root.
Run the README's CPU reanalysis commands after extraction.

## File formats

| Input | Contents |
|---|---|
| Axis | Trusted PyTorch tensor `(36, 2880)`, or mapping with `axis` and `model`. Selected layer directions are normalized. Shape alone does not prove construction provenance. |
| Shard `manifest.json` | Model/revision, extraction-input hash, layers, shard count/index, expected rows, software versions, dimensions and completion state. |
| Shard `records.jsonl` | Observation ID, status, outcome verdict/label/problem/stratum, prompt/region token counts and relative residual file path. |
| `residuals/*.npz` | Float32 `layer_17` array `(3, 2880)`: prompt, reasoning, final region means. Missing regions use NaNs. |
| Transcripts for new extraction | JSONL with `example_id`, `scenario`, `turn`, `messages`, `chat_kwargs`, `raw_response` (channel markers retained), `truncated`, and `outcome`. See `TranscriptRecord` in `src/axis_rh/correlation/records.py`. |

A stratum preserves problem, protocol, run family and turn. The analyzer rejects missing
or duplicate shards and smoke-test caches. Exact token alignment excludes control markers
and the last unprocessed response token. The transcript hash in a manifest identifies
original extraction inputs, not the reduced metadata file.

These inputs support fixed-cohort statistical reanalysis. They do not support independently
rejudging hacking or repeating extraction without the conversations. “Unflagged” is not a
judge-confirmed negative label. The original coding-run importer
(`axis_rh.correlation.rh_hillclimb`) is optional provenance tooling for the original run
layout; it requires run data, worklists and reasoning sidecars not included here. Public
cache analysis does not depend on it. Its prompt helpers are tested with synthetic inputs.

To rebuild reduced metadata from complete source caches, use
`scripts/prepare_observations.py --help`. That exporter preserves scoring inputs and
writes a checksum manifest; it performs no upload.
