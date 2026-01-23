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
    # Exemple d'utilisation (commenté pour éviter l'exécution lors de l'import)
    # print(f"Python files: {metrics['python_files']['count']}")

Classes principales:
    - MetricsCollector: Collecte des métriques du projet
    - MetricsExporter: Export des métriques en différents formats
    - MetricsValidator: Validation des métriques collectées
"""

__version__ = "1.1.1"
__author__ = "Arkalia Luna System"
__email__ = "arkalia.luna.system@gmail.com"
__license__ = "MIT"

from .collectors.github_collector import GitHubCollector
from .collectors.metrics_collector import MetricsCollector
from .collectors.multi_project_aggregator import MultiProjectAggregator
from .exceptions import (
    ArkaliaMetricsError,
    CollectionError,
    ConfigurationError,
    CoverageParseError,
    ExportError,
    GitHubAPIError,
    GitHubAuthenticationError,
    GitHubRateLimitError,
    InvalidProjectPathError,
    ProjectNotFoundError,
    ValidationError,
)
from .exporters.badges_generator import BadgesGenerator
from .exporters.external_exporters import (
    AirtableExporter,
    GoogleSheetsExporter,
    NotionExporter,
    RESTAPIExporter,
)
from .exporters.interactive_dashboard import InteractiveDashboardGenerator
from .exporters.metrics_exporter import MetricsExporter
from .notifications.notifiers import DiscordNotifier, EmailNotifier, SlackNotifier
from .validators.metrics_validator import MetricsValidator

__all__ = [
    "AirtableExporter",
    "ArkaliaMetricsError",
    "BadgesGenerator",
    "CollectionError",
    "ConfigurationError",
    "CoverageParseError",
    "DiscordNotifier",
    "EmailNotifier",
    "ExportError",
    "GitHubAPIError",
    "GitHubAuthenticationError",
    "GitHubCollector",
    "GitHubRateLimitError",
    "GoogleSheetsExporter",
    "InteractiveDashboardGenerator",
    "InvalidProjectPathError",
    "MetricsCollector",
    "MetricsExporter",
    "MetricsValidator",
    "MultiProjectAggregator",
    "NotionExporter",
    "ProjectNotFoundError",
    "RESTAPIExporter",
    "SlackNotifier",
    "ValidationError",
    "__author__",
    "__email__",
    "__license__",
    "__version__",
]
