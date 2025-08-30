#!/usr/bin/env python3
"""
Arkalia Metrics Collector
=========================

Collecteur de métriques universel et professionnel pour projets Python.
Exclut automatiquement les venv, cache, et génère des rapports fiables.

Ce package fournit des outils pour collecter, analyser et exporter
des métriques de qualité sur vos projets Python.

Usage:
    from arkalia_metrics_collector import MetricsCollector

    collector = MetricsCollector(".")
    metrics = collector.collect_all_metrics()
    print(f"Python files: {metrics['python_files']['count']}")

Classes principales:
    - MetricsCollector: Collecte des métriques du projet
    - MetricsExporter: Export des métriques en différents formats
    - MetricsValidator: Validation des métriques collectées
"""

__version__ = "1.0.0"
__author__ = "Arkalia Luna System"
__email__ = "contact@arkalia-luna.com"
__license__ = "MIT"

from .collectors.metrics_collector import MetricsCollector
from .exporters.metrics_exporter import MetricsExporter
from .validators.metrics_validator import MetricsValidator


__all__ = [
    "MetricsCollector",
    "MetricsExporter",
    "MetricsValidator",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
]
