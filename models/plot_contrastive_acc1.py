from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def collect_results(run_dir: Path) -> pd.DataFrame:
    rows = []
    for csv_path in sorted(run_dir.glob("*/results.csv")):
        df = pd.read_csv(csv_path)
        if df.empty:
            continue

        if "acc@1" not in df.columns:
            continue

        eval_rows = df[df["acc@1"].notna()].copy()
        if "stage" in eval_rows.columns:
            eval_rows = eval_rows[eval_rows["stage"].astype(str).str.contains("eval", na=False)]

        for _, row in eval_rows.iterrows():
            rows.append(
                {
                    "run_name": csv_path.parent.name,
                    "model": row.get("model"),
                    "contrastive": int(row.get("contrastive", 0)),
                    "gradient": int(row.get("gradient")),
                    "window": int(row.get("window")),
                    "lr": float(row.get("lr")),
                    "seed": int(row.get("seed")),
                    "acc1": float(row.get("acc@1")),
                    "acc5": float(row.get("acc@5")),
                    "stage": row.get("stage"),
                }
            )

    if not rows:
        raise RuntimeError(f"No eval rows with acc@1 found under {run_dir}")

    return pd.DataFrame(rows)


def plot_acc1(df: pd.DataFrame, out_path: Path) -> None:
    sns.set_theme(style="whitegrid", context="talk")

    df = df.copy()
    df["lr_label"] = "lr=" + df["lr"].map("{:.4g}".format)
    df = df.sort_values(["gradient", "lr", "model"])

    grid = sns.catplot(
        data=df,
        kind="bar",
        x="model",
        y="acc1",
        hue="lr_label",
        col="gradient",
        col_order=sorted(df["gradient"].unique()),
        errorbar=None,
        palette="Set2",
        height=6,
        aspect=1.15,
        sharey=True,
    )

    grid.set_axis_labels("Model", "Acc@1 (%)")
    grid.set_titles("gradient={col_name}")
    grid.figure.suptitle("Acc@1 by Model, Gradient, and Learning Rate", y=1.04)
    grid.set(ylim=(0, max(70, df["acc1"].max() + 8)))

    for ax in grid.axes.flat:
        ax.tick_params(axis="x", rotation=25)
        for container in ax.containers:
            ax.bar_label(container, fmt="%.1f", padding=3, fontsize=9)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    grid.figure.tight_layout()
    grid.figure.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot acc@1 from contrastive run results.csv files.")
    parser.add_argument(
        "--run-dir",
        type=Path,
        default=Path("contrastive_runs_w50_seed42"),
        help="Directory containing one subfolder per run, each with results.csv.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("analysis_acc1"),
        help="Output directory for the summary CSV and figure.",
    )
    args = parser.parse_args()

    run_dir = args.run_dir.resolve()
    out_dir = args.out_dir.resolve()

    df = collect_results(run_dir)

    out_dir.mkdir(parents=True, exist_ok=True)
    summary_csv = out_dir / f"{run_dir.name}_acc1_summary.csv"
    figure_png = out_dir / f"{run_dir.name}_acc1_comparison.png"

    df.sort_values(["model", "gradient", "lr", "seed"]).to_csv(summary_csv, index=False)
    plot_acc1(df, figure_png)

    print(f"Collected {len(df)} runs from {run_dir}")
    print(f"Saved summary: {summary_csv}")
    print(f"Saved figure: {figure_png}")
    print("\nBest by acc@1:")
    print(df.sort_values("acc1", ascending=False).head(10).to_string(index=False))


if __name__ == "__main__":
    main()
