#!/usr/bin/env bash
set -e

echo "======================================================================="
echo "Déploiement sur GitHub - NLP Robustesse IDS"
echo "======================================================================="
echo ""

# Vérifier que git est installé
if ! command -v git &> /dev/null; then
    echo "❌ Git n'est pas installé. Installe-le d'abord :"
    echo "   sudo apt install git"
    exit 1
fi

echo "1️⃣  Initialise le dépôt git local..."
git init

echo "2️⃣  Ajoute tous les fichiers..."
git add .

echo "3️⃣  Crée le commit initial..."
git commit -m "Initial commit - NLP robustesse IDS"

echo "4️⃣  Change le nom de branche en 'main'..."
git branch -M main

echo ""
echo "======================================================================="
echo "✓ Dépôt local créé avec succès"
echo "======================================================================="
echo ""
echo "📌 PROCHAINES ÉTAPES :"
echo ""
echo "1. Crée un nouveau repository sur GitHub :"
echo "   👉 https://github.com/new"
echo ""
echo "   - Repository name: nlp-robustesse-ids"
echo "   - Sélectionne Public ou Private"
echo "   - Clique 'Create repository'"
echo ""
echo "2. Copie l'URL donnée par GitHub (ex: https://github.com/TON_USERNAME/nlp-robustesse-ids.git)"
echo ""
echo "3. Tapes cette commande (remplace TON_URL_GITHUB) :"
echo "   git remote add origin TON_URL_GITHUB"
echo ""
echo "4. Pousse le code :"
echo "   git push -u origin main"
echo ""
echo "======================================================================="
