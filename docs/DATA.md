# Observation data

The [public MIT-licensed bundle](https://huggingface.co/datasets/Arkonyx/assistant-axis-reward-hacking)
contains 824 GPT-OSS-120B observations, six activation-cache shards and the Assistant
Axis tensor (27 MB compressed). It retains verdicts, matching strata and token counts;
generated code is removed from this compact bundle. Exact extraction transcripts are
now available in a separate archive below; base-model weights remain separate.
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

The compact observation bundle supports fixed-cohort statistical reanalysis. The
separate recovered transcripts below also allow inspection of the supplied context
and selected responses, and provide the exact input bytes for repeating extraction. “Unflagged” is not a
judge-confirmed negative label. The original coding-run importer
(`axis_rh.correlation.rh_hillclimb`) is optional provenance tooling for the original run
layout; its required cohort run data, worklists and reasoning sidecars are now in the
[episode archive](EPISODES.md).
The recovered extraction inputs bypass that importer. Public
cache analysis does not depend on it. Its prompt helpers are tested with synthetic inputs.

To rebuild reduced metadata from complete source caches, use
`scripts/prepare_observations.py --help`. That exporter preserves scoring inputs and
writes a checksum manifest; it performs no upload.

## Recovered extraction transcripts

[`published/extraction-transcripts.jsonl.gz`](../published/extraction-transcripts.jsonl.gz)
contains the original 824-record extraction-input JSONL (5.9 MB compressed, 25 MB
uncompressed). Its uncompressed SHA-256 exactly matches `transcripts_sha256` in all
six published cache manifests. No transcript bytes were changed. It includes the
messages supplied for each selected turn, raw response with channel markers, generated
code and recorded verdict. This is a collection of extraction inputs, not the full
archive of every run or execution environment. A [separate episode archive](EPISODES.md)
now includes the contributing episodes, source settings and recorded judge explanations.

```bash
python scripts/verify_transcripts.py
# After downloading the observation bundle, additionally check the six actual shards:
python scripts/verify_transcripts.py --cache artifacts/cache
# Write a new file for the README's GPU extraction command:
python scripts/verify_transcripts.py --output artifacts/transcripts.jsonl
```

The output path must not already exist. The verifier checks compressed and uncompressed
checksums and joins all 824 IDs/turns/outcomes to the published observation index.
`published/transcript-manifest.json` pins the hashes; `transcript-observations.json`
contains the corresponding previously published scoring metadata.

Readers can now inspect the text and code behind recorded verdicts. A matching verdict
is still not independent adjudication: the episode archive adds the original recorded judge explanations and saved test
results, but not every judge API request or a frozen executable environment, and unflagged observations are
not judge-confirmed negatives. Repeating activation extraction additionally requires
the pinned model and compatible hardware/software. No new GPU extraction or judging
was performed for this recovery.
