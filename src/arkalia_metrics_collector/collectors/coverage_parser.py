#!/usr/bin/env python3
"""
Parser pour les fichiers coverage.xml (format Cobertura).

Extrait les métriques de coverage depuis les fichiers XML générés par coverage.py.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


class CoverageParser:
    """
    Parser pour les fichiers coverage.xml.

    Supporte le format Cobertura XML généré par coverage.py.
    """

    @staticmethod
    def parse_coverage_xml(coverage_path: str | Path) -> dict[str, Any] | None:
        """
        Parse un fichier coverage.xml et extrait les métriques.

        Args:
            coverage_path: Chemin vers le fichier coverage.xml

        Returns:
            Dictionnaire avec les métriques de coverage ou None si erreur
        """
        coverage_file = Path(coverage_path)

        if not coverage_file.exists():
            return None

        try:
            tree = ET.parse(coverage_file)
            root = tree.getroot()

            # Extraire les métriques depuis l'élément racine <coverage>
            line_rate = root.get("line-rate")
            branch_rate = root.get("branch-rate")
            lines_covered = root.get("lines-covered")
            lines_valid = root.get("lines-valid")
            branches_covered = root.get("branches-covered")
            branches_valid = root.get("branches-valid")

            # Convertir en float/int
            coverage_percentage = None
            if line_rate is not None:
                try:
                    coverage_percentage = float(line_rate) * 100
                except (ValueError, TypeError):
                    pass

            branch_coverage = None
            if branch_rate is not None:
                try:
                    branch_coverage = float(branch_rate) * 100
                except (ValueError, TypeError):
                    pass

            return {
                "coverage_percentage": (
                    round(coverage_percentage, 2) if coverage_percentage else None
                ),
                "branch_coverage": (
                    round(branch_coverage, 2) if branch_coverage else None
                ),
                "lines_covered": int(lines_covered) if lines_covered else None,
                "lines_valid": int(lines_valid) if lines_valid else None,
                "branches_covered": int(branches_covered) if branches_covered else None,
                "branches_valid": int(branches_valid) if branches_valid else None,
                "coverage_file": str(coverage_file),
            }

        except (ET.ParseError, ValueError, TypeError):
            # Erreur de parsing XML
            return None

    @staticmethod
    def find_coverage_file(project_root: str | Path) -> Path | None:
        """
        Cherche un fichier coverage.xml dans le projet.

        Cherche dans l'ordre :
        1. coverage.xml à la racine
        2. .coverage.xml
        3. htmlcov/coverage.xml
        4. tests/coverage.xml

        Args:
            project_root: Racine du projet

        Returns:
            Chemin vers le fichier coverage.xml ou None si non trouvé
        """
        root = Path(project_root).resolve()

        # Ordre de recherche
        possible_paths = [
            root / "coverage.xml",
            root / ".coverage.xml",
            root / "htmlcov" / "coverage.xml",
            root / "tests" / "coverage.xml",
            root / ".coverage",
        ]

        for path in possible_paths:
            if path.exists():
                # Si c'est .coverage (fichier binaire), on ne peut pas le parser
                if path.name == ".coverage":
                    continue
                return path

        return None

    @staticmethod
    def get_coverage_for_project(project_root: str | Path) -> dict[str, Any] | None:
        """
        Récupère le coverage pour un projet en cherchant coverage.xml.

        Args:
            project_root: Racine du projet

        Returns:
            Dictionnaire avec les métriques de coverage ou None
        """
        coverage_file = CoverageParser.find_coverage_file(project_root)

        if coverage_file is None:
            return None

        return CoverageParser.parse_coverage_xml(coverage_file)
