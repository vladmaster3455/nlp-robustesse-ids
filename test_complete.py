#!/usr/bin/env python3
"""
Script de test complet : génère données, entraîne, évalue et teste robustesse.
"""
from __future__ import annotations

import json
from pathlib import Path

from src.data import extract_text_and_label, load_csv, split_dataset
from src.evaluate import compute_metrics
from src.modeling import build_baseline_model, load_model, save_model
from src.robustness import evaluate_robustness
from src.synthetic_data import save_synthetic_dataset
from src.utils import save_json, set_seed


def main() -> None:
    print("=" * 70)
    print("NLP - Étude de Robustesse IDS - Test Complet")
    print("=" * 70)
    
    # Configuration
    seed = 42
    set_seed(seed)
    
    project_root = Path(__file__).parent
    data_path = project_root / "data" / "raw" / "synthetic_dataset.csv"
    model_path = project_root / "results" / "baseline_tfidf_logreg.joblib"
    train_metrics_json = project_root / "results" / "train_metrics.json"
    eval_metrics_json = project_root / "results" / "eval_clean.json"
    robustness_json = project_root / "reports" / "robustness_report.json"
    
    # Étape 1 : Générer données synthétiques
    print("\n[1/4] Génération des données synthétiques...")
    save_synthetic_dataset(data_path, n_samples=500)
    
    # Étape 2 : Charger données et entraîner
    print("\n[2/4] Entraînement du modèle...")
    df = load_csv(data_path)
    texts, labels = extract_text_and_label(
        df,
        label_column="label",
        text_column="text",
    )
    split = split_dataset(texts, labels, test_size=0.2, seed=seed)
    
    model = build_baseline_model(seed=seed)
    model.fit(split.x_train, split.y_train)
    
    # Évaluation sur données d'entraînement
    train_pred = model.predict(split.x_train)
    train_metrics = compute_metrics(split.y_train, train_pred)
    save_json(train_metrics, train_metrics_json)
    print(f"  Accuracy train: {train_metrics['accuracy']:.4f}")
    print(f"  F1 macro train: {train_metrics['f1_macro']:.4f}")
    
    # Sauvegarde du modèle
    save_model(model, model_path)
    print(f"  Modèle sauvegardé: {model_path}")
    
    # Étape 3 : Évaluation sur test set
    print("\n[3/4] Évaluation sur données de test...")
    eval_pred = model.predict(split.x_test)
    eval_metrics = compute_metrics(split.y_test, eval_pred)
    save_json(eval_metrics, eval_metrics_json)
    print(f"  Accuracy test: {eval_metrics['accuracy']:.4f}")
    print(f"  F1 macro test: {eval_metrics['f1_macro']:.4f}")
    
    # Étape 4 : Étude de robustesse
    print("\n[4/4] Étude de robustesse (perturbations)...")
    robustness_report = evaluate_robustness(
        model=model,
        texts=split.x_test,
        labels=split.y_test,
        severity=0.2,
        seed=seed,
    )
    save_json(robustness_report, robustness_json)
    print(f"  Chute accuracy: {robustness_report['delta_accuracy']:.4f}")
    print(f"  Chute F1: {robustness_report['delta_f1_macro']:.4f}")
    
    print("\n" + "=" * 70)
    print("✓ Test complet terminé avec succès !")
    print("=" * 70)
    print(f"\nFichiers générés :")
    print(f"  - Dataset: {data_path}")
    print(f"  - Modèle: {model_path}")
    print(f"  - Métriques train: {train_metrics_json}")
    print(f"  - Métriques eval: {eval_metrics_json}")
    print(f"  - Rapport robustesse: {robustness_json}")
    print()


if __name__ == "__main__":
    main()
