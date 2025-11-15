#!/usr/bin/env python3
"""
Arkalia Metrics Collector - Générateur de Badges.

Génère des badges automatiques pour :
- Shields.io (statut, version, coverage, etc.)
- Codecov
- GitHub Actions
- PyPI
"""

from typing import Any


class BadgesGenerator:
    """
    Générateur de badges automatiques pour README.

    Génère des badges au format Markdown pour :
    - Shields.io (statut, métriques, coverage)
    - Codecov (coverage)
    - GitHub Actions (CI/CD)
    - PyPI (version)
    """

    @staticmethod
    def generate_shields_badge(
        label: str,
        message: str,
        color: str = "blue",
        style: str = "flat",
        logo: str | None = None,
    ) -> str:
        """
        Génère un badge Shields.io.

        Args:
            label: Texte du label
            message: Texte du message
            color: Couleur du badge (blue, green, red, orange, etc.)
            style: Style du badge (flat, flat-square, plastic, etc.)
            logo: Logo à afficher (github, python, etc.)

        Returns:
            URL du badge Shields.io
        """
        base_url = "https://img.shields.io/badge"
        label_encoded = label.replace(" ", "%20").replace("-", "--")
        message_encoded = message.replace(" ", "%20").replace("-", "--")

        url = f"{base_url}/{label_encoded}-{message_encoded}-{color}?style={style}"

        if logo:
            url += f"&logo={logo}"

        return url

    @staticmethod
    def generate_codecov_badge(owner: str, repo: str, branch: str = "main") -> str:
        """
        Génère un badge Codecov.

        Args:
            owner: Propriétaire du dépôt
            repo: Nom du dépôt
            branch: Branche à suivre

        Returns:
            URL du badge Codecov
        """
        return f"https://codecov.io/gh/{owner}/{repo}/branch/{branch}/graph/badge.svg"

    @staticmethod
    def generate_github_actions_badge(
        owner: str, repo: str, workflow: str = "ci"
    ) -> str:
        """
        Génère un badge GitHub Actions.

        Args:
            owner: Propriétaire du dépôt
            repo: Nom du dépôt
            workflow: Nom du workflow

        Returns:
            URL du badge GitHub Actions
        """
        return f"https://github.com/{owner}/{repo}/actions/workflows/{workflow}.yml/badge.svg"

    @staticmethod
    def generate_pypi_badge(package_name: str) -> str:
        """
        Génère un badge PyPI.

        Args:
            package_name: Nom du package PyPI

        Returns:
            URL du badge PyPI
        """
        return f"https://img.shields.io/pypi/v/{package_name}?logo=pypi&logoColor=white"

    def generate_metrics_badges(
        self,
        metrics: dict[str, Any],
        github_owner: str | None = None,
        github_repo: str | None = None,
    ) -> str:
        """
        Génère tous les badges de métriques.

        Args:
            metrics: Dictionnaire de métriques
            github_owner: Propriétaire GitHub (optionnel)
            github_repo: Dépôt GitHub (optionnel)

        Returns:
            Bloc de badges en Markdown
        """
        badges = []

        summary = metrics.get("summary", {})
        python_files = summary.get("total_python_files", 0)
        lines_of_code = summary.get("lines_of_code", 0)
        tests = summary.get("collected_tests", 0)

        # Badge modules Python
        modules_badge = self.generate_shields_badge(
            "Python Modules",
            f"{python_files:,}",
            color="blue",
            logo="python",
        )
        badges.append(
            f"[![Modules]({modules_badge})](https://github.com/{github_owner}/{github_repo})"
            if github_owner and github_repo
            else f"![Modules]({modules_badge})"
        )

        # Badge lignes de code
        loc_badge = self.generate_shields_badge(
            "Lines of Code",
            f"{lines_of_code:,}",
            color="green",
        )
        badges.append(
            f"[![LOC]({loc_badge})](https://github.com/{github_owner}/{github_repo})"
            if github_owner and github_repo
            else f"![LOC]({loc_badge})"
        )

        # Badge tests
        tests_badge = self.generate_shields_badge(
            "Tests",
            f"{tests:,}",
            color="purple",
        )
        badges.append(
            f"[![Tests]({tests_badge})](https://github.com/{github_owner}/{github_repo})"
            if github_owner and github_repo
            else f"![Tests]({tests_badge})"
        )

        # Badge coverage si disponible
        coverage = metrics.get("coverage") or metrics.get("test_metrics", {}).get(
            "coverage_percentage"
        )
        if coverage is not None:
            try:
                coverage_float = float(coverage)
                color = (
                    "green"
                    if coverage_float >= 80
                    else "yellow" if coverage_float >= 50 else "red"
                )
                coverage_badge = self.generate_shields_badge(
                    "Coverage",
                    f"{coverage_float}%25",
                    color=color,
                )
                badges.append(
                    f"[![Coverage]({coverage_badge})](https://github.com/{github_owner}/{github_repo})"
                    if github_owner and github_repo
                    else f"![Coverage]({coverage_badge})"
                )
            except (ValueError, TypeError):
                pass

        # Badge GitHub Actions si disponible
        if github_owner and github_repo:
            actions_badge = self.generate_github_actions_badge(
                github_owner, github_repo
            )
            badges.append(
                f"[![CI]({actions_badge})](https://github.com/{github_owner}/{github_repo}/actions)"
            )

        # Badge Codecov si disponible
        if github_owner and github_repo:
            codecov_badge = self.generate_codecov_badge(github_owner, github_repo)
            badges.append(
                f"[![Codecov]({codecov_badge})](https://codecov.io/gh/{github_owner}/{github_repo})"
            )

        return "\n".join(badges)

    def generate_status_badges(
        self,
        github_owner: str | None = None,
        github_repo: str | None = None,
        pypi_name: str | None = None,
        license_name: str = "MIT",
    ) -> str:
        """
        Génère les badges de statut standards.

        Args:
            github_owner: Propriétaire GitHub
            github_repo: Dépôt GitHub
            pypi_name: Nom du package PyPI
            license_name: Nom de la licence

        Returns:
            Bloc de badges en Markdown
        """
        badges = []

        # Badge licence
        license_badge = self.generate_shields_badge(
            "License",
            license_name,
            color="blue",
        )
        badges.append(f"![License]({license_badge})")

        # Badge Python version
        python_badge = self.generate_shields_badge(
            "Python",
            "3.8%2B",
            color="blue",
            logo="python",
        )
        badges.append(f"![Python]({python_badge})")

        # Badge GitHub stars si disponible
        if github_owner and github_repo:
            stars_badge = f"https://img.shields.io/github/stars/{github_owner}/{github_repo}?style=flat&logo=github"
            badges.append(
                f"[![Stars]({stars_badge})](https://github.com/{github_owner}/{github_repo})"
            )

        # Badge PyPI si disponible
        if pypi_name:
            pypi_badge = self.generate_pypi_badge(pypi_name)
            badges.append(
                f"[![PyPI]({pypi_badge})](https://pypi.org/project/{pypi_name}/)"
            )

        return "\n".join(badges)

    def generate_all_badges(
        self,
        metrics: dict[str, Any],
        github_owner: str | None = None,
        github_repo: str | None = None,
        pypi_name: str | None = None,
        license_name: str = "MIT",
    ) -> str:
        """
        Génère tous les badges (statut + métriques).

        Args:
            metrics: Dictionnaire de métriques
            github_owner: Propriétaire GitHub
            github_repo: Dépôt GitHub
            pypi_name: Nom du package PyPI
            license_name: Nom de la licence

        Returns:
            Bloc complet de badges en Markdown
        """
        all_badges = []

        # Badges de statut
        status_badges = self.generate_status_badges(
            github_owner, github_repo, pypi_name, license_name
        )
        if status_badges:
            all_badges.append(status_badges)

        # Badges de métriques
        metrics_badges = self.generate_metrics_badges(
            metrics, github_owner, github_repo
        )
        if metrics_badges:
            all_badges.append(metrics_badges)

        return "\n\n".join(all_badges)
