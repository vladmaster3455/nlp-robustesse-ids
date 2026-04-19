# NLP - Etude de la robustesse des modeles pour la detection d'intrusion reseau

Ce projet est un socle complet et separable pour etudier la robustesse d'un modele NLP applique a la detection d'intrusion reseau.

## Démarrage Rapide

```bash
# 1. Installation
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

# 2. Test complet
python test_complete.py

# 3. Voir les résultats
ls results/ reports/
```

## Objectif

1. Entrainer un classifieur NLP sur des donnees de trafic/logs converties en texte.
2. Evaluer les performances sur donnees propres.
3. Mesurer la degradation sous perturbations (fautes de frappe, suppression de caracteres, substitutions simples).
4. Generer un rapport de robustesse exploitable pour un memoire/rapport scientifique.

## Structure

- `src/` : code principal (chargement, entrainement, evaluation, robustesse)
- `data/raw/` : donnees sources CSV
- `data/processed/` : donnees transformees
- `results/` : modele sauvegarde et sorties JSON
- `reports/` : rapports de robustesse
- `scripts/` : scripts shell de lancement

## Format de donnees accepte

Le pipeline attend un CSV avec au minimum une colonne texte et une colonne label.

Exemple:

- `text`: description textuelle du flux reseau/log
- `label`: classe (normal, attack, etc.)

Si tes donnees sont tabulaires (NSL-KDD, UNSW-NB15, etc.), le projet inclut une conversion automatique ligne -> phrase textuelle.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Test Complet (Avant GitHub)

**La manière la plus simple de tester le projet :**

```bash
chmod +x test.sh
./test.sh
```

Ou directement :

```bash
source .venv/bin/activate
python test_complete.py
```

**Le test exécute 4 étapes :**
1. Génère 500 samples synthétiques (40% attacks, 60% normal)
2. Entraîne un modèle TF-IDF + Logistic Regression
3. Évalue sur données de test
4. Teste la robustesse avec perturbations textuelles (20% du texte)

**Résultat attendu :**
```
✓ Test complet terminé avec succès !

Fichiers générés :
  - Dataset: ./data/raw/synthetic_dataset.csv
  - Modèle: ./results/baseline_tfidf_logreg.joblib
  - Métriques train: ./results/train_metrics.json
  - Métriques eval: ./results/eval_clean.json
  - Rapport robustesse: ./reports/robustness_report.json
```

Pour plus de détails, voir [README_TEST.md](README_TEST.md).

## Entrainement

```bash
python -m src.main train \
  --data-path data/raw/dataset.csv \
  --label-column label \
  --model-path results/baseline_tfidf_logreg.joblib
```

Si la colonne texte n'existe pas, utilise `--auto-text-from-tabular`.

## Evaluation

```bash
python -m src.main evaluate \
  --data-path data/raw/dataset.csv \
  --label-column label \
  --model-path results/baseline_tfidf_logreg.joblib \
  --output-json results/eval_clean.json
```

## Etude de robustesse

```bash
python -m src.main robustness \
  --data-path data/raw/dataset.csv \
  --label-column label \
  --model-path results/baseline_tfidf_logreg.joblib \
  --output-json reports/robustness_report.json \
  --severity 0.2
```

`severity` controle l'intensite des perturbations textuelles.

