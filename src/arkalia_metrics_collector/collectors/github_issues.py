#!/usr/bin/env python3
"""
Création automatique d'issues GitHub pour les alertes métriques.

Utilise l'API GitHub pour créer des issues automatiquement.
"""

import logging
import os
from typing import Any

try:
    import requests  # type: ignore[import-untyped]
except ImportError:
    requests = None

logger = logging.getLogger(__name__)


class GitHubIssues:
    """
    Créateur d'issues GitHub pour les alertes métriques.
    """

    def __init__(self, github_token: str | None = None) -> None:
        """
        Initialise le créateur d'issues GitHub.

        Args:
            github_token: Token GitHub (optionnel, peut être dans GITHUB_TOKEN env)
        """
        self.token = github_token or os.getenv("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"
        self.session = self._create_session()

    def _create_session(self) -> requests.Session | None:
        """Crée une session requests avec authentification."""
        if requests is None:
            logger.warning(
                "requests n'est pas installé. Installez-le avec: pip install requests"
            )
            return None

        if not self.token:
            logger.warning("GITHUB_TOKEN non défini. Impossible de créer des issues.")
            return None

        session = requests.Session()
        session.headers.update(
            {
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "Arkalia-Metrics-Collector",
            }
        )
        return session

    def create_issue(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str,
        labels: list[str] | None = None,
        assignees: list[str] | None = None,
    ) -> dict[str, Any] | None:
        """
        Crée une issue GitHub.

        Args:
            owner: Propriétaire du dépôt
            repo: Nom du dépôt
            title: Titre de l'issue
            body: Corps de l'issue (Markdown)
            labels: Labels à ajouter à l'issue

        Returns:
            Données de l'issue créée ou None en cas d'erreur
        """
        if self.session is None:
            logger.error("Session GitHub non disponible")
            return None

        url = f"{self.base_url}/repos/{owner}/{repo}/issues"

        payload: dict[str, Any] = {
            "title": title,
            "body": body,
        }

        if labels:
            payload["labels"] = labels

        if assignees:
            payload["assignees"] = assignees

        try:
            response = self.session.post(url, json=payload, timeout=10)

            if response.status_code == 201:
                issue_data = response.json()
                logger.info(f"Issue créée: #{issue_data.get('number')} - {title}")
                return issue_data
            elif response.status_code == 401:
                logger.error("Erreur d'authentification GitHub. Vérifiez votre token.")
                return None
            elif response.status_code == 403:
                logger.error("Permission refusée. Vérifiez les permissions du token.")
                return None
            elif response.status_code == 404:
                logger.error(f"Dépôt {owner}/{repo} non trouvé ou inaccessible.")
                return None
            else:
                logger.error(
                    f"Erreur lors de la création de l'issue: {response.status_code} - {response.text}"
                )
                return None

        except Exception as e:
            logger.error(f"Exception lors de la création de l'issue: {e}")
            return None

    def check_existing_issue(
        self, owner: str, repo: str, title_prefix: str
    ) -> dict[str, Any] | None:
        """
        Vérifie si une issue avec un titre similaire existe déjà.

        Args:
            owner: Propriétaire du dépôt
            repo: Nom du dépôt
            title_prefix: Préfixe du titre à rechercher

        Returns:
            Issue existante ou None
        """
        if self.session is None:
            return None

        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        params = {"state": "open", "per_page": 100}

        try:
            response = self.session.get(url, params=params, timeout=10)

            if response.status_code == 200:
                issues = response.json()
                for issue in issues:
                    if issue.get("title", "").startswith(title_prefix):
                        return issue

            return None

        except Exception as e:
            logger.warning(f"Erreur lors de la vérification des issues: {e}")
            return None
