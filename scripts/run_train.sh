#!/usr/bin/env bash
set -e

python -m src.main train \
  --data-path data/raw/dataset.csv \
  --label-column label \
  --auto-text-from-tabular \
  --model-path results/baseline_tfidf_logreg.joblib \
  --metrics-json results/train_metrics.json
