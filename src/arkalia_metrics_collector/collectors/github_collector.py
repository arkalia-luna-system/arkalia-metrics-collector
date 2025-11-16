#!/usr/bin/env python3
"""
Arkalia Metrics Collector - Collecteur GitHub API.

Collecte des métriques depuis l'API GitHub :
- Stars, forks, watchers
- Dernière mise à jour
- Issues ouvertes/fermées
- Pull requests
- Releases
"""

import logging
import os
import re
import time
from datetime import datetime
from typing import Any

from arkalia_metrics_collector import __version__

try:
    import requests  # type: ignore[import-untyped]
except ImportError:
    requests = None

# Configuration du logger
logger = logging.getLogger(__name__)


class GitHubCollector:
    """
    Collecteur de métriques depuis l'API GitHub.

    Collecte des métriques publiques sur :
    - Stars, forks, watchers
    - Dernière mise à jour
    - Issues et pull requests
    - Releases
    """

    def __init__(
        self, github_token: str | None = None, cache_duration: int = 300
    ) -> None:
        """
        Initialise le collecteur GitHub.

        Args:
            github_token: Token GitHub (optionnel, peut être dans GITHUB_TOKEN env)
        """
        self.token = github_token or os.getenv("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"
        self.session = self._create_session()
        self.cache_duration = cache_duration
        self._cache: dict[str, tuple[float, Any]] = {}
        self._rate_limit_remaining = 5000
        self._rate_limit_reset = 0

    def _create_session(self) -> requests.Session | None:
        """
        Crée une session HTTP avec authentification si disponible.

        Returns:
            Session requests ou None si requests n'est pas installé
        """
        if requests is None:
            logger.warning(
                "Module 'requests' non disponible. Installer avec: pip install 'arkalia-metrics-collector[github]'"
            )
            return None

        session = requests.Session()
        if self.token:
            session.headers.update({"Authorization": f"token {self.token}"})
        else:
            logger.warning(
                "Aucun token GitHub fourni. Les limites de taux seront plus restrictives."
            )

        session.headers.update(
            {
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": f"Arkalia-Metrics-Collector/{__version__}",
            }
        )
        return session

    def _get_cached(self, key: str) -> Any | None:
        """Récupère une valeur du cache si elle est encore valide."""
        if key in self._cache:
            timestamp, value = self._cache[key]
            if time.time() - timestamp < self.cache_duration:
                return value
            else:
                del self._cache[key]
        return None

    def _set_cache(self, key: str, value: Any) -> None:
        """Met en cache une valeur avec timestamp."""
        self._cache[key] = (time.time(), value)

    def _make_request(self, url: str, timeout: int = 10) -> requests.Response | None:
        """
        Effectue une requête HTTP avec gestion du rate limiting.

        Args:
            url: URL à requêter
            timeout: Timeout en secondes

        Returns:
            Response ou None en cas d'erreur
        """
        if self.session is None:
            return None

        # Vérifier le cache d'abord
        cached = self._get_cached(url)
        if cached is not None:
            logger.debug(f"Cache hit pour {url}")
            return cached

        # Vérifier le rate limiting
        if self._rate_limit_remaining <= 1 and time.time() < self._rate_limit_reset:
            wait_time = self._rate_limit_reset - time.time()
            logger.warning(f"Rate limit atteint. Attente de {wait_time:.1f}s")
            time.sleep(wait_time)

        try:
            response = self.session.get(url, timeout=timeout)

            # Mettre à jour les informations de rate limiting
            self._rate_limit_remaining = int(
                response.headers.get("X-RateLimit-Remaining", 5000)
            )
            self._rate_limit_reset = int(
                response.headers.get("X-RateLimit-Reset", time.time() + 3600)
            )

            if response.status_code == 200:
                self._set_cache(url, response)
                logger.debug(f"Requête réussie: {url}")
            else:
                logger.warning(f"Erreur HTTP {response.status_code} pour {url}")

            return response

        except Exception as e:
            logger.error(f"Erreur lors de la requête {url}: {e}")
            return None

    def collect_repo_metrics(self, owner: str, repo: str) -> dict[str, Any] | None:
        """
        Collecte les métriques d'un dépôt GitHub.

        Args:
            owner: Propriétaire du dépôt (organisation ou utilisateur)
            repo: Nom du dépôt

        Returns:
            Dictionnaire avec les métriques ou None en cas d'erreur
        """
        if self.session is None:
            return None

        try:
            # Informations de base du dépôt
            repo_url = f"{self.base_url}/repos/{owner}/{repo}"
            response = self._make_request(repo_url)

            if response is None or response.status_code != 200:
                logger.error(f"Impossible de récupérer les données pour {owner}/{repo}")
                return None

            repo_data = response.json()

            # Collecter les issues
            issues_data = self._collect_issues(owner, repo)

            # Collecter les pull requests
            prs_data = self._collect_pull_requests(owner, repo)

            # Collecter les releases
            releases_data = self._collect_releases(owner, repo)

            # Formater les métriques
            metrics = {
                "repository": {
                    "full_name": repo_data.get("full_name", f"{owner}/{repo}"),
                    "name": repo_data.get("name", repo),
                    "owner": repo_data.get("owner", {}).get("login", owner),
                    "description": repo_data.get("description", ""),
                    "url": repo_data.get("html_url", ""),
                    "language": repo_data.get("language", ""),
                    "license": (
                        repo_data.get("license", {}).get("name", "")
                        if repo_data.get("license")
                        else ""
                    ),
                    "created_at": repo_data.get("created_at", ""),
                    "updated_at": repo_data.get("updated_at", ""),
                    "pushed_at": repo_data.get("pushed_at", ""),
                },
                "stats": {
                    "stars": repo_data.get("stargazers_count", 0),
                    "forks": repo_data.get("forks_count", 0),
                    "watchers": repo_data.get("watchers_count", 0),
                    "open_issues": repo_data.get("open_issues_count", 0),
                    "size": repo_data.get("size", 0),  # Taille en KB
                },
                "issues": issues_data,
                "pull_requests": prs_data,
                "releases": releases_data,
                "last_update": repo_data.get("pushed_at", ""),
                "collection_date": datetime.now().isoformat(),
            }

            return metrics

        except Exception:
            return None

    def _collect_issues(self, owner: str, repo: str) -> dict[str, Any]:
        """
        Collecte les métriques sur les issues.

        Args:
            owner: Propriétaire du dépôt
            repo: Nom du dépôt

        Returns:
            Dictionnaire avec les métriques d'issues
        """
        if self.session is None:
            return {"open": 0, "closed": 0, "total": 0}

        try:
            # Issues ouvertes
            open_url = (
                f"{self.base_url}/repos/{owner}/{repo}/issues?state=open&per_page=1"
            )
            open_response = self._make_request(open_url)
            open_count = 0
            if open_response is not None and open_response.status_code == 200:
                # Utiliser le header Link pour obtenir le total
                link_header = open_response.headers.get("Link", "")
                if link_header:
                    # Parser le header Link pour obtenir le total
                    # Format: <url>; rel="last", on extrait le numéro de page
                    try:
                        last_link = [
                            link
                            for link in link_header.split(",")
                            if 'rel="last"' in link
                        ]
                        if last_link:
                            # Extraire le numéro de page depuis l'URL
                            match = re.search(r"page=(\d+)", last_link[0])
                            if match:
                                # Calculer le total approximatif basé sur la pagination
                                last_page = int(match.group(1))
                                # Faire une requête à la dernière page pour obtenir le nombre exact
                                last_page_url = f"{self.base_url}/repos/{owner}/{repo}/issues?state=open&per_page=100&page={last_page}"
                                last_page_response = self._make_request(last_page_url)
                                if (
                                    last_page_response
                                    and last_page_response.status_code == 200
                                ):
                                    last_page_issues = [
                                        i
                                        for i in last_page_response.json()
                                        if "pull_request" not in i
                                    ]
                                    # Total = (pages complètes - 1) * 100 + issues de la dernière page
                                    open_count = (last_page - 1) * 100 + len(
                                        last_page_issues
                                    )
                    except Exception:  # nosec B110
                        pass
                else:
                    # Pas de pagination, compter directement
                    open_issues = [
                        i for i in open_response.json() if "pull_request" not in i
                    ]
                    open_count = len(open_issues)

            # Issues fermées (estimation via l'API search)
            closed_count = 0
            try:
                search_url = f"{self.base_url}/search/issues?q=repo:{owner}/{repo}+type:issue+state:closed"
                search_response = self._make_request(search_url)
                if search_response and search_response.status_code == 200:
                    closed_count = search_response.json().get("total_count", 0)
            except Exception:  # nosec B110
                pass

            return {
                "open": open_count,
                "closed": closed_count,
                "total": open_count + closed_count,
            }

        except Exception:
            return {"open": 0, "closed": 0, "total": 0}

    def _collect_pull_requests(self, owner: str, repo: str) -> dict[str, Any]:
        """
        Collecte les métriques sur les pull requests.

        Args:
            owner: Propriétaire du dépôt
            repo: Nom du dépôt

        Returns:
            Dictionnaire avec les métriques de PRs
        """
        if self.session is None:
            return {"open": 0, "closed": 0, "merged": 0, "total": 0}

        try:
            # PRs ouvertes
            open_url = (
                f"{self.base_url}/repos/{owner}/{repo}/pulls?state=open&per_page=1"
            )
            open_response = self._make_request(open_url)
            open_count = 0
            if open_response is not None and open_response.status_code == 200:
                link_header = open_response.headers.get("Link", "")
                if link_header:
                    try:
                        last_link = [
                            link
                            for link in link_header.split(",")
                            if 'rel="last"' in link
                        ]
                        if last_link:
                            match = re.search(r"page=(\d+)", last_link[0])
                            if match:
                                last_page = int(match.group(1))
                                last_page_url = f"{self.base_url}/repos/{owner}/{repo}/pulls?state=open&per_page=100&page={last_page}"
                                last_page_response = self._make_request(last_page_url)
                                if (
                                    last_page_response
                                    and last_page_response.status_code == 200
                                ):
                                    last_page_prs = last_page_response.json()
                                    # Total = (pages complètes - 1) * 100 + PRs de la dernière page
                                    open_count = (last_page - 1) * 100 + len(
                                        last_page_prs
                                    )
                    except Exception:  # nosec B110
                        pass
                else:
                    open_count = len(open_response.json())

            # PRs fermées/mergées (estimation)
            closed_count = 0
            merged_count = 0
            try:
                search_url = f"{self.base_url}/search/issues?q=repo:{owner}/{repo}+type:pr+state:closed"
                search_response = self._make_request(search_url)
                if search_response and search_response.status_code == 200:
                    closed_count = search_response.json().get("total_count", 0)
                    # Estimation: 80% des PRs fermées sont mergées
                    merged_count = int(closed_count * 0.8)
            except Exception:  # nosec B110
                pass

            return {
                "open": open_count,
                "closed": closed_count,
                "merged": merged_count,
                "total": open_count + closed_count,
            }

        except Exception:
            return {"open": 0, "closed": 0, "merged": 0, "total": 0}

    def _collect_releases(self, owner: str, repo: str) -> dict[str, Any]:
        """
        Collecte les métriques sur les releases.

        Args:
            owner: Propriétaire du dépôt
            repo: Nom du dépôt

        Returns:
            Dictionnaire avec les métriques de releases
        """
        if self.session is None:
            return {"total": 0, "latest": None}

        try:
            releases_url = f"{self.base_url}/repos/{owner}/{repo}/releases?per_page=1"
            response = self._make_request(releases_url)

            if response and response.status_code == 200:
                releases = response.json()
                total = len(releases) if isinstance(releases, list) else 0
                latest = (
                    releases[0] if releases and isinstance(releases, list) else None
                )

                return {
                    "total": total,
                    "latest": (
                        {
                            "tag_name": latest.get("tag_name", "") if latest else "",
                            "published_at": (
                                latest.get("published_at", "") if latest else ""
                            ),
                            "name": latest.get("name", "") if latest else "",
                        }
                        if latest
                        else None
                    ),
                }

        except Exception:  # nosec B110
            pass

        return {"total": 0, "latest": None}

    def collect_multiple_repos(self, repos: list[dict[str, str]]) -> dict[str, Any]:
        """
        Collecte les métriques de plusieurs dépôts.

        Args:
            repos: Liste de dictionnaires avec 'owner' et 'repo'

        Returns:
            Dictionnaire avec les métriques agrégées
        """
        all_metrics = {}
        total_stars = 0
        total_forks = 0
        total_watchers = 0

        for repo_info in repos:
            owner = repo_info.get("owner", "")
            repo = repo_info.get("repo", "")
            if not owner or not repo:
                continue

            metrics = self.collect_repo_metrics(owner, repo)
            if metrics:
                all_metrics[f"{owner}/{repo}"] = metrics
                total_stars += metrics.get("stats", {}).get("stars", 0)
                total_forks += metrics.get("stats", {}).get("forks", 0)
                total_watchers += metrics.get("stats", {}).get("watchers", 0)

        return {
            "repositories": all_metrics,
            "aggregated": {
                "total_repos": len(all_metrics),
                "total_stars": total_stars,
                "total_forks": total_forks,
                "total_watchers": total_watchers,
            },
            "collection_date": datetime.now().isoformat(),
        }
