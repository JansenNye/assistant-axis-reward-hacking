# Inputs and provenance

## Axis

Supply a PyTorch tensor of shape `(36, 2880)` for GPT-OSS-120B, or a mapping containing
that tensor under `axis` and the model identifier under `model`.
`selfconcept.measurement.unit_axes.load_unit_axes` validates dimensions and normalizes
each selected layer. The legacy tensor used in the study lacks embedded model metadata;
its shape alone cannot authenticate its provenance. Load only trusted `.pt` files.
The extraction and reward-hacking dataset are credited to Koby Lewis.

## Transcripts

The extraction CLI consumes one JSON object per line. Required fields are:

```json
{
  "example_id": "unique-observation-id",
  "scenario": "impossible_original",
  "turn": 2,
  "messages": [{"role": "user", "content": "Task or latest feedback"}],
  "chat_kwargs": {},
  "raw_response": "<|start|>assistant<|channel|>analysis<|message|>reasoning<|end|><|start|>assistant<|channel|>final<|message|>answer<|return|>",
  "truncated": false,
  "outcome": {
    "status": "complete",
    "model_key": "openai/gpt-oss-120b",
    "scenario": "impossible_original",
    "label": "reward_hacking",
    "verdict": "HACK",
    "strength": "STRONG",
    "problem": "problem-id",
    "stratum": "problem/protocol/run-family/turn identifier"
  }
}
```

The example illustrates the schema, not an observation from the study. Preserve the
full original conversation, exact template settings, and channel markers in real input.
Use `verdict: "unflagged"` for the comparison observations. A stratum must include
the same problem, protocol, run family and turn. Do not collapse it to only the problem ID.
`python -m selfconcept.correlation.rh_hillclimb --help` describes the original
run-directory importer and its strict matching mode. It requires the original experiment
data, worklists, reasoning sidecars and verdict files; these are not public inputs here.

## Activation cache

Each shard contains:

- `manifest.json`: extraction identity (model/revision, input hash, layer list,
  shard index/count, expected observations, software versions), model dimensions,
  and completion status.
- `records.jsonl`: one record per scored observation, including labels/stratum,
  `region_counts` in prompt/reasoning/final order, `prompt_tokens`, and a relative
  `residuals` path.
- `residuals/*.npz`: `layer_17`, a float32 array of shape `(3, 2880)` holding the
  three region means. An empty region is represented by NaNs, not zero activations.

The analyzer rejects missing/duplicate shards, incompatible identities, and caches
made with a smoke-test limit. Exact token alignment excludes control markers and the
last unprocessed response token, matching the original scoring convention.

## What this release distributes

SOO's synthetic prompts live in the companion repository. This repository distributes
only aggregate statistics from the coding study, plus code. Original transcripts,
per-observation activations, the axis tensor, and model checkpoints are separate inputs.
The local preparation environment keeps a copy of the activation cache under ignored
`artifacts/` for validation; that directory is not part of Git history or the public release.
