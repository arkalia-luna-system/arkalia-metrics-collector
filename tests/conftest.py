"""
Configuration professionnelle récupérée d'Athalia Core.
"""

import shutil
import tempfile
from collections.abc import Generator
from pathlib import Path
from typing import Any
from unittest.mock import Mock, patch

import pytest

# Import des modules à tester
from arkalia_metrics_collector.collectors.metrics_collector import MetricsCollector
from arkalia_metrics_collector.exporters.metrics_exporter import MetricsExporter
from arkalia_metrics_collector.validators.metrics_validator import MetricsValidator

# ========================================
# FIXTURES DE BASE
# ========================================


@pytest.fixture(scope="session")
def temp_project_dir() -> Generator[Path, None, None]:
    """Crée un répertoire de projet temporaire pour les tests."""
    temp_dir = tempfile.mkdtemp()
    project_dir = Path(temp_dir) / "test_project"
    project_dir.mkdir()

    # Créer une structure de projet de test
    (project_dir / "src").mkdir()
    (project_dir / "tests").mkdir()
    (project_dir / "docs").mkdir()

    # Créer des fichiers Python de test
    (project_dir / "src" / "__init__.py").touch()
    (project_dir / "src" / "main.py").write_text(
        "def main():\n    return 'Hello World'\n"
    )
    (project_dir / "src" / "utils.py").write_text("def helper():\n    return 42\n")

    # Créer des tests
    (project_dir / "tests" / "__init__.py").touch()
    (project_dir / "tests" / "test_main.py").write_text(
        "def test_main():\n    assert True\n"
    )

    # Créer de la documentation
    (project_dir / "docs" / "README.md").write_text(
        "# Test Project\n\nThis is a test.\n"
    )

    yield project_dir

    # Nettoyage
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_metrics_data() -> dict[str, Any]:
    """Données de métriques d'exemple pour les tests."""
    return {
        "timestamp": "2024-01-01T00:00:00",
        "project_root": "/test/project",
        "collection_info": {
            "collector_version": "1.0.0",
            "python_version": "3.10.0",
            "collection_date": "2024-01-01T00:00:00",
        },
        "python_files": {
            "count": 3,
            "total_lines": 150,
            "core_files": 2,
            "test_files": 1,
            "files_list": ["src/main.py", "src/utils.py", "tests/test_main.py"],
        },
        "test_metrics": {
            "collected_tests_count": 2,
            "test_files_count": 1,
            "test_files": ["tests/test_main.py"],
        },
        "documentation_metrics": {
            "documentation_files": 1,
            "documentation_list": ["docs/README.md"],
        },
        "summary": {
            "total_python_files": 3,
            "lines_of_code": 150,
            "collected_tests": 2,
            "documentation_files": 1,
        },
    }


# ========================================
# FIXTURES DES COLLECTORS
# ========================================


@pytest.fixture
def metrics_collector(temp_project_dir: Path) -> MetricsCollector:
    """Instance de MetricsCollector configurée pour les tests."""
    return MetricsCollector(temp_project_dir)


@pytest.fixture
def mock_collector() -> Mock:
    """Collector mocké pour les tests unitaires."""
    mock = Mock(spec=MetricsCollector)
    mock.project_root = Path("/mock/project")
    mock.exclude_patterns = {"__pycache__", ".venv", ".git"}
    return mock


# ========================================
# FIXTURES DES EXPORTERS
# ========================================


@pytest.fixture
def metrics_exporter() -> MetricsExporter:
    """Instance de MetricsExporter pour les tests."""
    return MetricsExporter()


@pytest.fixture
def temp_output_dir() -> Generator[Path, None, None]:
    """Répertoire de sortie temporaire pour les tests d'export."""
    temp_dir = tempfile.mkdtemp()
    output_dir = Path(temp_dir) / "output"
    output_dir.mkdir()

    yield output_dir

    shutil.rmtree(temp_dir)


# ========================================
# FIXTURES DES VALIDATORS
# ========================================


@pytest.fixture
def metrics_validator() -> MetricsValidator:
    """Instance de MetricsValidator pour les tests."""
    return MetricsValidator()


# ========================================
# FIXTURES DES CLI
# ========================================


@pytest.fixture
def cli_runner():
    """Runner CLI pour tester les commandes."""
    from click.testing import CliRunner

    return CliRunner()


# ========================================
# FIXTURES DE PERFORMANCE
# ========================================


@pytest.fixture
def large_project_dir() -> Generator[Path, None, None]:
    """Répertoire de projet avec beaucoup de fichiers pour les tests de performance."""
    temp_dir = tempfile.mkdtemp()
    project_dir = Path(temp_dir) / "large_project"
    project_dir.mkdir()

    # Créer beaucoup de fichiers Python
    for i in range(100):
        file_path = project_dir / f"module_{i}.py"
        file_path.write_text(f"def func_{i}():\n    return {i}\n")

    # Créer des tests
    (project_dir / "tests").mkdir()
    for i in range(20):
        test_file = project_dir / "tests" / f"test_module_{i}.py"
        test_file.write_text(f"def test_func_{i}():\n    assert func_{i}() == {i}\n")

    yield project_dir

    shutil.rmtree(temp_dir)


# ========================================
# MARQUEURS PERSONNALISÉS
# ========================================


def pytest_configure(config):
    """Configuration des marqueurs pytest personnalisés."""
    config.addinivalue_line(
        "markers", "fast: marks tests as fast (deselect with '-m \"not fast\"')"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "performance: marks tests as performance tests")


# ========================================
# UTILITAIRES DE TEST
# ========================================


def create_test_file(path: Path, content: str = "") -> None:
    """Crée un fichier de test avec le contenu spécifié."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content or f"# Test file: {path.name}\n")


def assert_metrics_structure(metrics: dict[str, Any]) -> None:
    """Vérifie que la structure des métriques est correcte."""
    required_keys = [
        "timestamp",
        "project_root",
        "collection_info",
        "python_files",
        "test_metrics",
        "documentation_metrics",
        "summary",
    ]

    for key in required_keys:
        assert key in metrics, f"Clé manquante: {key}"

    # Vérifier la structure des sous-sections
    assert "count" in metrics["python_files"]
    assert "total_lines" in metrics["python_files"]
    assert "collected_tests_count" in metrics["test_metrics"]
    assert "documentation_files" in metrics["documentation_metrics"]
