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

__version__ = "1.1.0"
__author__ = "Arkalia Luna System"
__email__ = "arkalia.luna.system@gmail.com"
__license__ = "MIT"

from .collectors.github_collector import GitHubCollector
from .collectors.metrics_collector import MetricsCollector
from .collectors.multi_project_aggregator import MultiProjectAggregator
from .exporters.badges_generator import BadgesGenerator
from .exporters.metrics_exporter import MetricsExporter
from .exporters.external_exporters import (
    AirtableExporter,
    GoogleSheetsExporter,
    NotionExporter,
    RESTAPIExporter,
)
from .notifications.notifiers import DiscordNotifier, EmailNotifier, SlackNotifier
from .validators.metrics_validator import MetricsValidator

__all__ = [
    "MetricsCollector",
    "GitHubCollector",
    "MultiProjectAggregator",
    "MetricsExporter",
    "BadgesGenerator",
    "MetricsValidator",
    "EmailNotifier",
    "SlackNotifier",
    "DiscordNotifier",
    "RESTAPIExporter",
    "GoogleSheetsExporter",
    "NotionExporter",
    "AirtableExporter",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
]
