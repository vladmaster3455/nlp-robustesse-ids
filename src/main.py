from __future__ import annotations

import argparse
from pathlib import Path

from .data import extract_text_and_label, load_csv, split_dataset
from .evaluate import compute_metrics
from .modeling import build_baseline_model, load_model, save_model
from .robustness import evaluate_robustness
from .utils import save_json, set_seed


def cmd_train(args: argparse.Namespace) -> None:
    set_seed(args.seed)
    df = load_csv(Path(args.data_path))
    texts, labels = extract_text_and_label(
        df,
        label_column=args.label_column,
        text_column=args.text_column,
        auto_text_from_tabular=args.auto_text_from_tabular,
    )

    split = split_dataset(texts, labels, test_size=args.test_size, seed=args.seed)
    model = build_baseline_model(seed=args.seed)
    model.fit(split.x_train, split.y_train)

    preds = model.predict(split.x_test)
    metrics = compute_metrics(split.y_test, preds)

    save_model(model, Path(args.model_path))
    if args.metrics_json:
        save_json(metrics, Path(args.metrics_json))

    print("Train termine.")
    print(f"Modele sauvegarde: {args.model_path}")
    print(f"Accuracy test: {metrics['accuracy']:.4f}")
    print(f"F1 macro test: {metrics['f1_macro']:.4f}")


def cmd_evaluate(args: argparse.Namespace) -> None:
    df = load_csv(Path(args.data_path))
    texts, labels = extract_text_and_label(
        df,
        label_column=args.label_column,
        text_column=args.text_column,
        auto_text_from_tabular=args.auto_text_from_tabular,
    )

    model = load_model(Path(args.model_path))
    preds = model.predict(texts)
    metrics = compute_metrics(labels, preds)
    save_json(metrics, Path(args.output_json))

    print("Evaluation terminee.")
    print(f"Resultats: {args.output_json}")
    print(f"Accuracy: {metrics['accuracy']:.4f}")


def cmd_robustness(args: argparse.Namespace) -> None:
    df = load_csv(Path(args.data_path))
    texts, labels = extract_text_and_label(
        df,
        label_column=args.label_column,
        text_column=args.text_column,
        auto_text_from_tabular=args.auto_text_from_tabular,
    )

    model = load_model(Path(args.model_path))
    report = evaluate_robustness(
        model=model,
        texts=texts,
        labels=labels,
        severity=args.severity,
        seed=args.seed,
    )
    save_json(report, Path(args.output_json))

    print("Etude de robustesse terminee.")
    print(f"Rapport: {args.output_json}")
    print(f"Delta accuracy: {report['delta_accuracy']:.4f}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="NLP - Robustesse des modeles pour la detection d'intrusion reseau"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    def add_common(p: argparse.ArgumentParser) -> None:
        p.add_argument("--data-path", required=True)
        p.add_argument("--label-column", default="label")
        p.add_argument("--text-column", default=None)
        p.add_argument("--auto-text-from-tabular", action="store_true")

    p_train = sub.add_parser("train")
    add_common(p_train)
    p_train.add_argument("--model-path", default="results/baseline_tfidf_logreg.joblib")
    p_train.add_argument("--metrics-json", default="results/train_metrics.json")
    p_train.add_argument("--test-size", type=float, default=0.2)
    p_train.add_argument("--seed", type=int, default=42)
    p_train.set_defaults(func=cmd_train)

    p_eval = sub.add_parser("evaluate")
    add_common(p_eval)
    p_eval.add_argument("--model-path", required=True)
    p_eval.add_argument("--output-json", default="results/eval_clean.json")
    p_eval.set_defaults(func=cmd_evaluate)

    p_rob = sub.add_parser("robustness")
    add_common(p_rob)
    p_rob.add_argument("--model-path", required=True)
    p_rob.add_argument("--output-json", default="reports/robustness_report.json")
    p_rob.add_argument("--severity", type=float, default=0.2)
    p_rob.add_argument("--seed", type=int, default=42)
    p_rob.set_defaults(func=cmd_robustness)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
