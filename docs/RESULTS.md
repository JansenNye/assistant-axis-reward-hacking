# Published numbers and validation

The standalone release was run against all six original activation-cache shards:
824 complete observations, 41 problems, no extraction OOM records. These are CPU
analyses of existing model activations; the 120B model was not rerun for this release.

For strict problem/protocol/family/turn matching, the validated 256-direction run gives:

| Region | AA AUROC | 95% whole-problem bootstrap CI | Random directions at least as extreme |
|---|---:|---|---:|
| Prompt | 0.524770 | [0.484931, 0.567623] | 49.805% |
| Reasoning | 0.695502 | [0.607552, 0.780853] | 5.447% |
| Final answer | 0.714286 | [0.608749, 0.798374] | 30.350% |

Both validated runs use seed 1729 and 1,000 bootstrap draws. With 2,000 random
directions, the corresponding tail fractions are 54.073%, 4.398%, and 28.936%.
Tail fractions use the original `(1 + exceedances) / (1 + directions)` convention.
The final-answer norm-only AUROC is 0.116359 (inverse association); token-count-only
AUROC is 0.543779. There are 868 prompt/final pairs and 867 reasoning pairs after
excluding empty/nonfinite reasoning regions.

## Which archive to use

- `published/original-256`: historical 256-direction analysis as found on disk.
- `published/original-2000`: historical 2,000-direction analysis as found on disk.
- `published/validated-random-256`: recomputed with this release's code; corresponds
  to the post's main table after rounding.
- `published/validated-random-2000`: recomputed 2,000-direction sensitivity analysis.

The historical 256-direction archive has an earlier prompt-region result
(AA AUROC 0.514977), while the current release and historical 2,000-direction archive
both yield 0.524770. The later projection implementation preserves ties for identical
residual vectors; the tests explicitly check this behavior. Both original files are
preserved rather than silently replaced. Use the validated files for reproduction.

The post's displayed bounds are rounded, and its figure/footnotes draw on different
random-direction counts. The plotting script here uses the validated **256-direction**
run consistently and reads its values from JSON. The bootstrap interval describes
uncertainty for the fixed Assistant Axis; the random-direction interval describes
variation across directions. These intervals have different meanings.

The held-out baseline and noise experiment have separate scripts. The former fits
pooled class-mean differences excluding the scored problem; the latter holds a
pair-weighted in-sample direction fixed while adding isotropic noise. Neither is a
causal intervention on model behavior.
