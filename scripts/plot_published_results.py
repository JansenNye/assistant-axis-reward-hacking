"""Plot the validated 256-direction control from archived aggregate statistics."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main():
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "published/validated-random-256/analysis.json").read_text())
    cells = {c["region"]: c for c in data["cells"]
             if c["scenario"] == "all" and c["grouping"] == "problem_family_turn"}
    fig, ax = plt.subplots(figsize=(8, 4))
    for y, region in enumerate(("prompt", "cot", "final")):
        c = cells[region]
        low, _, high = c["auroc"]["random_quantiles"]
        axis = c["auroc"]["assistant_axis"]
        ci = c["assistant_axis_problem_bootstrap_ci"]
        ax.plot([low, high], [y, y], lw=9, color="#d6e2ee", solid_capstyle="round",
                label="Middle 95% of random directions" if y == 0 else None)
        ax.errorbar(axis, y, xerr=[[axis-ci[0]], [ci[1]-axis]], fmt="o", color="#315b8a",
                    capsize=4, label="Assistant Axis, 95% problem bootstrap CI" if y == 0 else None)
        ax.plot(c["baseline_aurocs"]["residual_norm"], y, "x", color="#c76c3d", ms=9,
                label="Activation norm" if y == 0 else None)
    ax.axvline(.5, color="gray", linestyle="--", lw=1)
    ax.set_yticks(range(3), ["Prompt", "Reasoning", "Final answer"])
    ax.invert_yaxis()
    ax.set_xlim(0, 1)
    ax.set_xlabel("Stratified AUROC")
    ax.set_title("GPT-OSS-120B, layer 17 · 256 random directions")
    ax.legend(loc="upper center", bbox_to_anchor=(.5, -.2), frameon=False, fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    out = root / "outputs"
    out.mkdir(exist_ok=True)
    for extension in ("png", "svg"):
        fig.savefig(out / f"assistant-axis-controls.{extension}", dpi=180, bbox_inches="tight")
    plt.close(fig)
    print(out / "assistant-axis-controls.png")


if __name__ == "__main__":
    main()
