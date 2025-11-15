#!/usr/bin/env python3
"""
Collecteur de statistiques de contribution Git.

Analyse l'historique Git pour calculer :
- Nombre de commits
- Lignes ajoutées/supprimées
- Fichiers modifiés
- Contributeurs
- Activité temporelle
"""

import logging
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class GitContributions:
    """
    Collecteur de statistiques de contribution Git.
    """

    def __init__(self, project_path: str | Path) -> None:
        """
        Initialise le collecteur de contributions Git.

        Args:
            project_path: Chemin vers le projet
        """
        self.project_path = Path(project_path)

    def collect_contributions(self, days: int = 30) -> dict[str, Any] | None:
        """
        Collecte les statistiques de contribution Git.

        Args:
            days: Nombre de jours à analyser (défaut: 30)

        Returns:
            Dictionnaire avec les statistiques ou None en cas d'erreur
        """
        if not self.project_path.exists():
            logger.error(f"Chemin projet non trouvé: {self.project_path}")
            return None

        if not (self.project_path / ".git").exists():
            logger.warning(f"Pas de dépôt Git dans: {self.project_path}")
            return None

        try:
            # Statistiques générales
            total_commits = self._get_total_commits()
            recent_commits = self._get_recent_commits(days)
            contributors = self._get_contributors(days)
            lines_stats = self._get_lines_stats(days)
            files_changed = self._get_files_changed(days)
            activity_by_day = self._get_activity_by_day(days)

            return {
                "total_commits": total_commits,
                "recent_commits": recent_commits,
                "contributors": contributors,
                "lines": lines_stats,
                "files_changed": files_changed,
                "activity_by_day": activity_by_day,
                "period_days": days,
                "collection_date": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"Erreur lors de la collecte Git: {e}")
            return None

    def _run_git_command(self, command: list[str]) -> str | None:
        """Exécute une commande Git et retourne la sortie."""
        try:
            result = subprocess.run(
                ["git"] + command,
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                return result.stdout.strip()
            return None
        except Exception as e:
            logger.debug(f"Erreur commande Git: {e}")
            return None

    def _get_total_commits(self) -> int:
        """Retourne le nombre total de commits."""
        output = self._run_git_command(["rev-list", "--count", "HEAD"])
        if output:
            try:
                return int(output)
            except ValueError:
                return 0
        return 0

    def _get_recent_commits(self, days: int) -> int:
        """Retourne le nombre de commits récents."""
        since_date = (datetime.now() - timedelta(days=days)).isoformat()
        output = self._run_git_command(
            ["rev-list", "--count", f"--since={since_date}", "HEAD"]
        )
        if output:
            try:
                return int(output)
            except ValueError:
                return 0
        return 0

    def _get_contributors(self, days: int) -> list[dict[str, Any]]:
        """Retourne la liste des contributeurs avec leurs statistiques."""
        since_date = (datetime.now() - timedelta(days=days)).isoformat()
        output = self._run_git_command(
            [
                "shortlog",
                "-sn",
                f"--since={since_date}",
                "HEAD",
            ]
        )

        contributors = []
        if output:
            for line in output.split("\n"):
                if line.strip():
                    parts = line.strip().split("\t")
                    if len(parts) == 2:
                        try:
                            commits = int(parts[0].strip())
                            name = parts[1].strip()
                            contributors.append({"name": name, "commits": commits})
                        except ValueError:
                            continue

        return contributors

    def _get_lines_stats(self, days: int) -> dict[str, int]:
        """Retourne les statistiques de lignes ajoutées/supprimées."""
        since_date = (datetime.now() - timedelta(days=days)).isoformat()
        output = self._run_git_command(
            [
                "log",
                f"--since={since_date}",
                "--pretty=tformat:",
                "--numstat",
                "HEAD",
            ]
        )

        added = 0
        deleted = 0

        if output:
            for line in output.split("\n"):
                if line.strip():
                    parts = line.strip().split("\t")
                    if len(parts) >= 2:
                        try:
                            added += int(parts[0]) if parts[0] != "-" else 0
                            deleted += int(parts[1]) if parts[1] != "-" else 0
                        except ValueError:
                            continue

        return {"added": added, "deleted": deleted, "net": added - deleted}

    def _get_files_changed(self, days: int) -> int:
        """Retourne le nombre de fichiers modifiés."""
        since_date = (datetime.now() - timedelta(days=days)).isoformat()
        output = self._run_git_command(
            [
                "log",
                f"--since={since_date}",
                "--pretty=tformat:",
                "--name-only",
                "HEAD",
            ]
        )

        if output:
            files = {line.strip() for line in output.split("\n") if line.strip()}
            return len(files)

        return 0

    def _get_activity_by_day(self, days: int) -> list[dict[str, Any]]:
        """Retourne l'activité par jour."""
        since_date = (datetime.now() - timedelta(days=days)).isoformat()
        output = self._run_git_command(
            [
                "log",
                f"--since={since_date}",
                "--pretty=format:%ad",
                "--date=short",
                "HEAD",
            ]
        )

        activity: dict[str, int] = {}
        if output:
            for line in output.split("\n"):
                if line.strip():
                    date = line.strip()
                    activity[date] = activity.get(date, 0) + 1

        # Convertir en liste triée
        result = [
            {"date": date, "commits": count} for date, count in sorted(activity.items())
        ]

        return result
