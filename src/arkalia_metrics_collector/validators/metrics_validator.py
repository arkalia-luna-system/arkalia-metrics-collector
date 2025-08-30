#!/usr/bin/env python3
"""
Arkalia Metrics Validator - Validation des métriques collectées.

Module de validation des métriques pour s'assurer de leur cohérence
et de leur qualité.
"""

from typing import Any


class MetricsValidator:
    """
    Validateur de métriques pour Arkalia Metrics Collector.

    Valide la cohérence et la qualité des métriques collectées.
    """

    def __init__(self) -> None:
        """Initialise le validateur de métriques."""
        self.validation_errors: list[str] = []
        self.validation_warnings: list[str] = []

    def validate_metrics(
        self, metrics_data: dict[str, Any]
    ) -> tuple[bool, list[str], list[str]]:
        """
        Valide les métriques collectées.

        Args:
            metrics_data: Données des métriques à valider

        Returns:
            Tuple (is_valid, errors, warnings)
        """
        self.validation_errors = []
        self.validation_warnings = []

        # Validation de base
        self._validate_structure(metrics_data)
        self._validate_python_metrics(metrics_data)
        self._validate_test_metrics(metrics_data)
        self._validate_documentation_metrics(metrics_data)
        self._validate_summary_consistency(metrics_data)

        is_valid = len(self.validation_errors) == 0

        return is_valid, self.validation_errors, self.validation_warnings

    def _validate_structure(self, metrics_data: dict[str, Any]) -> None:
        """
        Valide la structure générale des métriques.

        Args:
            metrics_data: Données des métriques
        """
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
            if key not in metrics_data:
                self.validation_errors.append(f"Clé manquante: {key}")

        if "collection_info" in metrics_data:
            required_info_keys = [
                "collector_version",
                "python_version",
                "collection_date",
            ]
            for key in required_info_keys:
                if key not in metrics_data["collection_info"]:
                    self.validation_warnings.append(
                        f"Info de collection manquante: {key}"
                    )

    def _validate_python_metrics(self, metrics_data: dict[str, Any]) -> None:
        """
        Valide les métriques Python.

        Args:
            metrics_data: Données des métriques
        """
        python_metrics = metrics_data.get("python_files", {})

        if "count" not in python_metrics:
            self.validation_errors.append("Nombre de fichiers Python manquant")
            return

        count = python_metrics["count"]
        core_files = python_metrics.get("core_files", 0)
        test_files = python_metrics.get("test_files", 0)
        total_lines = python_metrics.get("total_lines", 0)

        # Validation de cohérence
        if core_files + test_files != count:
            self.validation_errors.append(
                f"Incohérence dans le comptage des fichiers: {core_files} + {test_files} != {count}"
            )

        if count > 0 and total_lines == 0:
            self.validation_warnings.append(
                "Fichiers Python détectés mais 0 lignes de code"
            )

        if count == 0:
            self.validation_warnings.append("Aucun fichier Python détecté")

    def _validate_test_metrics(self, metrics_data: dict[str, Any]) -> None:
        """
        Valide les métriques de tests.

        Args:
            metrics_data: Données des métriques
        """
        test_metrics = metrics_data.get("test_metrics", {})
        python_metrics = metrics_data.get("python_files", {})

        test_files_count = test_metrics.get("test_files_count", 0)
        python_test_files = python_metrics.get("test_files", 0)

        if test_files_count != python_test_files:
            self.validation_errors.append(
                f"Incohérence dans le comptage des tests: {test_files_count} != {python_test_files}"
            )

        collected_tests = test_metrics.get("collected_tests_count", 0)
        if collected_tests < 0:
            self.validation_errors.append(f"Nombre de tests négatif: {collected_tests}")

    def _validate_documentation_metrics(self, metrics_data: dict[str, Any]) -> None:
        """
        Valide les métriques de documentation.

        Args:
            metrics_data: Données des métriques
        """
        doc_metrics = metrics_data.get("documentation_metrics", {})
        doc_files = doc_metrics.get("documentation_files", 0)

        if doc_files < 0:
            self.validation_errors.append(
                f"Nombre de fichiers de documentation négatif: {doc_files}"
            )

        if doc_files == 0:
            self.validation_warnings.append("Aucun fichier de documentation détecté")

    def _validate_summary_consistency(self, metrics_data: dict[str, Any]) -> None:
        """
        Valide la cohérence du résumé.

        Args:
            metrics_data: Données des métriques
        """
        summary = metrics_data.get("summary", {})
        python_metrics = metrics_data.get("python_files", {})
        test_metrics = metrics_data.get("test_metrics", {})
        doc_metrics = metrics_data.get("documentation_metrics", {})

        # Vérifier la cohérence du résumé
        expected_total_files = summary.get("total_python_files", 0)
        actual_total_files = python_metrics.get("count", 0)

        if expected_total_files != actual_total_files:
            self.validation_errors.append(
                f"Incohérence dans le résumé: total_python_files {expected_total_files} != {actual_total_files}"
            )

        expected_lines = summary.get("lines_of_code", 0)
        actual_lines = python_metrics.get("total_lines", 0)

        if expected_lines != actual_lines:
            self.validation_errors.append(
                f"Incohérence dans le résumé: lines_of_code {expected_lines} != {actual_lines}"
            )

        expected_tests = summary.get("collected_tests", 0)
        actual_tests = test_metrics.get("collected_tests_count", 0)

        if expected_tests != actual_tests:
            self.validation_errors.append(
                f"Incohérence dans le résumé: collected_tests {expected_tests} != {actual_tests}"
            )

        expected_docs = summary.get("documentation_files", 0)
        actual_docs = doc_metrics.get("documentation_files", 0)

        if expected_docs != actual_docs:
            self.validation_errors.append(
                f"Incohérence dans le résumé: documentation_files {expected_docs} != {actual_docs}"
            )

    def get_validation_report(self) -> dict[str, Any]:
        """
        Génère un rapport de validation.

        Returns:
            Dictionnaire avec le rapport de validation
        """
        return {
            "is_valid": len(self.validation_errors) == 0,
            "errors_count": len(self.validation_errors),
            "warnings_count": len(self.validation_warnings),
            "errors": self.validation_errors,
            "warnings": self.validation_warnings,
            "validation_summary": {
                "status": (
                    "✅ VALID" if len(self.validation_errors) == 0 else "❌ INVALID"
                ),
                "score": max(
                    0,
                    100
                    - len(self.validation_errors) * 10
                    - len(self.validation_warnings) * 2,
                ),
            },
        }
