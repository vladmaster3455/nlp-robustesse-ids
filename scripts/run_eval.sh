#!/usr/bin/env bash
set -e

python -m src.main evaluate \
  --data-path data/raw/dataset.csv \
  --label-column label \
  --auto-text-from-tabular \
  --model-path results/baseline_tfidf_logreg.joblib \
  --output-json results/eval_clean.json
