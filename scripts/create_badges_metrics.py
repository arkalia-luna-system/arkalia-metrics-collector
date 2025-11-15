#!/usr/bin/env python3
"""
Script pour créer metrics_for_badges.json depuis aggregated_metrics.json

Ce script est utilisé par le workflow GitHub Actions si metrics_for_badges.json
n'existe pas encore.
"""

import json
from pathlib import Path


def create_badges_metrics():
    """Crée metrics_for_badges.json depuis aggregated_metrics.json."""
    aggregated_path = Path("metrics/aggregated_metrics.json")
    badges_path = Path("metrics/metrics_for_badges.json")

    if not aggregated_path.exists():
        raise FileNotFoundError(f"Fichier non trouvé: {aggregated_path}")

    # Lire les métriques agrégées
    with open(aggregated_path, encoding="utf-8") as f:
        data = json.load(f)

    aggregated = data.get("aggregated", {})

    # Créer la structure pour les badges
    summary = {
        "total_python_files": aggregated.get("total_modules", 0),
        "lines_of_code": aggregated.get("total_lines_of_code", 0),
        "collected_tests": aggregated.get("total_tests", 0),
        "documentation_files": aggregated.get("total_documentation_files", 0),
    }

    metrics_for_badges = {
        "summary": summary,
        "collection_info": {
            "collection_date": data.get("collection_date", ""),
        },
    }

    # Écrire metrics_for_badges.json
    with open(badges_path, "w", encoding="utf-8") as f:
        json.dump(metrics_for_badges, f, indent=2, ensure_ascii=False)

    print(f"✅ {badges_path} créé avec succès")
    print(f"   Modules: {summary['total_python_files']:,}")
    print(f"   Lignes: {summary['lines_of_code']:,}")
    print(f"   Tests: {summary['collected_tests']:,}")


if __name__ == "__main__":
    try:
        create_badges_metrics()
    except Exception as e:
        print(f"❌ Erreur: {e}")
        exit(1)
