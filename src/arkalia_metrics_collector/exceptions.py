#!/usr/bin/env python3
"""
Exceptions personnalisées pour Arkalia Metrics Collector.

Ce module définit toutes les exceptions personnalisées utilisées dans le projet
pour une meilleure gestion d'erreurs et un debugging facilité.
"""


class ArkaliaMetricsError(Exception):
    """Exception de base pour toutes les erreurs du collecteur."""

    pass


class CollectionError(ArkaliaMetricsError):
    """Erreur lors de la collecte de métriques."""

    pass


class ProjectNotFoundError(CollectionError):
    """Erreur lorsque le projet n'est pas trouvé."""

    pass


class InvalidProjectPathError(CollectionError):
    """Erreur lorsque le chemin du projet est invalide."""

    pass


class ExportError(ArkaliaMetricsError):
    """Erreur lors de l'export des métriques."""

    pass


class ValidationError(ArkaliaMetricsError):
    """Erreur lors de la validation des métriques."""

    pass


class GitHubAPIError(ArkaliaMetricsError):
    """Erreur lors de l'utilisation de l'API GitHub."""

    pass


class GitHubRateLimitError(GitHubAPIError):
    """Erreur lorsque la limite de taux GitHub est atteinte."""

    pass


class GitHubAuthenticationError(GitHubAPIError):
    """Erreur d'authentification GitHub."""

    pass


class ConfigurationError(ArkaliaMetricsError):
    """Erreur de configuration."""

    pass


class CoverageParseError(ArkaliaMetricsError):
    """Erreur lors du parsing du fichier coverage.xml."""

    pass
