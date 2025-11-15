#!/usr/bin/env python3
"""
Gestionnaire d'historique des métriques.

Gère le stockage et la comparaison temporelle des métriques agrégées.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class MetricsHistory:
    """
    Gestionnaire d'historique des métriques.

    Permet de :
    - Sauvegarder les métriques avec timestamp
    - Charger les métriques précédentes
    - Comparer les métriques actuelles vs précédentes
    - Générer des rapports d'évolution
    """

    def __init__(self, history_dir: str | Path = "metrics/history") -> None:
        """
        Initialise le gestionnaire d'historique.

        Args:
            history_dir: Dossier pour stocker l'historique
        """
        self.history_dir = Path(history_dir)
        self.history_dir.mkdir(parents=True, exist_ok=True)

    def save_metrics(self, aggregated_metrics: dict[str, Any]) -> Path:
        """
        Sauvegarde les métriques agrégées avec timestamp.

        Args:
            aggregated_metrics: Métriques agrégées à sauvegarder

        Returns:
            Chemin vers le fichier sauvegardé
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"metrics_{timestamp}.json"
        filepath = self.history_dir / filename

        # Ajouter le timestamp de sauvegarde
        metrics_with_timestamp = {
            **aggregated_metrics,
            "saved_at": datetime.now().isoformat(),
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(metrics_with_timestamp, f, indent=2, ensure_ascii=False)

        return filepath

    def get_latest_metrics(self) -> dict[str, Any] | None:
        """
        Récupère les métriques les plus récentes.

        Returns:
            Métriques les plus récentes ou None si aucun historique
        """
        history_files = sorted(self.history_dir.glob("metrics_*.json"), reverse=True)

        if not history_files:
            return None

        latest_file = history_files[0]
        with open(latest_file, encoding="utf-8") as f:
            return json.load(f)

    def compare_metrics(
        self, current: dict[str, Any], previous: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        Compare les métriques actuelles avec les précédentes.

        Args:
            current: Métriques actuelles
            previous: Métriques précédentes (si None, charge la plus récente)

        Returns:
            Dictionnaire avec les deltas et pourcentages de changement
        """
        if previous is None:
            previous = self.get_latest_metrics()

        if previous is None:
            return {
                "has_previous": False,
                "message": "Aucune métrique précédente disponible",
            }

        current_agg = current.get("aggregated", {})
        previous_agg = previous.get("aggregated", {})

        # Calculer les deltas
        deltas = {
            "total_modules": self._calculate_delta(
                current_agg.get("total_modules", 0),
                previous_agg.get("total_modules", 0),
            ),
            "total_lines_of_code": self._calculate_delta(
                current_agg.get("total_lines_of_code", 0),
                previous_agg.get("total_lines_of_code", 0),
            ),
            "total_tests": self._calculate_delta(
                current_agg.get("total_tests", 0),
                previous_agg.get("total_tests", 0),
            ),
            "total_documentation_files": self._calculate_delta(
                current_agg.get("total_documentation_files", 0),
                previous_agg.get("total_documentation_files", 0),
            ),
            "global_coverage": self._calculate_delta(
                current_agg.get("global_coverage"),
                previous_agg.get("global_coverage"),
                is_percentage=True,
            ),
        }

        # Comparer les projets
        current_projects = {p["name"]: p for p in current.get("projects", [])}
        previous_projects = {p["name"]: p for p in previous.get("projects", [])}

        project_changes = {}
        for name in set(current_projects.keys()) | set(previous_projects.keys()):
            current_p = current_projects.get(name, {})
            previous_p = previous_projects.get(name, {})

            project_changes[name] = {
                "modules": self._calculate_delta(
                    current_p.get("modules", 0),
                    previous_p.get("modules", 0),
                ),
                "lines_of_code": self._calculate_delta(
                    current_p.get("lines_of_code", 0),
                    previous_p.get("lines_of_code", 0),
                ),
                "tests": self._calculate_delta(
                    current_p.get("tests", 0),
                    previous_p.get("tests", 0),
                ),
            }

        return {
            "has_previous": True,
            "previous_date": previous.get("collection_date", "Inconnu"),
            "current_date": current.get("collection_date", "Inconnu"),
            "deltas": deltas,
            "project_changes": project_changes,
        }

    def _calculate_delta(
        self,
        current: int | float | None,
        previous: int | float | None,
        is_percentage: bool = False,
    ) -> dict[str, Any]:
        """
        Calcule le delta entre deux valeurs.

        Args:
            current: Valeur actuelle
            previous: Valeur précédente
            is_percentage: Si True, traite comme un pourcentage

        Returns:
            Dictionnaire avec delta, pourcentage de changement, etc.
        """
        if current is None or previous is None:
            return {
                "current": current,
                "previous": previous,
                "delta": None,
                "delta_percent": None,
                "trend": "unknown",
            }

        try:
            current_val = float(current)
            previous_val = float(previous)
            delta = current_val - previous_val

            if previous_val == 0:
                delta_percent = 100.0 if current_val > 0 else 0.0
            else:
                delta_percent = (delta / previous_val) * 100.0

            # Déterminer la tendance
            if abs(delta) < 0.01:  # Équivalent à 0 pour les floats
                trend = "stable"
            elif delta > 0:
                trend = "up"
            else:
                trend = "down"

            return {
                "current": current_val,
                "previous": previous_val,
                "delta": delta,
                "delta_percent": round(delta_percent, 2),
                "trend": trend,
            }
        except (ValueError, TypeError):
            return {
                "current": current,
                "previous": previous,
                "delta": None,
                "delta_percent": None,
                "trend": "unknown",
            }

    def generate_evolution_report(self, comparison: dict[str, Any]) -> str:
        """
        Génère un rapport d'évolution en Markdown.

        Args:
            comparison: Résultat de compare_metrics()

        Returns:
            Rapport Markdown formaté
        """
        if not comparison.get("has_previous"):
            return "## 📈 Évolution des Métriques\n\n*Aucune métrique précédente disponible pour comparaison.*\n"

        report = "## 📈 Évolution des Métriques\n\n"
        report += f"**Comparaison** : {comparison['previous_date']} → {comparison['current_date']}\n\n"

        deltas = comparison.get("deltas", {})
        report += "### 📊 Métriques Globales\n\n"
        report += "| Métrique | Avant | Après | Delta | Évolution |\n"
        report += "|:---------|:-----:|:-----:|:-----:|:----------:|\n"

        for metric_name, delta_data in deltas.items():
            if delta_data.get("delta") is None:
                continue

            current = delta_data["current"]
            previous = delta_data["previous"]
            delta = delta_data["delta"]
            delta_pct = delta_data["delta_percent"]
            trend = delta_data["trend"]

            # Formater selon le type
            if "coverage" in metric_name.lower():
                current_str = f"{current:.1f}%" if current else "N/A"
                previous_str = f"{previous:.1f}%" if previous else "N/A"
                delta_str = f"{delta:+.1f}%" if delta else "N/A"
            else:
                current_str = f"{current:,.0f}" if current else "N/A"
                previous_str = f"{previous:,.0f}" if previous else "N/A"
                delta_str = f"{delta:+,.0f}" if delta else "N/A"

            # Icône de tendance
            if trend == "up":
                trend_icon = "📈"
            elif trend == "down":
                trend_icon = "📉"
            else:
                trend_icon = "➡️"

            delta_pct_str = f"({delta_pct:+.1f}%)" if delta_pct else ""
            report += f"| **{metric_name.replace('_', ' ').title()}** | {previous_str} | {current_str} | {delta_str} {delta_pct_str} | {trend_icon} |\n"

        report += "\n"
        return report
