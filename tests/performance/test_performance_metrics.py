#!/usr/bin/env python3
"""
Tests de performance pour le collecteur de métriques.

Valide les performances sur des projets de différentes tailles
et mesure les temps d'exécution critiques.
"""

import time
from pathlib import Path

import pytest

from arkalia_metrics_collector import (
    MetricsCollector,
    MetricsExporter,
    MetricsValidator,
)


class TestPerformanceMetrics:
    """Tests de performance du collecteur de métriques."""

    @pytest.fixture
    def small_project(self, tmp_path: Path) -> Path:
        """Projet de petite taille (10-50 fichiers)."""
        project = tmp_path / "small_project"
        project.mkdir()

        # Structure simple
        src_dir = project / "src" / "package"
        src_dir.mkdir(parents=True)
        tests_dir = project / "tests"
        tests_dir.mkdir()

        # 10 fichiers source
        for i in range(10):
            (src_dir / f"module_{i}.py").write_text(f'''"""Module {i}."""
def function_{i}():
    """Fonction {i}."""
    return {i}
''')

        # 5 fichiers de test
        for i in range(5):
            (tests_dir / f"test_module_{i}.py").write_text(f'''"""Tests module {i}."""
import pytest
from package.module_{i} import function_{i}

def test_function_{i}():
    """Test fonction {i}."""
    assert function_{i}() == {i}
''')

        return project

    @pytest.fixture
    def medium_project(self, tmp_path: Path) -> Path:
        """Projet de taille moyenne (100-500 fichiers)."""
        project = tmp_path / "medium_project"
        project.mkdir()

        # Structure modulaire
        for module in ["core", "api", "database", "auth", "utils"]:
            module_dir = project / "src" / "package" / module
            module_dir.mkdir(parents=True)

            # 20 fichiers par module
            for i in range(20):
                (module_dir / f"{module}_{i}.py").write_text(
                    f'''"""Module {module}_{i}."""
class {module.title()}{i}:
    """Classe {module.title()}{i}."""

    def __init__(self):
        self.value = {i}

    def process(self, data):
        """Traite les données."""
        return data * {i}
'''
                )

        # Tests correspondants
        tests_dir = project / "tests"
        for module in ["core", "api", "database", "auth", "utils"]:
            test_module_dir = tests_dir / module
            test_module_dir.mkdir(parents=True)

            for i in range(20):
                (test_module_dir / f"test_{module}_{i}.py").write_text(
                    f'''"""Tests {module}_{i}."""
import pytest
from package.{module}.{module}_{i} import {module.title()}{i}

def test_{module}_{i}_init():
    """Test initialisation."""
    obj = {module.title()}{i}()
    assert obj.value == {i}

def test_{module}_{i}_process():
    """Test process."""
    obj = {module.title()}{i}()
    assert obj.process(2) == 2 * {i}
'''
                )

        return project

    @pytest.fixture
    def large_project(self, tmp_path: Path) -> Path:
        """Projet de grande taille (1000+ fichiers)."""
        project = tmp_path / "large_project"
        project.mkdir()

        # Structure complexe avec sous-modules
        for main_module in ["frontend", "backend", "shared", "tools"]:
            main_dir = project / "src" / main_module
            main_dir.mkdir(parents=True)

            # 10 sous-modules par module principal
            for sub_module in range(10):
                sub_dir = main_dir / f"sub_{sub_module}"
                sub_dir.mkdir()

                # 25 fichiers par sous-module
                for file_num in range(25):
                    (sub_dir / f"file_{file_num}.py").write_text(
                        f'''"""Fichier {file_num} du sous-module {sub_module}."""
def process_{file_num}(data):
    """Traite les données."""
    return data + {file_num}

class Handler_{file_num}:
    """Gestionnaire {file_num}."""

    def handle(self, request):
        """Gère une requête."""
        return process_{file_num}(request)
'''
                    )

        # Tests correspondants (moins nombreux)
        tests_dir = project / "tests"
        for main_module in ["frontend", "backend", "shared", "tools"]:
            test_main_dir = tests_dir / main_module
            test_main_dir.mkdir(parents=True)

            for sub_module in range(10):
                test_sub_dir = test_main_dir / f"sub_{sub_module}"
                test_sub_dir.mkdir()

                # 5 fichiers de test par sous-module
                for file_num in range(5):
                    (test_sub_dir / f"test_file_{file_num}.py").write_text(
                        f'''"""Tests fichier {file_num}."""
import pytest
from {main_module}.sub_{sub_module}.file_{file_num} import process_{file_num}, Handler_{file_num}

def test_process_{file_num}():
    """Test process_{file_num}."""
    assert process_{file_num}(10) == 10 + {file_num}

def test_handler_{file_num}():
    """Test Handler_{file_num}."""
    handler = Handler_{file_num}()
    assert handler.handle(5) == 5 + {file_num}
'''
                    )

        return project

    def test_small_project_performance(self, small_project: Path):
        """Test de performance sur petit projet."""
        collector = MetricsCollector(str(small_project))

        # Mesurer le temps de collecte
        start_time = time.time()
        metrics = collector.collect_all_metrics()
        end_time = time.time()

        collection_time = end_time - start_time

        # Petit projet : < 1 seconde
        assert collection_time < 1.0

        # Vérifier les métriques
        assert metrics["python_files"]["count"] >= 15  # 10 + 5
        assert metrics["test_metrics"]["collected_tests_count"] >= 5

    def test_medium_project_performance(self, medium_project: Path):
        """Test de performance sur projet moyen."""
        collector = MetricsCollector(str(medium_project))

        # Mesurer le temps de collecte
        start_time = time.time()
        metrics = collector.collect_all_metrics()
        end_time = time.time()

        collection_time = end_time - start_time

        # Projet moyen : < 3 secondes
        assert collection_time < 3.0

        # Vérifier les métriques
        assert metrics["python_files"]["count"] >= 100  # 5 * 20
        assert metrics["test_metrics"]["collected_tests_count"] >= 100  # 5 * 20

    def test_large_project_performance(self, large_project: Path):
        """Test de performance sur grand projet."""
        collector = MetricsCollector(str(large_project))

        # Mesurer le temps de collecte
        start_time = time.time()
        metrics = collector.collect_all_metrics()
        end_time = time.time()

        collection_time = end_time - start_time

        # Grand projet : < 10 secondes
        assert collection_time < 10.0

        # Vérifier les métriques
        assert metrics["python_files"]["count"] >= 1000  # 4 * 10 * 25
        assert metrics["test_metrics"]["collected_tests_count"] >= 200  # 4 * 10 * 5

    def test_export_performance_small(self, small_project: Path, tmp_path: Path):
        """Test de performance d'export sur petit projet."""
        collector = MetricsCollector(str(small_project))
        metrics = collector.collect_all_metrics()

        exporter = MetricsExporter(metrics)
        output_dir = tmp_path / "export_perf"
        output_dir.mkdir()

        # Mesurer le temps d'export
        start_time = time.time()

        exporter.export_json(str(output_dir / "metrics.json"))
        exporter.export_markdown_summary(str(output_dir / "metrics.md"))
        exporter.export_html_dashboard(str(output_dir / "dashboard.html"))
        exporter.export_csv(str(output_dir / "metrics.csv"))

        end_time = time.time()
        export_time = end_time - start_time

        # Export doit être rapide : < 2 secondes
        assert export_time < 2.0

    def test_export_performance_large(self, large_project: Path, tmp_path: Path):
        """Test de performance d'export sur grand projet."""
        collector = MetricsCollector(str(large_project))
        metrics = collector.collect_all_metrics()

        exporter = MetricsExporter(metrics)
        output_dir = tmp_path / "export_perf_large"
        output_dir.mkdir()

        # Mesurer le temps d'export
        start_time = time.time()

        exporter.export_json(str(output_dir / "metrics.json"))
        exporter.export_markdown_summary(str(output_dir / "metrics.md"))
        exporter.export_html_dashboard(str(output_dir / "dashboard.html"))
        exporter.export_csv(str(output_dir / "metrics.csv"))

        end_time = time.time()
        export_time = end_time - start_time

        # Export grand projet : < 5 secondes
        assert export_time < 5.0

    def test_validation_performance(self, large_project: Path):
        """Test de performance de validation."""
        collector = MetricsCollector(str(large_project))
        metrics = collector.collect_all_metrics()

        validator = MetricsValidator()

        # Mesurer le temps de validation
        start_time = time.time()
        is_valid, errors, warnings = validator.validate_metrics(metrics)
        end_time = time.time()

        validation_time = end_time - start_time

        # Validation doit être rapide : < 1 seconde
        assert validation_time < 1.0
        assert is_valid is True

    def test_memory_usage_small(self, small_project: Path):
        """Test d'utilisation mémoire sur petit projet."""
        import os

        import psutil

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        collector = MetricsCollector(str(small_project))
        metrics = collector.collect_all_metrics()

        final_memory = process.memory_info().rss
        memory_used = final_memory - initial_memory

        # Utilisation mémoire raisonnable : < 50 MB
        assert memory_used < 50 * 1024 * 1024  # 50 MB

        # Vérifier que les métriques sont complètes
        assert metrics["python_files"]["count"] > 0

    def test_memory_usage_large(self, large_project: Path):
        """Test d'utilisation mémoire sur grand projet."""
        import os

        import psutil

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        collector = MetricsCollector(str(large_project))
        metrics = collector.collect_all_metrics()

        final_memory = process.memory_info().rss
        memory_used = final_memory - initial_memory

        # Utilisation mémoire acceptable : < 200 MB
        assert memory_used < 200 * 1024 * 1024  # 200 MB

        # Vérifier que les métriques sont complètes
        assert metrics["python_files"]["count"] > 0

    def test_concurrent_collection(self, small_project: Path):
        """Test de collecte concurrente."""
        import queue
        import threading

        results = queue.Queue()

        def collect_metrics():
            """Collecte les métriques dans un thread."""
            try:
                collector = MetricsCollector(str(small_project))
                metrics = collector.collect_all_metrics()
                results.put(("success", metrics))
            except Exception as e:
                results.put(("error", str(e)))

        # Lancer plusieurs collectes en parallèle
        threads = []
        for _ in range(3):
            thread = threading.Thread(target=collect_metrics)
            threads.append(thread)
            thread.start()

        # Attendre la fin de tous les threads
        for thread in threads:
            thread.join()

        # Vérifier que toutes les collectes ont réussi
        success_count = 0
        while not results.empty():
            status, data = results.get()
            if status == "success":
                success_count += 1
                assert data["python_files"]["count"] > 0

        assert success_count == 3

    def test_benchmark_collection_speed(
        self, small_project: Path, medium_project: Path, large_project: Path
    ):
        """Benchmark de vitesse de collecte."""
        projects = [
            ("small", small_project),
            ("medium", medium_project),
            ("large", large_project),
        ]

        results = {}

        for name, project in projects:
            collector = MetricsCollector(str(project))

            # Mesurer plusieurs fois pour avoir une moyenne
            times = []
            for _ in range(3):
                start_time = time.time()
                metrics = collector.collect_all_metrics()
                end_time = time.time()
                times.append(end_time - start_time)

            avg_time = sum(times) / len(times)
            results[name] = {
                "avg_time": avg_time,
                "files_count": metrics["python_files"]["count"],
                "tests_count": metrics["test_metrics"]["collected_tests_count"],
            }

        # Vérifier que les temps sont cohérents avec la taille
        assert results["small"]["avg_time"] < results["medium"]["avg_time"]
        assert results["medium"]["avg_time"] < results["large"]["avg_time"]

        # Vérifier que le nombre de fichiers est cohérent
        assert results["small"]["files_count"] < results["medium"]["files_count"]
        assert results["medium"]["files_count"] < results["large"]["files_count"]

    @pytest.mark.performance
    def test_stress_collection(self, tmp_path: Path):
        """Test de stress avec collecte répétée."""
        # Créer un projet de taille moyenne
        project = tmp_path / "stress_project"
        project.mkdir()

        src_dir = project / "src" / "package"
        src_dir.mkdir(parents=True)

        # 50 fichiers
        for i in range(50):
            (src_dir / f"module_{i}.py").write_text(f'''"""Module {i}."""
def function_{i}():
    return {i}
''')

        collector = MetricsCollector(str(project))

        # Collecter 10 fois de suite
        times = []
        for _ in range(10):
            start_time = time.time()
            metrics = collector.collect_all_metrics()
            end_time = time.time()
            times.append(end_time - start_time)

            # Vérifier que les métriques sont cohérentes
            assert metrics["python_files"]["count"] == 50

        # Le temps ne doit pas dégrader significativement
        first_half = times[:5]
        second_half = times[5:]

        avg_first = sum(first_half) / len(first_half)
        avg_second = sum(second_half) / len(second_half)

        # La différence ne doit pas être trop importante
        assert abs(avg_second - avg_first) < avg_first * 0.5  # Max 50% de différence
