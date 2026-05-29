#!/usr/bin/env bash
# Example contrastive sweep. Set seed=42 (default) or export seed before running.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO/models"
seed="${seed:-42}"

for lr in 0.0003 0.001 0.003; do
  for m in mlp cnn lstm transformer; do
    for g in 0 25; do
      for w in 50 100; do
        python run.py \
          --train-dir "$REPO/base_data/training" \
          --test-dir "$REPO/base_data/testing" \
          --real-test-dir "$REPO/base_data/testing" \
          --gcms-csv "$REPO/gcms_processed/gcms_food_vectors.csv" \
          --models "$m" --contrastive on --gradients "$g" --window-sizes "$w" \
          --seed "${seed}" \
          --epochs 90 --batch-size 32 --lr "$lr" \
          --run-name-prefix "SEL_grad${g}_w${w}_lr${lr}" \
          --log-dir "./contrastive_runs_w${w}_seed${seed}"
      done
    done
  done
done
