#!/usr/bin/env python3
"""
Arkalia Metrics Exporter - Export des métriques en différents formats.

Module d'export des métriques en différents formats.
Supporte JSON, Markdown, HTML, CSV et YAML.
"""

import csv
import json
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore[import-untyped]
except ImportError:
    yaml = None

from arkalia_metrics_collector import __version__
from arkalia_metrics_collector.exporters.interactive_dashboard import (
    InteractiveDashboardGenerator,
)


class MetricsExporter:
    """
    Exporteur de métriques en différents formats.

    Supporte l'export en :
    - JSON (format complet)
    - Markdown (pour README)
    - HTML (pour dashboards)
    - CSV (pour analyse)
    - YAML (pour configuration)
    """

    def __init__(self, metrics_data: dict[str, Any]) -> None:
        """
        Initialise l'exporteur avec les données de métriques.

        Args:
            metrics_data: Données des métriques à exporter
        """
        self.metrics_data = metrics_data

    def export_json(self, output_file: str) -> bool:
        """
        Exporte en format JSON.

        Args:
            output_file: Chemin du fichier de sortie

        Returns:
            True si l'export a réussi
        """
        try:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(self.metrics_data, f, indent=2, ensure_ascii=False)

            return True

        except (OSError, TypeError) as e:
            print(f"Erreur lors de l'export JSON: {e}")
            return False

    def export_markdown_summary(self, output_file: str) -> bool:
        """
        Exporte un résumé en format Markdown pour le README.

        Args:
            output_file: Chemin du fichier de sortie

        Returns:
            True si l'export a réussi
        """
        try:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            summary = self.metrics_data.get("summary", {})
            collection_info = self.metrics_data.get("collection_info", {})

            content = f"""## 📊 **Métriques du Projet** *(Mise à jour automatique)*

<div align="center">

| **Composant** | **Valeur** | **Statut** | **Vérifié** |
|:-------------:|:---------:|:----------:|:------------:|
| **🐍 Fichiers Python** | `{summary.get("total_python_files", 0):,} modules` | ![Actif](https://img.shields.io/badge/status-actif-brightgreen) | ✅ **COMPTÉ** |
| **📝 Lignes de Code** | `{summary.get("lines_of_code", 0):,} lignes` | ![Maintenu](https://img.shields.io/badge/status-maintenu-blue) | ✅ **MESURÉ** |
| **🧪 Tests** | `{summary.get("collected_tests", 0):,} tests` | ![Testé](https://img.shields.io/badge/status-testé-green) | ✅ **COLLECTÉ** |
| **📚 Documentation** | `{summary.get("documentation_files", 0)} fichiers` | ![Complet](https://img.shields.io/badge/status-complet-yellow) | ✅ **ORGANISÉ** |

</div>

*Métriques collectées automatiquement le {collection_info.get("collection_date", "Inconnu")} par [Arkalia Metrics Collector](data/metrics.json)*
"""

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)

            return True

        except OSError as e:
            print(f"Erreur lors de l'export Markdown: {e}")
            return False

    def export_html_dashboard(
        self, output_file: str, use_interactive: bool = True
    ) -> bool:
        """
        Exporte un dashboard HTML interactif.

        Args:
            output_file: Chemin du fichier de sortie
            use_interactive: Utiliser le dashboard interactif avec Chart.js
                (défaut: True)

        Returns:
            True si l'export a réussi
        """
        # Utiliser le dashboard interactif si demandé
        if use_interactive:
            try:
                # Détecter si ce sont des métriques agrégées
                is_aggregated = (
                    "aggregated" in self.metrics_data
                    and "projects" in self.metrics_data
                )

                # Essayer de charger l'historique si disponible
                from arkalia_metrics_collector.collectors.metrics_history import (
                    MetricsHistory,
                )

                history = MetricsHistory()
                latest_history = []
                # Charger la dernière entrée
                entry = history.get_latest_metrics()
                if entry:
                    latest_history.append(entry)

                return InteractiveDashboardGenerator.generate_dashboard(
                    self.metrics_data,
                    latest_history if latest_history else None,
                    output_file,
                    is_aggregated=is_aggregated,
                )
            except Exception:  # nosec B110
                # Si échec, utiliser le dashboard basique
                pass

        # Dashboard basique (fallback)
        try:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            summary = self.metrics_data.get("summary", {})
            collection_info = self.metrics_data.get("collection_info", {})

            html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arkalia Metrics Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-900 text-white min-h-screen">
    <div class="container mx-auto px-4 py-8">
        <header class="text-center mb-12">
            <h1 class="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-600 mb-4">
                🚀 Arkalia Metrics Dashboard
            </h1>
            <p class="text-xl text-gray-300">
                Métriques collectées le {collection_info.get("collection_date", "Inconnu")}
            </p>
        </header>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
            <!-- Fichiers Python -->
            <div class="bg-gradient-to-br from-blue-600 to-blue-800 p-6 rounded-xl shadow-lg">
                <div class="text-center">
                    <div class="text-4xl font-bold mb-2">{summary.get("total_python_files", 0):,}</div>
                    <div class="text-blue-200">Fichiers Python</div>
                </div>
            </div>

            <!-- Lignes de Code -->
            <div class="bg-gradient-to-br from-green-600 to-green-800 p-6 rounded-xl shadow-lg">
                <div class="text-center">
                    <div class="text-4xl font-bold mb-2">{summary.get("lines_of_code", 0):,}</div>
                    <div class="text-green-200">Lignes de Code</div>
                </div>
            </div>

            <!-- Tests -->
            <div class="bg-gradient-to-br from-purple-600 to-purple-800 p-6 rounded-xl shadow-lg">
                <div class="text-center">
                    <div class="text-4xl font-bold mb-2">{summary.get("collected_tests", 0):,}</div>
                    <div class="text-purple-200">Tests</div>
                </div>
            </div>

            <!-- Documentation -->
            <div class="bg-gradient-to-br from-orange-600 to-orange-800 p-6 rounded-xl shadow-lg">
                <div class="text-center">
                    <div class="text-4xl font-bold mb-2">{summary.get("documentation_files", 0):,}</div>
                    <div class="text-orange-200">Documentation</div>
                </div>
            </div>
        </div>

        <div class="bg-gray-800 rounded-xl p-6">
            <h2 class="text-2xl font-bold mb-4">📈 Détails des Métriques</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <h3 class="text-lg font-semibold mb-2">🐍 Métriques Python</h3>
                    <ul class="space-y-2 text-gray-300">
                        <li>• Fichiers core: {self.metrics_data.get("python_files", {}).get("core_files", 0)}</li>
                        <li>• Fichiers de test: {self.metrics_data.get("python_files", {}).get("test_files", 0)}</li>
                        <li>• Total lignes: {self.metrics_data.get("python_files", {}).get("total_lines", 0):,}</li>
                    </ul>
                </div>
                <div>
                    <h3 class="text-lg font-semibold mb-2">🧪 Métriques de Tests</h3>
                    <ul class="space-y-2 text-gray-300">
                        <li>• Fichiers de test: {self.metrics_data.get("test_metrics", {}).get("test_files_count", 0)}</li>
                        <li>• Dossiers de test: {self.metrics_data.get("test_metrics", {}).get("test_directories_count", 0)}</li>
                        <li>• Tests collectés: {self.metrics_data.get("test_metrics", {}).get("collected_tests_count", 0)}</li>
                    </ul>
                </div>
            </div>
        </div>

        <footer class="text-center mt-12 text-gray-400">
            <p>Généré par <strong>Arkalia Metrics Collector</strong> v{collection_info.get("collector_version", "1.1.0")}</p>
        </footer>
    </div>
