#!/usr/bin/env python3
"""
Script pour générer le dashboard interactif depuis les métriques agrégées.

Utilisé par le workflow GitHub Pages pour déployer le dashboard.
"""

import json
import sys
from pathlib import Path

# Ajouter le chemin du projet au PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

# Imports après modification du PYTHONPATH
from arkalia_metrics_collector.exporters.interactive_dashboard import (  # noqa: E402
    InteractiveDashboardGenerator,
)


def load_aggregated_metrics(metrics_file: str | Path) -> dict:
    """Charge les métriques agrégées depuis un fichier JSON."""
    metrics_path = Path(metrics_file)
    if not metrics_path.exists():
        raise FileNotFoundError(f"Fichier de métriques non trouvé: {metrics_path}")

    with open(metrics_path, encoding="utf-8") as f:
        return json.load(f)


def load_history(history_dir: str | Path = "metrics/history") -> list[dict] | None:
    """Charge l'historique des métriques."""
    try:
        # Charger les 10 dernières entrées pour les graphiques
        history_files = sorted(Path(history_dir).glob("metrics_*.json"), reverse=True)[
            :10
        ]

        history_data = []
        for file_path in history_files:
            try:
                with open(file_path, encoding="utf-8") as f:
                    data = json.load(f)
                    history_data.append(data)
            except Exception:
                continue

        return history_data if history_data else None
    except Exception:
        return None


def main():
    """Génère le dashboard interactif."""
    # Chemins
    metrics_file = Path("metrics/aggregated_metrics.json")
    output_file = Path("site/dashboard/index.html")
    history_dir = Path("metrics/history")

    print("🚀 Génération du dashboard interactif...")
    print(f"   📊 Métriques: {metrics_file}")
    print(f"   📁 Sortie: {output_file}")

    # Charger les métriques
    try:
        metrics_data = load_aggregated_metrics(metrics_file)
        print("✅ Métriques chargées")
    except FileNotFoundError:
        print(f"❌ Erreur: {metrics_file} non trouvé")
        print("   💡 Assurez-vous d'avoir exécuté 'arkalia-metrics aggregate'")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur lors du chargement des métriques: {e}")
        sys.exit(1)

    # Charger l'historique
    history_data = None
    if history_dir.exists():
        history_data = load_history(history_dir)
        if history_data:
            print(f"✅ Historique chargé ({len(history_data)} entrées)")
        else:
            print("ℹ️  Aucun historique disponible")
    else:
        print("ℹ️  Dossier historique non trouvé")

    # Détecter si métriques agrégées
    is_aggregated = "aggregated" in metrics_data and "projects" in metrics_data

    # Générer le dashboard
    try:
        success = InteractiveDashboardGenerator.generate_dashboard(
            metrics_data=metrics_data,
            history_data=history_data,
            output_file=output_file,
            is_aggregated=is_aggregated,
        )

        if success:
            print(f"✅ Dashboard généré avec succès: {output_file}")
            print("   🌐 Accessible sur GitHub Pages après déploiement")
        else:
            print("❌ Échec de la génération du dashboard")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
