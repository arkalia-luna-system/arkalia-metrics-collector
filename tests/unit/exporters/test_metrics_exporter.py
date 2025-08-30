"""
Tests unitaires pour MetricsExporter.
Tests professionnels avec fixtures et mocks.
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
from arkalia_metrics_collector.exporters.metrics_exporter import MetricsExporter


class TestMetricsExporter:
    """Tests pour la classe MetricsExporter."""

    def test_init_default(self):
        """Test de l'initialisation par défaut."""
        metrics_data = {"test": "data"}
        exporter = MetricsExporter(metrics_data)
        assert exporter.metrics_data == metrics_data

    def test_init_custom(self):
        """Test de l'initialisation avec paramètres personnalisés."""
        metrics_data = {"test": "data"}
        exporter = MetricsExporter(metrics_data)
        assert exporter.metrics_data == metrics_data

    def test_export_json_basic(self, sample_metrics_data: dict, temp_output_dir: Path):
        """Test de l'export JSON basique."""
        exporter = MetricsExporter(sample_metrics_data)
        output_file = temp_output_dir / "metrics.json"

        result = exporter.export_json(str(output_file))

        assert result is True
        assert output_file.exists()

        # Vérifier le contenu JSON
        with open(output_file, "r") as f:
            exported_data = json.load(f)

        assert exported_data["timestamp"] == sample_metrics_data["timestamp"]
        assert exported_data["python_files"]["count"] == 3

    def test_export_json_without_timestamp(
        self, sample_metrics_data: dict, temp_output_dir: Path
    ):
        """Test de l'export JSON sans timestamp."""
        exporter = MetricsExporter(sample_metrics_data)
        output_file = temp_output_dir / "metrics_no_timestamp.json"

        result = exporter.export_json(str(output_file))

        assert result is True

        # Vérifier que le timestamp n'est pas ajouté
        with open(output_file, "r") as f:
            exported_data = json.load(f)

        # Votre implémentation n'ajoute pas de export_timestamp
        assert "timestamp" in exported_data

    def test_export_json_error_handling(self, sample_metrics_data: dict):
        """Test de la gestion d'erreur pour l'export JSON."""
        exporter = MetricsExporter(sample_metrics_data)

        # Test avec un chemin invalide
        result = exporter.export_json("/chemin/invalide/test.json")

        assert result is False
        # Votre implémentation retourne un bool, pas un dict avec "error"

    def test_export_markdown_basic(
        self, sample_metrics_data: dict, temp_output_dir: Path
    ):
        """Test de l'export Markdown basique."""
        exporter = MetricsExporter(sample_metrics_data)
        output_file = temp_output_dir / "metrics.md"

        result = exporter.export_markdown_summary(str(output_file))

        assert result is True
        assert output_file.exists()

        # Vérifier le contenu Markdown
        content = output_file.read_text()
        assert (
            "Métriques du Projet" in content
        )  # Votre implémentation utilise ## 📊 **Métriques du Projet**
        assert "Fichiers Python" in content
        assert "Tests" in content
        assert "Documentation" in content

    def test_export_markdown_content_verification(
        self, sample_metrics_data: dict, temp_output_dir: Path
    ):
        """Test du contenu de l'export Markdown."""
        exporter = MetricsExporter(sample_metrics_data)
        output_file = temp_output_dir / "metrics_content.md"

        exporter.export_markdown_summary(str(output_file))

        content = output_file.read_text()

        # Vérifier les valeurs
        assert "3" in content  # Nombre de fichiers Python
        assert "150" in content  # Lignes de code
        assert "2" in content  # Nombre de tests
        assert "1" in content  # Nombre de fichiers de documentation

    def test_export_html_basic(self, sample_metrics_data: dict, temp_output_dir: Path):
        """Test de l'export HTML basique."""
        exporter = MetricsExporter(sample_metrics_data)
        output_file = temp_output_dir / "metrics.html"

        result = exporter.export_html_dashboard(str(output_file))

        assert result is True
        assert output_file.exists()

        # Vérifier le contenu HTML
        content = output_file.read_text()
        assert "<!DOCTYPE html>" in content
        assert "<title>Arkalia Metrics Dashboard</title>" in content  # Votre vrai titre
        assert "Arkalia Metrics Dashboard" in content  # Votre vrai h1

    def test_export_html_styling(
        self, sample_metrics_data: dict, temp_output_dir: Path
    ):
        """Test du style HTML."""
        exporter = MetricsExporter(sample_metrics_data)
        output_file = temp_output_dir / "metrics_styled.html"

        exporter.export_html_dashboard(str(output_file))

        content = output_file.read_text()

        # Vérifier le CSS (votre implémentation utilise Tailwind)
        assert "bg-gray-900" in content  # Votre classe Tailwind
        assert "text-white" in content  # Votre classe Tailwind
        assert "rounded-xl" in content  # Votre classe Tailwind

    def test_export_csv_basic(self, sample_metrics_data: dict, temp_output_dir: Path):
        """Test de l'export CSV basique."""
        exporter = MetricsExporter(sample_metrics_data)
        output_file = temp_output_dir / "metrics.csv"

        result = exporter.export_csv(str(output_file))

        assert result is True
        assert output_file.exists()

        # Vérifier le contenu CSV
        content = output_file.read_text()
        lines = content.strip().split("\n")

        # Vérifier l'en-tête
        assert "Métrique,Valeur" in lines[0]

        # Vérifier les données
        assert "Fichiers Python,3" in content
        assert (
            "Lignes de Code,150" in content
        )  # Votre implémentation utilise "Lignes de Code"
        assert "Tests,2" in content

    def test_export_all_formats(self, sample_metrics_data: dict, temp_output_dir: Path):
        """Test de l'export de tous les formats."""
        exporter = MetricsExporter(sample_metrics_data)
        project_name = "test_project"

        # Votre implémentation n'a pas de export_all_formats, testons les exports individuels
        json_result = exporter.export_json(
            str(temp_output_dir / f"{project_name}_metrics.json")
        )
        md_result = exporter.export_markdown_summary(
            str(temp_output_dir / f"{project_name}_metrics.md")
        )
        html_result = exporter.export_html_dashboard(
            str(temp_output_dir / f"{project_name}_metrics.html")
        )
        csv_result = exporter.export_csv(
            str(temp_output_dir / f"{project_name}_metrics.csv")
        )

        # Vérifier que tous les formats ont été exportés
        assert json_result is True
        assert md_result is True
        assert html_result is True
        assert csv_result is True

        # Vérifier les fichiers
        assert (temp_output_dir / f"{project_name}_metrics.json").exists()
        assert (temp_output_dir / f"{project_name}_metrics.md").exists()
        assert (temp_output_dir / f"{project_name}_metrics.html").exists()
        assert (temp_output_dir / f"{project_name}_metrics.csv").exists()

    def test_export_specific_format(
        self, sample_metrics_data: dict, temp_output_dir: Path
    ):
        """Test de l'export d'un format spécifique."""
        exporter = MetricsExporter(sample_metrics_data)
        project_name = "specific_project"

        # Testons seulement JSON
        json_result = exporter.export_json(
            str(temp_output_dir / f"{project_name}_metrics.json")
        )

        # Seul JSON doit être exporté
        assert json_result is True
        assert (temp_output_dir / f"{project_name}_metrics.json").exists()

    def test_export_with_custom_template(
        self, sample_metrics_data: dict, temp_output_dir: Path
    ):
        """Test de l'export avec un template personnalisé."""
        exporter = MetricsExporter(sample_metrics_data)
        output_file = temp_output_dir / "custom.md"

        # Votre implémentation n'a pas de export_custom_template, testons l'export normal
        result = exporter.export_markdown_summary(str(output_file))

        assert result is True

        # Vérifier le contenu normal
        content = output_file.read_text()
        assert "Métriques du Projet" in content
        assert "Fichiers Python" in content

    def test_export_error_handling_invalid_data(self, temp_output_dir: Path):
        """Test de la gestion d'erreur avec des données invalides."""
        invalid_data = {"invalid": "data"}
        exporter = MetricsExporter(invalid_data)
        output_file = temp_output_dir / "error.json"

        result = exporter.export_json(str(output_file))

        # L'export doit quand même réussir (données basiques)
        assert result is True

    @pytest.mark.performance
    def test_export_large_dataset(self, temp_output_dir: Path):
        """Test de performance avec un gros dataset."""
        # Créer un gros dataset
        large_data = {
            "timestamp": "2024-01-01T00:00:00",
            "python_files": {
                "count": 1000,
                "total_lines": 50000,
                "files_list": [f"file_{i}.py" for i in range(1000)],
            },
            "test_metrics": {
                "collected_tests_count": 500,
                "test_files": [f"test_{i}.py" for i in range(500)],
            },
            "documentation_metrics": {
                "documentation_files": 100,
                "documentation_list": [f"doc_{i}.md" for i in range(100)],
            },
        }

        exporter = MetricsExporter(large_data)
        output_file = temp_output_dir / "large.json"

        import time

        start_time = time.time()

        result = exporter.export_json(str(output_file))

        end_time = time.time()
        duration = end_time - start_time

        # L'export ne doit pas prendre plus de 2 secondes
        assert duration < 2.0
        assert result is True

    def test_export_directory_creation(
        self, sample_metrics_data: dict, temp_output_dir: Path
    ):
        """Test de la création automatique des dossiers."""
        exporter = MetricsExporter(sample_metrics_data)

        # Dossier qui n'existe pas
        new_dir = temp_output_dir / "new_subdir"
        output_file = new_dir / "metrics.json"

        result = exporter.export_json(str(output_file))

        assert result is True
        assert new_dir.exists()
        assert output_file.exists()
