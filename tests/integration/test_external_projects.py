#!/usr/bin/env python3
"""
Tests d'intégration pour projets externes.

Valide le fonctionnement du collecteur sur des projets réels
avec des structures et tailles différentes.
"""

from pathlib import Path

import pytest

from arkalia_metrics_collector import (
    MetricsCollector,
    MetricsExporter,
    MetricsValidator,
)


class TestExternalProjectsIntegration:
    """Tests d'intégration sur projets externes."""

    @pytest.fixture
    def mock_external_project(self, tmp_path: Path) -> Path:
        """Crée un projet externe simulé pour les tests."""
        project = tmp_path / "external_project"
        project.mkdir()

        # Structure de projet Python typique
        src_dir = project / "src" / "external_package"
        src_dir.mkdir(parents=True)

        tests_dir = project / "tests"
        tests_dir.mkdir()

        docs_dir = project / "docs"
        docs_dir.mkdir()

        # Fichiers source
        (src_dir / "__init__.py").write_text('"""Package externe."""\n')
        (src_dir / "core.py").write_text(
            '''"""Module principal."""
def main():
    """Fonction principale."""
    return "Hello World"

class ExternalClass:
    """Classe externe."""

    def __init__(self):
        self.value = 42

    def process(self, data):
        """Traite les données."""
        return data * 2
'''
        )
        (src_dir / "utils.py").write_text(
            '''"""Utilitaires."""
import os
from typing import List

def get_files(directory: str) -> List[str]:
    """Récupère la liste des fichiers."""
    return os.listdir(directory)

def validate_path(path: str) -> bool:
    """Valide un chemin."""
    return os.path.exists(path)
'''
        )

        # Fichiers de test
        (tests_dir / "__init__.py").write_text('"""Tests du package externe."""\n')
        (tests_dir / "test_core.py").write_text(
            '''"""Tests du module core."""
import pytest
from external_package.core import main, ExternalClass

def test_main():
    """Test de la fonction main."""
    assert main() == "Hello World"

def test_external_class():
    """Test de la classe ExternalClass."""
    obj = ExternalClass()
    assert obj.value == 42
    assert obj.process(5) == 10

def test_external_class_process_zero():
    """Test avec valeur zéro."""
    obj = ExternalClass()
    assert obj.process(0) == 0
'''
        )
        (tests_dir / "test_utils.py").write_text(
            '''"""Tests des utilitaires."""
import pytest
from external_package.utils import get_files, validate_path
from unittest.mock import patch

def test_get_files():
    """Test de get_files."""
    with patch('os.listdir', return_value=['file1.txt', 'file2.py']):
        files = get_files('/test')
        assert files == ['file1.txt', 'file2.py']

def test_validate_path():
    """Test de validate_path."""
    with patch('os.path.exists', return_value=True):
        assert validate_path('/test/path') is True

    with patch('os.path.exists', return_value=False):
        assert validate_path('/test/path') is False
'''
        )

        # Documentation
        (docs_dir / "README.md").write_text(
            """# External Package

Package externe pour les tests d'intégration.

## Installation

```bash
pip install external-package
```

## Usage

```python
from external_package import main
print(main())
```
"""
        )
        (docs_dir / "api.md").write_text(
            """# API Reference

## Functions

### main()
Fonction principale du package.

## Classes

### ExternalClass
Classe principale avec méthode process().
"""
        )

        # Configuration
        (project / "pyproject.toml").write_text(
            """[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "external-package"
version = "1.0.0"
description = "Package externe pour tests"
authors = [{name = "Test Author", email = "test@example.com"}]
"""
        )

        return project

    def test_external_project_collection(self, mock_external_project: Path):
        """Test de collecte sur projet externe simulé."""
        collector = MetricsCollector(str(mock_external_project))
        metrics = collector.collect_all_metrics()

        # Vérifications de base
        assert "timestamp" in metrics
        assert "project_root" in metrics
        assert "python_files" in metrics
        assert "test_metrics" in metrics
        assert "documentation_metrics" in metrics
        assert "summary" in metrics

        # Vérifications spécifiques
        python_files = metrics["python_files"]
        assert python_files["count"] >= 4  # Au moins 4 fichiers Python
        assert python_files["total_lines"] > 0
        
        # Vérification compatible Windows/Unix
        files_list = python_files["files_list"]
        assert any("__init__.py" in f and "external_package" in f for f in files_list)
        assert any("core.py" in f and "external_package" in f for f in files_list)

        test_metrics = metrics["test_metrics"]
        assert test_metrics["test_files_count"] >= 2  # Au moins 2 fichiers de test
        assert test_metrics["collected_tests_count"] >= 2  # Au moins 2 tests
        
        # Vérification compatible Windows/Unix
        test_files_list = test_metrics["test_files_list"]
        assert any("test_core.py" in f for f in test_files_list)

        doc_metrics = metrics["documentation_metrics"]
        assert doc_metrics["documentation_files"] >= 2  # Au moins 2 fichiers de doc
        
        # Vérification compatible Windows/Unix
        doc_list = doc_metrics["documentation_list"]
        assert any("README.md" in f for f in doc_list)

    def test_external_project_validation(self, mock_external_project: Path):
        """Test de validation sur projet externe."""
        collector = MetricsCollector(str(mock_external_project))
        metrics = collector.collect_all_metrics()

        validator = MetricsValidator()
        is_valid, errors, warnings = validator.validate_metrics(metrics)

        # Le projet doit être valide
        assert is_valid is True
        assert len(errors) == 0
        # Peut avoir des avertissements mais pas d'erreurs

    def test_external_project_export(self, mock_external_project: Path, tmp_path: Path):
        """Test d'export sur projet externe."""
        collector = MetricsCollector(str(mock_external_project))
        metrics = collector.collect_all_metrics()

        exporter = MetricsExporter(metrics)
        output_dir = tmp_path / "external_output"
        output_dir.mkdir()

        # Test export JSON
        json_file = output_dir / "external_metrics.json"
        assert exporter.export_json(str(json_file)) is True
        assert json_file.exists()

        # Test export Markdown
        md_file = output_dir / "external_metrics.md"
        assert exporter.export_markdown_summary(str(md_file)) is True
        assert md_file.exists()

        # Test export HTML
        html_file = output_dir / "external_dashboard.html"
        assert exporter.export_html_dashboard(str(html_file)) is True
        assert html_file.exists()

        # Test export CSV
        csv_file = output_dir / "external_metrics.csv"
        assert exporter.export_csv(str(csv_file)) is True
        assert csv_file.exists()

    def test_external_project_performance(self, mock_external_project: Path):
        """Test de performance sur projet externe."""
        import time

        collector = MetricsCollector(str(mock_external_project))

        # Mesurer le temps de collecte
        start_time = time.time()
        metrics = collector.collect_all_metrics()
        end_time = time.time()

        collection_time = end_time - start_time

        # La collecte doit être rapide (< 5 secondes)
        assert collection_time < 5.0

        # Vérifier que les métriques sont complètes
        assert metrics["python_files"]["count"] > 0
        assert metrics["test_metrics"]["collected_tests_count"] > 0

    def test_external_project_error_handling(self):
        """Test de gestion d'erreur avec projet inexistant."""
        # Test avec chemin inexistant
        collector = MetricsCollector("/chemin/inexistant/projet")

        # Le collecteur doit s'initialiser sans erreur
        assert collector.project_root is not None

        # Mais la collecte peut échouer gracieusement
        try:
            metrics = collector.collect_all_metrics()
            # Si ça marche, vérifier que c'est cohérent
            assert isinstance(metrics, dict)
        except Exception:
            # C'est acceptable si ça échoue
            pass

    def test_external_project_large_structure(self, tmp_path: Path):
        """Test avec structure de projet plus large."""
        project = tmp_path / "large_external_project"
        project.mkdir()

        # Créer une structure plus complexe
        for module in ["auth", "api", "database", "utils"]:
            module_dir = project / "src" / "external_package" / module
            module_dir.mkdir(parents=True)

            (module_dir / "__init__.py").write_text(f'"""Module {module}."""\n')
            (module_dir / f"{module}.py").write_text(
                f'''"""Module {module} principal."""
def {module}_function():
    """Fonction du module {module}."""
    return "{module}_result"
'''
            )

        # Tests correspondants
        for module in ["auth", "api", "database", "utils"]:
            test_dir = project / "tests" / module
            test_dir.mkdir(parents=True)

            (test_dir / f"test_{module}.py").write_text(
                f'''"""Tests du module {module}."""
import pytest
from external_package.{module}.{module} import {module}_function

def test_{module}_function():
    """Test de la fonction {module}."""
    assert {module}_function() == "{module}_result"
'''
            )

        # Test de collecte
        collector = MetricsCollector(str(project))
        metrics = collector.collect_all_metrics()

        # Vérifications
        assert metrics["python_files"]["count"] >= 8  # 4 modules * 2 fichiers
        assert metrics["test_metrics"]["test_files_count"] >= 4  # 4 fichiers de test
        assert metrics["test_metrics"]["collected_tests_count"] >= 4  # 4 tests

    @pytest.mark.integration
    def test_real_world_simulation(self, tmp_path: Path):
        """Simulation d'un projet du monde réel."""
        project = tmp_path / "real_world_project"
        project.mkdir()

        # Structure typique d'un projet Python professionnel
        structure = {
            "src/package/": [
                "__init__.py",
                "core.py",
                "models.py",
                "api.py",
                "utils.py",
            ],
            "tests/": ["__init__.py", "test_core.py", "test_models.py", "test_api.py"],
            "docs/": ["README.md", "CHANGELOG.md", "CONTRIBUTING.md"],
            "scripts/": ["deploy.py", "setup.py"],
            "config/": ["settings.yaml", "logging.yaml"],
        }

        for dir_path, files in structure.items():
            full_dir = project / dir_path
            full_dir.mkdir(parents=True)

            for file_name in files:
                file_path = full_dir / file_name
                if file_name.endswith(".py"):
                    file_path.write_text(f'"""Module {file_name}."""\n# Code Python\n')
                else:
                    file_path.write_text(f"# {file_name}\nContenu du fichier\n")

        # Test complet
        collector = MetricsCollector(str(project))
        metrics = collector.collect_all_metrics()

        validator = MetricsValidator()
        is_valid, errors, warnings = validator.validate_metrics(metrics)

        # Le projet doit être valide
        assert is_valid is True
        assert len(errors) == 0

        # Vérifications de cohérence
        summary = metrics["summary"]
        python_files = metrics["python_files"]
        test_metrics = metrics["test_metrics"]

        assert summary["total_python_files"] == python_files["count"]
        assert summary["collected_tests"] == test_metrics["collected_tests_count"]
        assert summary["lines_of_code"] == python_files["total_lines"]
