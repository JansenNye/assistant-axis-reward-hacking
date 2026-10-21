"""Leave one problem out when fitting each mean-difference direction (CPU)."""
import argparse
import json
from pathlib import Path

import numpy as np

from selfconcept.correlation.analyze import binary_outcome
from selfconcept.correlation.direction_analysis import held_out_diff_means
from selfconcept.correlation.random_vector_analysis import group_indices, load_cache, pair_totals
from selfconcept.correlation.random_vectors import REGIONS


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directories", nargs="+", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    records, manifest = load_cache(args.directories)
    completed = [(d, r) for d, r in records if r["status"] == "complete" and binary_outcome(r["outcome"])[0] is not None]
    rows = [r for _, r in completed]
    labels = np.array([binary_outcome(r["outcome"])[0] for r in rows])
    problems = [json.dumps([r["scenario"], r["outcome"]["problem"]]) for r in rows]
    strata = [r["outcome"]["stratum"] for r in rows]
    cells = []
    for layer in manifest["identity"]["layers"]:
        matrices = np.stack([np.load(d / r["residuals"])[f"layer_{layer}"] for d, r in completed])
        for region_index, region in enumerate(REGIONS):
            finite = np.flatnonzero(np.isfinite(matrices[:, region_index]).all(axis=1))
            valid_strata = [strata[i] for i in finite]
            groups = [g for g in group_indices(valid_strata).values() if len(np.unique(labels[finite[g]])) == 2]
            if not groups:
                cells.append({"layer": layer, "region": region, "status": "no_matched_pairs"})
                continue
            keep = finite[np.sort(np.concatenate(groups))]
            local_problems = [problems[i] for i in keep]
            scores = held_out_diff_means(matrices[keep, region_index], labels[keep], local_problems)
            ok = np.flatnonzero(np.isfinite(scores))
            u, pairs, _ = pair_totals(scores[ok, None], labels[keep[ok]],
                                      [strata[keep[i]] for i in ok], [local_problems[i] for i in ok])
            cells.append({"layer": layer, "region": region, "n": len(keep), "n_pairs": int(pairs.sum()),
                          "held_out_diff_means_auroc": float(u.sum() / pairs.sum()) if len(pairs) else None})
    args.out.parent.mkdir(parents=True, exist_ok=True)
    result = {"method": "pooled class means fitted excluding the scored problem; informative matched strata only", "cells": cells}
    args.out.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
