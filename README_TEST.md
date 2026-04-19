# Guide de Test Complet

Ce guide explique comment tester le projet en local **avant** de le pousser sur GitHub.

## Étapes rapides

### 1. Créer l'environnement virtuel

```bash
cd /home/srg/Documents/IA/bench_project\ \(2\)/nlp-robustesse-ids
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Installer les dépendances

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Note :** Si tu as des timeouts pip, réessaye avec un timeout plus long :
```bash
pip install --default-timeout=1000 -r requirements.txt
```

### 3. Lancer le test complet

Le script `test_complete.py` fait tout en une seule commande :

```bash
python test_complete.py
```

Cela va :
1. ✓ Générer un dataset synthétique de 500 samples (normal + attacks)
2. ✓ Entraîner un modèle TF-IDF + Logistic Regression
3. ✓ Évaluer sur les données de test
4. ✓ Tester la robustesse via perturbations textuelles

### 4. Consulter les résultats

Après l'exécution, tu trouveras :

**Fichiers de résultats :**
- `results/baseline_tfidf_logreg.joblib` — Modèle entraîné
- `results/train_metrics.json` — Métriques d'entraînement
- `results/eval_clean.json` — Métriques d'évaluation

**Rapport d'étude :**
- `reports/robustness_report.json` — Détails des tests de robustesse

## Résultat attendu

Quand tu lances `test_complete.py`, la sortie doit ressembler à :

```
======================================================================
NLP - Étude de Robustesse IDS - Test Complet
======================================================================

[1/4] Génération des données synthétiques...
Dataset synthétique créé: data/raw/synthetic_dataset.csv
  Total samples: 500
  Normal: 300
  Attack: 200

[2/4] Entraînement du modèle...
  Accuracy train: 0.9850
  F1 macro train: 0.9847
  Modèle sauvegardé: results/baseline_tfidf_logreg.joblib

[3/4] Évaluation sur données de test...
  Accuracy test: 0.9600
  F1 macro test: 0.9598

[4/4] Étude de robustesse (perturbations)...
  Chute accuracy: 0.0850
  Chute F1: 0.0856

=======================================================================
✓ Test complet terminé avec succès !
======================================================================
```

## Troubleshooting

### Problème : "ModuleNotFoundError: No module named 'sklearn'"

**Solution :** Réinstaller scikit-learn
```bash
pip install --force-reinstall scikit-learn
```

### Problème : "No module named 'reportlab'"

**Solution :** Installer reportlab explicitement
```bash
pip install reportlab
```

### Problème : "Read timeout" lors de pip install

**Solution :** Utiliser un timeout plus grand
```bash
pip install --default-timeout=2000 -r requirements.txt
```

## Tests optionnels avancés

### Test individuel de chaque commande

#### Juste l'entraînement :
```bash
python -m src.main train \
  --data-path data/raw/synthetic_dataset.csv \
  --label-column label \
  --text-column text
```

#### Juste l'évaluation :
```bash
python -m src.main evaluate \
  --data-path data/raw/synthetic_dataset.csv \
  --label-column label \
  --text-column text \
  --model-path results/baseline_tfidf_logreg.joblib
```

#### Juste la robustesse :
```bash
python -m src.main robustness \
  --data-path data/raw/synthetic_dataset.csv \
  --label-column label \
  --text-column text \
  --model-path results/baseline_tfidf_logreg.joblib \
  --severity 0.2
```


