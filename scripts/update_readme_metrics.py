#!/usr/bin/env python3
"""
Script pour mettre à jour automatiquement les métriques dans README.md

Ce script :
1. Lit les métriques agrégées depuis metrics/aggregated_metrics.json
2. Lit le tableau README depuis metrics/README_TABLE.md
3. Lit les badges depuis metrics/badges_final.md
4. Met à jour README.md avec les nouvelles valeurs
"""

import json
import re
from datetime import datetime
from pathlib import Path


def load_aggregated_metrics() -> dict:
    """Charge les métriques agrégées depuis JSON."""
    metrics_path = Path("metrics/aggregated_metrics.json")
    if not metrics_path.exists():
        raise FileNotFoundError(f"Fichier non trouvé: {metrics_path}")

    with open(metrics_path, encoding="utf-8") as f:
        data = json.load(f)

    return data.get("aggregated", {})


def load_readme_table() -> str:
    """Charge le tableau README depuis Markdown."""
    table_path = Path("metrics/README_TABLE.md")
    if not table_path.exists():
        raise FileNotFoundError(f"Fichier non trouvé: {table_path}")

    with open(table_path, encoding="utf-8") as f:
        return f.read()


def load_badges() -> str:
    """Charge les badges depuis Markdown."""
    badges_path = Path("metrics/badges_final.md")
    if not badges_path.exists():
        print("⚠️ badges_final.md non trouvé, utilisation des badges existants")
        return None

    with open(badges_path, encoding="utf-8") as f:
        return f.read()


def update_readme_metrics() -> bool:
    """Met à jour README.md avec les nouvelles métriques."""
    readme_path = Path("README.md")
    if not readme_path.exists():
        raise FileNotFoundError("README.md non trouvé")

    # Charger les données
    try:
        aggregated = load_aggregated_metrics()
        readme_table = load_readme_table()
        badges = load_badges()
    except FileNotFoundError as e:
        print(f"❌ Erreur: {e}")
        return False

    # Lire README.md
    readme_content = readme_path.read_text(encoding="utf-8")
    original_content = readme_content

    # Mettre à jour les métriques globales dans le tableau
    # Chercher la section "Métriques Globales"
    global_metrics_pattern = (
        r"(## 📊 \*\*Métriques Globales\*\*.*?\n</div>\n\n\*Métriques collectées.*?\*)"
    )

    if re.search(global_metrics_pattern, readme_content, re.DOTALL):
        readme_content = re.sub(
            global_metrics_pattern,
            readme_table.strip(),
            readme_content,
            flags=re.DOTALL,
        )
        print("✅ Tableau global mis à jour")
    else:
        # Si la section n'existe pas, l'ajouter après les métriques du projet
        project_metrics_pattern = (
            r"(## 📊 \*\*Métriques du Projet\*\*.*?\*Métriques collectées.*?\n)"
        )
        if re.search(project_metrics_pattern, readme_content, re.DOTALL):
            readme_content = re.sub(
                project_metrics_pattern,
                f"\\g<1>\n\n{readme_table.strip()}\n\n",
                readme_content,
                flags=re.DOTALL,
            )
            print("✅ Tableau global ajouté")

    # Mettre à jour les badges en haut du fichier
    if badges:
        # Chercher les badges existants (entre le titre et la description)
        badges_pattern = (
            r"(# Arkalia Metrics Collector 🚀\n\n)(.*?)(\n\n## Description)"
        )
        badges_match = re.search(badges_pattern, readme_content, re.DOTALL)

        if badges_match:
            readme_content = re.sub(
                badges_pattern,
                f"\\g<1>{badges.strip()}\\g<3>",
                readme_content,
                flags=re.DOTALL,
            )
            print("✅ Badges mis à jour")

    # Mettre à jour les métriques numériques dans le texte
    # Modules Python global
    readme_content = re.sub(
        r"\*\*52,320\*\*", f"**{aggregated.get('total_modules', 0):,}**", readme_content
    )

    # Lignes de code globales
    readme_content = re.sub(
        r"\*\*24,790,076\*\*",
        f"**{aggregated.get('total_lines_of_code', 0):,}**",
        readme_content,
    )

    # Tests globaux
    readme_content = re.sub(
        r"\*\*11,204\*\*", f"**{aggregated.get('total_tests', 0):,}**", readme_content
    )

    # Mettre à jour la date de collecte
    current_date = datetime.now().strftime("%Y-%m-%d")
    readme_content = re.sub(
        r"Métriques collectées automatiquement le \d{4}-\d{2}-\d{2}",
        f"Métriques collectées automatiquement le {current_date}",
        readme_content,
    )

    # Écrire README.md seulement si changé
    if readme_content != original_content:
        readme_path.write_text(readme_content, encoding="utf-8")
        print("✅ README.md mis à jour avec succès")
        return True
    else:
        print("ℹ️ Aucun changement nécessaire dans README.md")
        return False


def main():
    """Point d'entrée principal."""
    try:
        print("🚀 Mise à jour des métriques dans README.md...")
        updated = update_readme_metrics()
        if updated:
            print("✅ Mise à jour terminée avec succès")
            return 0
        else:
            print("ℹ️ Aucune mise à jour nécessaire")
            return 0
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