</body>
</html>"""

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            return True

        except OSError as e:
            print(f"Erreur lors de l'export HTML: {e}")
            return False

    def export_csv(self, output_file: str) -> bool:
        """
        Exporte en format CSV pour analyse.

        Args:
            output_file: Chemin du fichier de sortie

        Returns:
            True si l'export a réussi
        """
        try:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            summary = self.metrics_data.get("summary", {})
            collection_info = self.metrics_data.get("collection_info", {})

            with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)

                # En-têtes
                writer.writerow(["Métrique", "Valeur", "Unité"])
                writer.writerow([])

                # Données
                writer.writerow(
                    [
                        "Fichiers Python",
                        summary.get("total_python_files", 0),
                        "fichiers",
                    ]
                )
                writer.writerow(
                    ["Lignes de Code", summary.get("lines_of_code", 0), "lignes"]
                )
                writer.writerow(["Tests", summary.get("collected_tests", 0), "tests"])
                writer.writerow(
                    ["Documentation", summary.get("documentation_files", 0), "fichiers"]
                )
                writer.writerow([])
                writer.writerow(
                    [
                        "Date de collecte",
                        collection_info.get("collection_date", "Inconnu"),
                        "",
                    ]
                )
                writer.writerow(
                    [
                        "Version collecteur",
                        collection_info.get("collector_version", __version__),
                        "",
                    ]
                )

            return True

        except OSError as e:
            print(f"Erreur lors de l'export CSV: {e}")
            return False

    def export_yaml(self, output_file: str) -> bool:
        """
        Exporte en format YAML.

        Args:
            output_file: Chemin du fichier de sortie

        Returns:
            True si l'export a réussi
        """
        if yaml is None:
            print("⚠️  PyYAML n'est pas installé. Installez-le avec: pip install pyyaml")
            return False

        try:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                yaml.dump(
                    self.metrics_data,
                    f,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False,
                )

            return True

        except (OSError, TypeError) as e:
            print(f"Erreur lors de l'export YAML: {e}")
            return False

    def export_all_formats(self, output_dir: str = "metrics") -> dict[str, bool]:
        """
        Exporte dans tous les formats disponibles.

        Args:
            output_dir: Dossier de sortie

        Returns:
            Dictionnaire avec le statut de chaque export
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        results = {}
        results["json"] = self.export_json(str(output_path / "metrics.json"))
        results["markdown"] = self.export_markdown_summary(
            str(output_path / "metrics.md")
        )
        results["html"] = self.export_html_dashboard(
            str(output_path / "dashboard.html")
        )
        results["csv"] = self.export_csv(str(output_path / "metrics.csv"))
        results["yaml"] = self.export_yaml(str(output_path / "metrics.yaml"))

        return results
