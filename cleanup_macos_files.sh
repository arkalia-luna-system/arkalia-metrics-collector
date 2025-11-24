#!/bin/bash
# Script pour nettoyer les fichiers cachés macOS (.DS_Store et ._*)

echo "🧹 Nettoyage des fichiers cachés macOS..."

# Compter les fichiers avant
BEFORE=$(find . -name "._*" -type f -not -path "./.git/*" -not -path "./__pycache__/*" -not -path "./.venv/*" -not -path "./venv/*" -not -path "./site/*" -not -path "./htmlcov/*" 2>/dev/null | wc -l | tr -d ' ')

echo "📊 Fichiers ._* trouvés: $BEFORE"

if [ "$BEFORE" -gt 0 ]; then
    # Supprimer les fichiers ._*
    find . -name "._*" -type f -not -path "./.git/*" -not -path "./__pycache__/*" -not -path "./.venv/*" -not -path "./venv/*" -not -path "./site/*" -not -path "./htmlcov/*" -delete 2>/dev/null
    
    # Supprimer les dossiers ._*
    find . -name "._*" -type d -not -path "./.git/*" -not -path "./__pycache__/*" -not -path "./.venv/*" -not -path "./venv/*" -not -path "./site/*" -not -path "./htmlcov/*" -exec rm -rf {} + 2>/dev/null
    
    # Supprimer .DS_Store
    find . -name ".DS_Store" -type f -not -path "./.git/*" -delete 2>/dev/null
    
    AFTER=$(find . -name "._*" -type f -not -path "./.git/*" -not -path "./__pycache__/*" -not -path "./.venv/*" -not -path "./venv/*" -not -path "./site/*" -not -path "./htmlcov/*" 2>/dev/null | wc -l | tr -d ' ')
    
    echo "✅ Nettoyage terminé!"
    echo "📊 Fichiers ._* restants: $AFTER"
else
    echo "✅ Aucun fichier ._* à nettoyer"
fi

echo "✅ Nettoyage terminé!"
