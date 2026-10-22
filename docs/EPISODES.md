# Recovered source episodes and judge records

The shared research archive retained the source records behind the published cohort.
`published/cohort-episodes.tar.gz` (23 MB) contains 686 contributing episodes,
their per-turn reasoning sidecars, the corresponding problem inputs and run settings,
217 recorded judge decisions with explanations, and the original v3 judging rubric.
These episodes contribute 824 observations because some episodes are scored at more
than one turn. The 217 judge rows are decisions, not 217 distinct positive examples:
some episodes were reviewed by multiple judges.

The original 89 judge-result files all match the hashes recorded when the cohort was
built. Rebuilding from the shared sources produces the exact published extraction
input. Rebuilding from this smaller release does too: all 824 transcripts match
byte-for-byte, including their ordering, prompts, responses, labels and strata.

## Verify and reconstruct

From the repository root, verify and extract with Python's standard library:

```bash
python scripts/verify_episodes.py
python scripts/verify_episodes.py --extract outputs/episodes
```

The extraction destination must not exist. To reconstruct the transcripts, install
this package with its declared dependencies and use Python 3.13 or later:

```bash
python -m axis_rh.correlation.rh_hillclimb \
  --root outputs/episodes/rh_hillclimb \
  --verdicts outputs/episodes/rh_hillclimb/verdicts/v3/*.jsonl \
  --strict-strata --out outputs/rebuilt-transcripts.jsonl
sha256sum outputs/rebuilt-transcripts.jsonl
```

Expected SHA-256:
`f6848718b0a50f48ecc428bb538fa00ca0926c9774965b393175a34abaf41285`.
This reconstruction reads saved data; it does not execute generated code, call a
judge, generate responses, or require a GPU.

## Scope and provenance

[`episode-manifest.json`](../published/episode-manifest.json) records archive and
file hashes, hashes of the original full files, and each export transformation.
Selected JSONL rows retain their original bytes. Worklists retain the selected
commands with the private absolute run root replaced by `rh_hillclimb` so that the
importer can relocate them. Run summaries retain model identity only: full-run
aggregate counts would not describe this subset. System prompts and the rubric are
unchanged. Original enclosing repository names and source commit IDs are omitted.

The release contains all turns in the contributing episodes, including saved
stdout/stderr, test outcomes and available final test-file contents. It is not an
archive of every candidate episode considered by the original selection process,
every judge API request, or a frozen executable sandbox. The reconstructed cohort
matches the original, but this subset alone cannot audit which omitted candidates
were excluded. Koby Lewis developed the source generation and judging setup;
Jansen Nye conducted the controls, analysis and release verification.

Readers can inspect the recorded judgments and their evidence. These are still the
original labels, not independent adjudication; “unflagged” is not a judge-confirmed
negative. Re-executing submissions requires reconstructing the original harness and
environment. The [compact activation bundle and extraction transcripts](DATA.md)
remain available separately.
