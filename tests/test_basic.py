#!/usr/bin/env python3
"""
Tests de base pour Arkalia Metrics Collector.
"""

import sys
from pathlib import Path

# Ajouter le chemin du projet pour les imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.arkalia_metrics_collector import (
    MetricsCollector,
    MetricsExporter,
    MetricsValidator,
)


def test_imports():
    """Test que les modules peuvent être importés."""
    assert MetricsCollector is not None
    assert MetricsExporter is not None
    assert MetricsValidator is not None
    print("✅ Imports réussis")


def test_collector_initialization():
    """Test l'initialisation du collecteur."""
    collector = MetricsCollector(".")
    assert collector.project_root is not None
    assert len(collector.exclude_patterns) > 0
    print("✅ Collecteur initialisé")


def test_exporter_initialization():
    """Test l'initialisation de l'exporteur."""
    test_data = {"test": "data"}
    exporter = MetricsExporter(test_data)
    assert exporter.metrics_data == test_data
    print("✅ Exporteur initialisé")


def test_validator_initialization():
    """Test l'initialisation du validateur."""
    validator = MetricsValidator()
    assert validator.validation_errors == []
    assert validator.validation_warnings == []
    print("✅ Validateur initialisé")


def test_basic_metrics_collection():
    """Test la collecte basique de métriques."""
    collector = MetricsCollector(".")
    metrics = collector.collect_all_metrics()

    # Vérifier la structure de base
    assert "timestamp" in metrics
    assert "project_root" in metrics
    assert "collection_info" in metrics
    assert "python_files" in metrics
    assert "test_metrics" in metrics
    assert "documentation_metrics" in metrics
    assert "summary" in metrics

    print("✅ Collecte de métriques réussie")


if __name__ == "__main__":
    print("🧪 Tests de base pour Arkalia Metrics Collector")
    print("=" * 50)

    try:
        test_imports()
        test_collector_initialization()
        test_exporter_initialization()
        test_validator_initialization()
        test_basic_metrics_collection()

        print("=" * 50)
        print("🎉 Tous les tests de base ont réussi !")

    except Exception as e:
        print(f"❌ Test échoué: {e}")
        sys.exit(1)
