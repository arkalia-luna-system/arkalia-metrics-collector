#!/usr/bin/env python3
"""
Arkalia Metrics Collector - Agrégateur Multi-Projets.

Agrège les métriques de plusieurs projets pour générer :
- Coverage global
- Total de modules Python
- Métriques agrégées
- Tableau récapitulatif
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .metrics_collector import MetricsCollector
from .metrics_history import MetricsHistory


class MultiProjectAggregator:
    """
    Agrégateur de métriques pour plusieurs projets.

    Collecte et agrège les métriques de plusieurs projets pour :
    - Calculer le coverage global
    - Compter le total de modules Python
    - Générer des métriques agrégées
    - Créer des tableaux récapitulatifs
    """

    def __init__(self, enable_history: bool = True) -> None:
        """
        Initialise l'agrégateur multi-projets.

        Args:
            enable_history: Activer la sauvegarde de l'historique
        """
        self.projects_metrics: dict[str, Any] = {}
        self.history = MetricsHistory() if enable_history else None

    def collect_project(
        self, project_name: str, project_path: str | Path
    ) -> dict[str, Any] | None:
        """
        Collecte les métriques d'un projet.

        Args:
            project_name: Nom du projet
            project_path: Chemin vers le projet

        Returns:
            Métriques du projet ou None en cas d'erreur
        """
        try:
            collector = MetricsCollector(str(project_path))
            metrics = collector.collect_all_metrics()
            self.projects_metrics[project_name] = {
                "name": project_name,
                "path": str(project_path),
                "metrics": metrics,
                "collection_date": datetime.now().isoformat(),
            }
            return metrics
        except Exception:
            return None

    def load_from_json(self, json_file: str | Path) -> bool:
        """
        Charge les métriques depuis un fichier JSON.

        Args:
            json_file: Chemin vers le fichier JSON

        Returns:
            True si le chargement a réussi
        """
        try:
            json_path = Path(json_file)
            if not json_path.exists():
                return False

            with open(json_path, encoding="utf-8") as f:
                data = json.load(f)

            # Si c'est un dictionnaire de projets
            if isinstance(data, dict):
                if "projects" in data:
                    self.projects_metrics = data["projects"]
                else:
                    # Format simple: {project_name: metrics}
                    self.projects_metrics = data

            return True

        except Exception:
            return False

    def aggregate_metrics(self) -> dict[str, Any]:
        """
        Agrège toutes les métriques collectées.

        Returns:
            Dictionnaire avec les métriques agrégées
        """
        if not self.projects_metrics:
            return {}

        total_python_files = 0
        total_lines_of_code = 0
        total_tests = 0
        total_documentation_files = 0
        total_modules = 0

        projects_summary = []

        for project_name, project_data in self.projects_metrics.items():
            metrics = project_data.get("metrics", {})
            summary = metrics.get("summary", {})

            python_files = summary.get("total_python_files", 0)
            lines = summary.get("lines_of_code", 0)
            tests = summary.get("collected_tests", 0)
            docs = summary.get("documentation_files", 0)

            # Compter les modules (fichiers Python core, excluant les tests)
            python_metrics = metrics.get("python_files", {})
            modules = python_metrics.get("core_files", python_files)

            total_python_files += python_files
            total_lines_of_code += lines
            total_tests += tests
            total_documentation_files += docs
            total_modules += modules

            projects_summary.append(
                {
                    "name": project_name,
                    "path": project_data.get("path", ""),
                    "python_files": python_files,
                    "modules": modules,
                    "lines_of_code": lines,
                    "tests": tests,
                    "documentation_files": docs,
                }
            )

        # Calculer le coverage global (moyenne pondérée si disponible)
        global_coverage = self._calculate_global_coverage()

        return {
            "aggregated": {
                "total_projects": len(self.projects_metrics),
                "total_python_files": total_python_files,
                "total_modules": total_modules,
                "total_lines_of_code": total_lines_of_code,
                "total_tests": total_tests,
                "total_documentation_files": total_documentation_files,
                "global_coverage": global_coverage,
            },
            "projects": projects_summary,
            "collection_date": datetime.now().isoformat(),
        }

    def _calculate_global_coverage(self) -> float | None:
        """
        Calcule le coverage global depuis tous les projets.

        Returns:
            Coverage global en pourcentage ou None si non disponible
        """
        coverages = []
        total_lines = 0

        for project_data in self.projects_metrics.values():
            metrics = project_data.get("metrics", {})
            # Chercher le coverage dans les métriques de test
            test_metrics = metrics.get("test_metrics", {})
            # Le coverage peut être dans différents endroits selon l'implémentation
            # On cherche dans les métriques étendues
            coverage = None

            # Essayer de trouver le coverage dans les métriques
            if "coverage" in metrics:
                coverage = metrics["coverage"]
            elif "coverage_percentage" in test_metrics:
                coverage = test_metrics["coverage_percentage"]
            elif "test_coverage" in test_metrics:
                coverage = test_metrics["test_coverage"]

            if coverage is not None:
                try:
                    coverage_float = float(coverage)
                    lines = metrics.get("summary", {}).get("lines_of_code", 0)
                    if lines > 0:
                        coverages.append((coverage_float, lines))
                        total_lines += lines
                except (ValueError, TypeError):
                    pass

        if not coverages or total_lines == 0:
            return None

        # Calculer la moyenne pondérée
        weighted_sum = sum(coverage * lines for coverage, lines in coverages)
        return round(weighted_sum / total_lines, 2)

    def generate_readme_table(self) -> str:
        """
        Génère un tableau Markdown récapitulatif pour README.

        Returns:
            Tableau Markdown formaté
        """
        aggregated = self.aggregate_metrics()
        agg_data = aggregated.get("aggregated", {})
        projects = aggregated.get("projects", [])

        # En-tête du tableau
        table = "## 📊 **Métriques Globales** *(Mise à jour automatique)*\n\n"
        table += '<div align="center">\n\n'
        table += (
            "| **Projet** | **Modules** | **Lignes** | **Tests** | **Coverage** |\n"
        )
        table += (
            "|:-----------|:-----------:|:----------:|:---------:|:------------:|\n"
        )

        # Lignes pour chaque projet
        for project in sorted(projects, key=lambda x: x["name"]):
            name = project["name"]
            modules = project["modules"]
            lines = project["lines_of_code"]
            tests = project["tests"]
            # Récupérer le coverage depuis les métriques du projet
            project_data = self.projects_metrics.get(name, {})
            project_metrics = project_data.get("metrics", {})
            test_metrics = project_metrics.get("test_metrics", {})
            coverage_value = test_metrics.get("coverage_percentage")
            if coverage_value is not None:
                try:
                    coverage = f"{float(coverage_value):.1f}%"
                except (ValueError, TypeError):
                    coverage = "N/A"
            else:
                coverage = "N/A"

            table += f"| **{name}** | `{modules:,}` | `{lines:,}` | `{tests:,}` | `{coverage}` |\n"

        # Ligne de total
        table += "| **TOTAL** | "
        table += f"**`{agg_data.get('total_modules', 0):,}`** | "
        table += f"**`{agg_data.get('total_lines_of_code', 0):,}`** | "
        table += f"**`{agg_data.get('total_tests', 0):,}`** | "
        global_cov = agg_data.get("global_coverage")
        if global_cov is not None:
            table += f"**`{global_cov}%`** |\n"
        else:
            table += "**N/A** |\n"

        table += "\n</div>\n\n"
        table += f"*Métriques collectées automatiquement le {aggregated.get('collection_date', 'Inconnu')}*\n"

        return table

    def export_aggregated_json(self, output_file: str | Path) -> bool:
        """
        Exporte les métriques agrégées en JSON.

        Args:
            output_file: Chemin du fichier de sortie

        Returns:
            True si l'export a réussi
        """
        try:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            aggregated = self.aggregate_metrics()
            aggregated["projects_details"] = self.projects_metrics

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(aggregated, f, indent=2, ensure_ascii=False)

            # Sauvegarder dans l'historique si activé
            if self.history:
                self.history.save_metrics(aggregated)

            return True

        except Exception:
            return False

    def get_evolution_report(self) -> str:
        """
        Génère un rapport d'évolution des métriques.

        Returns:
            Rapport Markdown avec les deltas
        """
        if not self.history:
            return "## 📈 Évolution des Métriques\n\n*Historique désactivé.*\n"

        current = self.aggregate_metrics()
        comparison = self.history.compare_metrics(current)

        return self.history.generate_evolution_report(comparison)
