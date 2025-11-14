#!/usr/bin/env python3
"""
Arkalia Metrics Collector - Collecteur de métriques principal.

Collecte des métriques fiables sur :
- Fichiers Python et lignes de code
- Tests (nombre et couverture)
- Documentation
- Dashboards et scripts
- Sécurité et qualité
"""

import subprocess  # nosec B404
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from arkalia_metrics_collector.collectors.coverage_parser import CoverageParser


class MetricsCollector:
    """
    Collecteur de métriques complet pour les projets Python.

    Collecte des métriques fiables sur :
    - Fichiers Python et lignes de code
    - Tests (nombre et couverture)
    - Documentation
    - Dashboards et scripts
    - Sécurité et qualité

    Attributes:
        project_root: Chemin racine du projet
        exclude_patterns: Patterns de fichiers/dossiers à exclure
        metrics_data: Données des métriques collectées
    """

    def __init__(self, project_root: str = ".") -> None:
        """
        Initialise le collecteur de métriques.

        Args:
            project_root: Chemin racine du projet (défaut: répertoire courant)
        """
        self.project_root = Path(project_root).resolve()
        self.exclude_patterns: set[str] = {
            "__pycache__",
            ".venv",
            ".env",
            "venv",
            "env",
            ".git",
            ".pytest_cache",
            "htmlcov",
            ".coverage",
            ".tox",
            ".mypy_cache",
            "node_modules",
            ".DS_Store",
            "._*",  # AppleDouble files
        }
        self.metrics_data: dict[str, Any] = {}

    def _is_excluded(self, path: Path) -> bool:
        """
        Vérifie si un chemin doit être exclu de l'analyse.

        Args:
            path: Chemin à vérifier

        Returns:
            True si le chemin doit être exclu
        """
        path_str = str(path)
        path_parts = path.parts

        # Exclusion intelligente : seulement les dossiers système et cache
        for pattern in self.exclude_patterns:
            # Pattern avec wildcard (ex: ._*)
            if pattern.startswith("*") and path_str.endswith(pattern[1:]):
                return True

            # Exclusion des dossiers système uniquement (pas des fichiers Python dans ces dossiers)
            if pattern in path_parts:
                # Si c'est un dossier système, exclure
                if path.is_dir():
                    return True
                # Si c'est un fichier Python dans un dossier système, vérifier plus précisément
                elif path.is_file() and path.suffix == ".py":
                    # Ne pas exclure les fichiers Python dans .github, archive, etc.
                    if pattern in [".github", "archive", "build", "dist"]:
                        return False
                    # Exclure seulement les vrais dossiers système
                    if pattern in [
                        "__pycache__",
                        ".venv",
                        "venv",
                        ".git",
                        ".pytest_cache",
                    ]:
                        return True

        return False

    def collect_python_metrics(self) -> dict[str, Any]:
        """
        Collecte les métriques sur les fichiers Python.

        Returns:
            Dictionnaire avec les métriques Python
        """
        python_files: list[Path] = []
        total_lines = 0

        for py_file in self.project_root.rglob("*.py"):
            if not self._is_excluded(py_file):
                python_files.append(py_file)
                try:
                    with open(py_file, encoding="utf-8") as f:
                        lines = len(f.readlines())
                        total_lines += lines
                except (UnicodeDecodeError, OSError):
                    # Ignorer les fichiers qui ne peuvent pas être lus
                    continue

        # Séparation par type de fichier
        test_files = [f for f in python_files if self._is_test_file(f)]
        core_files = [f for f in python_files if not self._is_test_file(f)]

        return {
            "count": len(python_files),
            "core_files": len(core_files),
            "test_files": len(test_files),
            "total_lines": total_lines,
            "files_list": [str(f.relative_to(self.project_root)) for f in python_files],
        }

    def _is_test_file(self, path: Path) -> bool:
        """
        Détermine si un fichier est un fichier de test.

        Args:
            path: Chemin du fichier

        Returns:
            True si c'est un fichier de test
        """
        name = path.name

        # Vérifier si le fichier est dans un dossier de tests
        if "tests" in path.parts:
            return True

        # Vérifier le nom du fichier
        return (
            name.startswith("test_")
            or name.endswith("_test.py")
            or "test" in name.lower()
            or "conftest.py" in name
        )

    def collect_test_metrics(self) -> dict[str, Any]:
        """
        Collecte les métriques sur les tests.

        Returns:
            Dictionnaire avec les métriques de tests
        """
        test_files = []
        test_directories = set()

        # Collecter les fichiers de test
        for py_file in self.project_root.rglob("*.py"):
            if not self._is_excluded(py_file) and self._is_test_file(py_file):
                test_files.append(py_file)
                test_directories.add(py_file.parent)

        # Essayer de collecter les tests avec pytest
        collected_tests = self._collect_pytest_tests()

        # Essayer de récupérer le coverage depuis coverage.xml
        coverage_data = CoverageParser.get_coverage_for_project(self.project_root)
        coverage_percentage = None
        if coverage_data and coverage_data.get("coverage_percentage") is not None:
            coverage_percentage = coverage_data["coverage_percentage"]

        result = {
            "test_files_count": len(test_files),
            "test_directories_count": len(test_directories),
            "collected_tests_count": collected_tests,
            "test_files_list": [
                str(f.relative_to(self.project_root)) for f in test_files
            ],
        }

        # Ajouter le coverage si disponible
        if coverage_percentage is not None:
            result["coverage_percentage"] = coverage_percentage
            if coverage_data:
                result["coverage_details"] = {
                    "lines_covered": coverage_data.get("lines_covered"),
                    "lines_valid": coverage_data.get("lines_valid"),
                    "branch_coverage": coverage_data.get("branch_coverage"),
                }

        return result

    def _collect_pytest_tests(self) -> int:
        """
        Collecte le nombre de tests via pytest ou par comptage de fichiers.

        Returns:
            Nombre de tests collectés
        """
        try:
            # Changer vers le répertoire du projet
            original_cwd = Path.cwd()
            try:
                import os

                os.chdir(self.project_root)

                # Utiliser pytest pour collecter les tests
                result = subprocess.run(  # nosec B603
                    [sys.executable, "-m", "pytest", "--collect-only", "-q"],
                    capture_output=True,
                    text=True,
                    timeout=60,
                )

                if result.returncode == 0:
                    # Compter les lignes qui contiennent "test"
                    lines = result.stdout.split("\n")
                    test_count = sum(1 for line in lines if "test" in line.lower())
                    # Retourner le nombre de tests collectés par pytest
                    return test_count
                else:
                    # En cas d'échec, compter les fichiers de test manuellement
                    return self._count_test_files_manually()

            finally:
                os.chdir(original_cwd)

        except Exception:
            # En cas d'erreur, compter les fichiers de test manuellement
            return self._count_test_files_manually()

    def _count_test_files_manually(self) -> int:
        """
        Compte manuellement les fichiers de test.

        Returns:
            Nombre de fichiers de test
        """
        test_files = []

        # Méthode optimale : rglob + nom contenant "test"
        for test_file in self.project_root.rglob("*.py"):
            if not self._is_excluded(test_file):
                # Vérifier si le nom du fichier contient "test"
                if "test" in test_file.name.lower():
                    test_files.append(test_file)

        return len(test_files)

    def collect_documentation_metrics(self) -> dict[str, Any]:
        """
        Collecte les métriques sur la documentation.

        Returns:
            Dictionnaire avec les métriques de documentation
        """
        doc_files = []
        doc_extensions = {".md", ".rst", ".txt", ".html", ".pdf"}

        for doc_file in self.project_root.rglob("*"):
            if not self._is_excluded(doc_file) and doc_file.suffix in doc_extensions:
                doc_files.append(doc_file)

        return {
            "documentation_files": len(doc_files),
            "documentation_list": [
                str(f.relative_to(self.project_root)) for f in doc_files
            ],
        }

    def collect_all_metrics(self) -> dict[str, Any]:
        """
        Collecte toutes les métriques du projet.

        Returns:
            Dictionnaire complet avec toutes les métriques
        """
        collection_info = {
            "collector_version": "1.0.0",
            "python_version": (
                f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            ),
            "collection_date": datetime.now().isoformat(),
        }

        python_metrics = self.collect_python_metrics()
        test_metrics = self.collect_test_metrics()
        doc_metrics = self.collect_documentation_metrics()

        # Créer un résumé
        summary = {
            "total_python_files": python_metrics["count"],
            "lines_of_code": python_metrics["total_lines"],
            "collected_tests": test_metrics["collected_tests_count"],
            "documentation_files": doc_metrics["documentation_files"],
        }

        self.metrics_data = {
            "timestamp": datetime.now().isoformat(),
            "project_root": str(self.project_root),
            "collection_info": collection_info,
            "python_files": python_metrics,
            "test_metrics": test_metrics,
            "documentation_metrics": doc_metrics,
            "summary": summary,
        }

        return self.metrics_data
