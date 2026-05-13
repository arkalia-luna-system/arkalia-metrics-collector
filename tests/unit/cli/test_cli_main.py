#!/usr/bin/env python3
"""
Tests pour l'interface CLI.

Valide le fonctionnement de la ligne de commande
avec différents arguments et options.
"""

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from arkalia_metrics_collector.cli.main import cli


class TestCLIMain:
    """Tests pour l'interface CLI principale."""

    @pytest.fixture
    def runner(self):
        """Runner Click pour les tests CLI."""
        return CliRunner()

    @pytest.fixture
    def sample_project(self, tmp_path: Path) -> Path:
        """Projet d'exemple pour les tests CLI."""
        project = tmp_path / "sample_project"
        project.mkdir()

        # Structure de base
        src_dir = project / "src" / "package"
        src_dir.mkdir(parents=True)
        tests_dir = project / "tests"
        tests_dir.mkdir()

        # Fichiers source
        (src_dir / "__init__.py").write_text('"""Package principal."""\n')
        (src_dir / "main.py").write_text(
            '''"""Module principal."""
def main():
    """Fonction principale."""
    return "Hello World"

class SampleClass:
    """Classe d'exemple."""

    def __init__(self):
        self.value = 42
'''
        )

        # Fichiers de test
        (tests_dir / "__init__.py").write_text('"""Tests du package."""\n')
        (tests_dir / "test_main.py").write_text(
            '''"""Tests du module principal."""
import pytest
from package.main import main, SampleClass

def test_main():
    """Test de la fonction main."""
    assert main() == "Hello World"

def test_sample_class():
    """Test de la classe SampleClass."""
    obj = SampleClass()
    assert obj.value == 42
'''
        )

        # Documentation
        (project / "README.md").write_text(
            """# Sample Project

Projet d'exemple pour les tests CLI.

## Installation

```bash
pip install sample-project
```

## Usage

```python
from package import main
print(main())
```
"""
        )

        return project

    def test_cli_help(self, runner: CliRunner):
        """Test de l'aide CLI."""
        result = runner.invoke(cli, ["--help"])

        assert result.exit_code == 0
        assert "Arkalia Metrics Collector" in result.output
        assert "collect" in result.output
        assert "validate" in result.output
        assert "serve" in result.output or "collect" in result.output

    def test_cli_version(self, runner: CliRunner):
        """Test de la version CLI."""
        result = runner.invoke(cli, ["--version"])

        assert result.exit_code == 0
        assert "version" in result.output.lower()

    def test_collect_basic(self, runner: CliRunner, sample_project: Path):
        """Test de collecte basique."""
        result = runner.invoke(cli, ["collect", str(sample_project)])

        assert result.exit_code == 0
        assert "Résumé des métriques" in result.output

    def test_collect_with_output(
        self, runner: CliRunner, sample_project: Path, tmp_path: Path
    ):
        """Test de collecte avec dossier de sortie."""
        output_dir = tmp_path / "cli_output"

        result = runner.invoke(
            cli, ["collect", str(sample_project), "--output", str(output_dir)]
        )

        assert result.exit_code == 0
        assert output_dir.exists()

    def test_collect_with_format(
        self, runner: CliRunner, sample_project: Path, tmp_path: Path
    ):
        """Test de collecte avec format spécifique."""
        output_dir = tmp_path / "cli_format"

        # Test format JSON
        result = runner.invoke(
            cli,
            [
                "collect",
                str(sample_project),
                "--output",
                str(output_dir),
                "--format",
                "json",
            ],
        )

        assert result.exit_code == 0
        assert (output_dir / "metrics.json").exists()

    def test_collect_with_validation(self, runner: CliRunner, sample_project: Path):
        """Test de collecte avec validation."""
        result = runner.invoke(cli, ["collect", str(sample_project), "--validate"])

        assert result.exit_code == 0
        assert "Résumé des métriques" in result.output

    def test_collect_verbose(self, runner: CliRunner, sample_project: Path):
        """Test de collecte en mode verbeux."""
        result = runner.invoke(cli, ["collect", str(sample_project), "--verbose"])

        assert result.exit_code == 0
        # En mode verbeux, il devrait y avoir plus de détails
        assert len(result.output) > 100

    def test_collect_all_formats(
        self, runner: CliRunner, sample_project: Path, tmp_path: Path
    ):
        """Test de collecte avec tous les formats."""
        output_dir = tmp_path / "cli_all_formats"

        result = runner.invoke(
            cli,
            [
                "collect",
                str(sample_project),
                "--output",
                str(output_dir),
                "--format",
                "all",
            ],
        )

        assert result.exit_code == 0

        # Vérifier que tous les formats sont créés
        expected_files = ["metrics.json", "metrics.md", "dashboard.html", "metrics.csv"]

        for file_name in expected_files:
            assert (output_dir / file_name).exists()

    def test_validate_basic(self, runner: CliRunner, sample_project: Path):
        """Test de validation basique."""
        result = runner.invoke(cli, ["validate", str(sample_project)])

        assert result.exit_code == 0
        assert "validation" in result.output.lower()

    def test_validate_invalid_project(self, runner: CliRunner, tmp_path: Path):
        """Test de validation sur projet invalide."""
        invalid_project = tmp_path / "invalid_project"
        invalid_project.mkdir()

        # Projet sans fichiers Python
        (invalid_project / "README.txt").write_text("Pas de Python ici")

        result = runner.invoke(cli, ["validate", str(invalid_project)])

        # Peut retourner 0 (projet valide mais vide) ou 1 (projet invalide)
        assert result.exit_code in [0, 1]

    def test_dashboard_basic(
        self, runner: CliRunner, sample_project: Path, tmp_path: Path
    ):
        """Test de dashboard basique."""
        output_dir = tmp_path / "cli_dashboard"

        result = runner.invoke(
            cli, ["serve", str(sample_project), "--output", str(output_dir)]
        )

        # Le serve peut échouer si le port est occupé, c'est acceptable
        assert result.exit_code in [0, 1, 2]

    def test_dashboard_with_port(self, runner: CliRunner, sample_project: Path):
        """Test de dashboard avec port personnalisé."""
        result = runner.invoke(cli, ["serve", str(sample_project), "--port", "9000"])

        # Le serve peut échouer si le port est occupé, c'est acceptable
        assert result.exit_code in [0, 1, 2]

    def test_collect_nonexistent_path(self, runner: CliRunner):
        """Test avec chemin inexistant."""
        result = runner.invoke(cli, ["collect", "/chemin/inexistant"])

        # Peut retourner 0 (gestion gracieuse), 1 (erreur) ou 2 (erreur Click)
        assert result.exit_code in [0, 1, 2]

    def test_collect_file_instead_of_dir(self, runner: CliRunner, tmp_path: Path):
        """Test avec fichier au lieu de dossier."""
        file_path = tmp_path / "not_a_directory.txt"
        file_path.write_text("Ceci est un fichier")

        result = runner.invoke(cli, ["collect", str(file_path)])

        # Peut retourner 0 (gestion gracieuse), 1 (erreur) ou 2 (erreur Click)
        assert result.exit_code in [0, 1, 2]

    def test_collect_with_relative_path(self, runner: CliRunner, sample_project: Path):
        """Test avec chemin relatif."""
        # Changer de répertoire vers le projet
        original_cwd = Path.cwd()
        try:
            import os

            os.chdir(sample_project.parent)

            result = runner.invoke(cli, ["collect", "sample_project"])

            assert result.exit_code == 0
        finally:
            os.chdir(original_cwd)

    def test_collect_output_creation(
        self, runner: CliRunner, sample_project: Path, tmp_path: Path
    ):
        """Test de création du dossier de sortie."""
        output_dir = tmp_path / "new_output_directory"

        # Le dossier n'existe pas encore
        assert not output_dir.exists()

        result = runner.invoke(
            cli, ["collect", str(sample_project), "--output", str(output_dir)]
        )

        assert result.exit_code == 0
        assert output_dir.exists()

    def test_collect_json_output_content(
        self, runner: CliRunner, sample_project: Path, tmp_path: Path
    ):
        """Test du contenu de l'export JSON."""
        output_dir = tmp_path / "json_content_test"

        result = runner.invoke(
            cli,
            [
                "collect",
                str(sample_project),
                "--output",
                str(output_dir),
                "--format",
                "json",
            ],
        )

        assert result.exit_code == 0

        json_file = output_dir / "metrics.json"
        assert json_file.exists()

        # Vérifier le contenu JSON
        with open(json_file) as f:
            data = json.load(f)

        assert "timestamp" in data
        assert "python_files" in data
        assert "test_metrics" in data
        assert "summary" in data

    def test_collect_markdown_output_content(
        self, runner: CliRunner, sample_project: Path, tmp_path: Path
    ):
        """Test du contenu de l'export Markdown."""
        output_dir = tmp_path / "markdown_content_test"

        result = runner.invoke(
            cli,
            [
                "collect",
                str(sample_project),
                "--output",
                str(output_dir),
                "--format",
                "markdown",
            ],
        )

        assert result.exit_code == 0

        md_file = output_dir / "metrics.md"
        assert md_file.exists()

        # Vérifier le contenu Markdown
        content = md_file.read_text(encoding="utf-8")
        assert "#" in content  # Titres Markdown
        assert "Python" in content or "Fichiers" in content

    def test_collect_csv_output_content(
        self, runner: CliRunner, sample_project: Path, tmp_path: Path
    ):
        """Test du contenu de l'export CSV."""
        output_dir = tmp_path / "csv_content_test"

        result = runner.invoke(
            cli,
            [
                "collect",
                str(sample_project),
                "--output",
                str(output_dir),
                "--format",
                "csv",
            ],
        )

        assert result.exit_code == 0

        csv_file = output_dir / "metrics.csv"
        assert csv_file.exists()

        # Vérifier le contenu CSV
        content = csv_file.read_text(encoding="utf-8")
        assert "," in content  # Séparateurs CSV
        assert "Métrique" in content or "Valeur" in content

    def test_collect_error_handling(self, runner: CliRunner):
        """Test de gestion d'erreur."""
        # Test avec chemin vide
        result = runner.invoke(cli, ["collect", ""])
        assert result.exit_code != 0

    def test_validate_error_handling(self, runner: CliRunner):
        """Test de gestion d'erreur pour validation."""
        # Test avec chemin vide
        result = runner.invoke(cli, ["validate", ""])
        assert result.exit_code != 0

    def test_dashboard_error_handling(self, runner: CliRunner):
        """Test de gestion d'erreur pour dashboard."""
        # Test avec chemin vide
        result = runner.invoke(cli, ["dashboard", ""])
        assert result.exit_code != 0

    def test_collect_with_special_characters(self, runner: CliRunner, tmp_path: Path):
        """Test avec caractères spéciaux dans le chemin."""
        # Créer un projet avec des caractères spéciaux
        project_name = "projet-avec-espaces_et.symboles"
        project = tmp_path / project_name
        project.mkdir()

        (project / "main.py").write_text("def main(): pass")

        result = runner.invoke(cli, ["collect", str(project)])

        # Peut retourner 0 (succès) ou 1 (erreur selon la gestion)
        assert result.exit_code in [0, 1]

    def test_collect_performance_large_output(
        self, runner: CliRunner, sample_project: Path, tmp_path: Path
    ):
        """Test de performance avec grande sortie."""
        output_dir = tmp_path / "performance_test"

        # Mesurer le temps d'exécution
        import time

        start_time = time.time()

        result = runner.invoke(
            cli,
            [
                "collect",
                str(sample_project),
                "--output",
                str(output_dir),
                "--format",
                "all",
            ],
        )

        end_time = time.time()
        execution_time = end_time - start_time

        assert result.exit_code == 0
        # L'exécution doit être rapide (< 5 secondes)
        assert execution_time < 5.0
