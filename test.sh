#!/usr/bin/env bash
set -e

echo "======================================================================="
echo "Installation et Test Complet - NLP Robustesse IDS"
echo "======================================================================="
echo ""

if [ ! -d ".venv" ]; then
    echo "[1/4] Création de l'environnement virtuel..."
    python3 -m venv .venv
else
    echo "[1/4] Environnement virtuel existant détecté"
fi

echo "[2/4] Activation et mise à jour pip..."
source .venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1

echo "[3/4] Installation des dépendances..."
pip install --default-timeout=1000 -r requirements.txt > /dev/null 2>&1

echo "[4/4] Lancement du test complet..."
python test_complete.py

echo ""
echo "======================================================================="
echo "✓ Test terminé"
echo "======================================================================="
