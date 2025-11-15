#!/usr/bin/env python3
"""
Tests d'intégration pour la génération du dashboard interactif.
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from arkalia_metrics_collector.exporters.interactive_dashboard import (
    InteractiveDashboardGenerator,
)


class TestDashboardGeneration:
    """Tests pour la génération du dashboard."""

    def test_generate_dashboard_simple_metrics(self):
        """Test la génération du dashboard avec métriques simples."""
        with TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "dashboard.html"

            metrics_data = {
                "summary": {
                    "total_python_files": 100,
                    "lines_of_code": 5000,
                    "collected_tests": 50,
                    "documentation_files": 10,
                },
                "collection_info": {
                    "collection_date": "2025-01-01T00:00:00",
                    "collector_version": "1.0.0",
                },
                "test_metrics": {
                    "coverage_percentage": 80.5,
                },
            }

            success = InteractiveDashboardGenerator.generate_dashboard(
                metrics_data=metrics_data,
                history_data=None,
                output_file=str(output_file),
                is_aggregated=False,
            )

            assert success is True
            assert output_file.exists()

            # Vérifier le contenu
            content = output_file.read_text(encoding="utf-8")
            assert "Arkalia Metrics Dashboard" in content
            assert "100" in content  # Modules
            assert "5,000" in content  # Lignes
            assert (
                "chart.js" in content.lower() or "Chart.js" in content
            )  # Chart.js inclus

    def test_generate_dashboard_aggregated_metrics(self):
        """Test la génération du dashboard avec métriques agrégées."""
        with TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "dashboard.html"

            metrics_data = {
                "aggregated": {
                    "total_modules": 1000,
                    "total_lines_of_code": 50000,
                    "total_tests": 200,
                    "total_documentation_files": 100,
                    "global_coverage": 75.5,
                },
                "projects": [
                    {
                        "name": "project1",
                        "modules": 500,
                        "lines_of_code": 25000,
                        "tests": 100,
                        "coverage": 80.0,
                    },
                    {
                        "name": "project2",
                        "modules": 500,
                        "lines_of_code": 25000,
                        "tests": 100,
                        "coverage": 71.0,
                    },
                ],
                "collection_date": "2025-01-01T00:00:00",
            }

            success = InteractiveDashboardGenerator.generate_dashboard(
                metrics_data=metrics_data,
                history_data=None,
                output_file=str(output_file),
                is_aggregated=True,
            )

            assert success is True
            assert output_file.exists()

            # Vérifier le contenu
            content = output_file.read_text(encoding="utf-8")
            assert "Arkalia Metrics Dashboard" in content
            assert "1,000" in content  # Modules totaux
            assert "project1" in content  # Projet dans le tableau
            assert "project2" in content
            assert "Projets" in content  # Tableau des projets

    def test_generate_dashboard_with_history(self):
        """Test la génération du dashboard avec historique."""
        with TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / "dashboard.html"

            metrics_data = {
                "summary": {
                    "total_python_files": 100,
                    "lines_of_code": 5000,
                    "collected_tests": 50,
                    "documentation_files": 10,
                },
                "collection_info": {
                    "collection_date": "2025-01-03T00:00:00",
                    "collector_version": "1.0.0",
                },
                "test_metrics": {},
            }

            history_data = [
                {
                    "aggregated": {
                        "total_modules": 90,
                        "total_lines_of_code": 4500,
                        "total_tests": 45,
                    },
                    "saved_at": "2025-01-01T00:00:00",
                },
                {
                    "aggregated": {
                        "total_modules": 95,
                        "total_lines_of_code": 4750,
                        "total_tests": 48,
                    },
                    "saved_at": "2025-01-02T00:00:00",
                },
            ]

            success = InteractiveDashboardGenerator.generate_dashboard(
                metrics_data=metrics_data,
                history_data=history_data,
                output_file=str(output_file),
                is_aggregated=False,
            )

            assert success is True
            assert output_file.exists()

            # Vérifier que les graphiques sont inclus
            content = output_file.read_text(encoding="utf-8")
            assert "modulesChart" in content
            assert "linesChart" in content
            assert "testsChart" in content
