#!/usr/bin/env python3
"""
Système de notifications et alertes pour les métriques.

Détecte les changements significatifs dans les métriques et génère des alertes.
"""

from datetime import datetime
from pathlib import Path
from typing import Any

from arkalia_metrics_collector.collectors.metrics_history import MetricsHistory


class MetricsAlerts:
    """
    Système d'alertes pour les métriques.

    Détecte les changements significatifs et génère des notifications.
    """

    def __init__(
        self,
        threshold_percent: float = 10.0,
        history_dir: str | Path = "metrics/history",
    ) -> None:
        """
        Initialise le système d'alertes.

        Args:
            threshold_percent: Seuil de changement significatif (en %)
            history_dir: Dossier contenant l'historique des métriques
        """
        self.threshold_percent = threshold_percent
        self.history = MetricsHistory(history_dir)

    def check_significant_changes(
        self, current_metrics: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Vérifie les changements significatifs dans les métriques.

        Args:
            current_metrics: Métriques actuelles

        Returns:
            Dictionnaire avec les alertes détectées
        """
        previous_metrics = self.history.get_latest_metrics()

        if not previous_metrics:
            return {
                "has_alerts": False,
                "message": "Aucun historique disponible pour comparaison",
            }

        alerts = []
        current_agg = current_metrics.get("aggregated", {})
        previous_agg = previous_metrics.get("aggregated", {})

        metrics_to_check = [
            ("total_modules", "Modules Python"),
            ("total_lines_of_code", "Lignes de code"),
            ("total_tests", "Tests"),
            ("total_documentation_files", "Fichiers de documentation"),
            ("global_coverage", "Coverage global"),
        ]

        for metric_key, metric_name in metrics_to_check:
            current_value = current_agg.get(metric_key)
            previous_value = previous_agg.get(metric_key)

            if current_value is None or previous_value is None:
                continue

            if previous_value == 0:
                continue  # Éviter division par zéro

            delta = current_value - previous_value
            delta_percent = (delta / previous_value) * 100

            if abs(delta_percent) >= self.threshold_percent:
                alert_type = "increase" if delta > 0 else "decrease"
                alerts.append(
                    {
                        "metric": metric_name,
                        "metric_key": metric_key,
                        "previous": previous_value,
                        "current": current_value,
                        "delta": delta,
                        "delta_percent": round(delta_percent, 2),
                        "type": alert_type,
                        "threshold": self.threshold_percent,
                    }
                )

        return {
            "has_alerts": len(alerts) > 0,
            "alerts": alerts,
            "previous_date": previous_metrics.get("collection_date", "Inconnu"),
            "current_date": current_metrics.get("collection_date", "Inconnu"),
        }

    def generate_alert_message(self, alerts_data: dict[str, Any]) -> str:
        """
        Génère un message d'alerte formaté.

        Args:
            alerts_data: Données des alertes

        Returns:
            Message d'alerte formaté
        """
        if not alerts_data.get("has_alerts"):
            return "Aucune alerte détectée."

        alerts = alerts_data.get("alerts", [])
        message_parts = [
            "## 🚨 Alertes Métriques - Changements Significatifs",
            "",
            f"**Date précédente:** {alerts_data.get('previous_date', 'Inconnu')}",
            f"**Date actuelle:** {alerts_data.get('current_date', 'Inconnu')}",
            "",
            "### Changements détectés:",
            "",
        ]

        for alert in alerts:
            delta_sign = "+" if alert["delta"] > 0 else ""
            emoji = "📈" if alert["type"] == "increase" else "📉"
            message_parts.append(
                f"{emoji} **{alert['metric']}**: "
                f"{alert['previous']:,} → {alert['current']:,} "
                f"({delta_sign}{alert['delta_percent']:.1f}%)"
            )

        return "\n".join(message_parts)

    def create_github_issue_body(self, alerts_data: dict[str, Any]) -> str:
        """
        Génère le corps d'une issue GitHub pour les alertes.

        Args:
            alerts_data: Données des alertes

        Returns:
            Corps de l'issue GitHub formaté
        """
        if not alerts_data.get("has_alerts"):
            return ""

        alerts = alerts_data.get("alerts", [])
        body_parts = [
            "## 🚨 Alertes Métriques - Changements Significatifs",
            "",
            "Des changements significatifs ont été détectés dans les métriques du projet.",
            "",
            "### 📊 Résumé",
            "",
            f"- **Date précédente:** {alerts_data.get('previous_date', 'Inconnu')}",
            f"- **Date actuelle:** {alerts_data.get('current_date', 'Inconnu')}",
            f"- **Seuil d'alerte:** {self.threshold_percent}%",
            "",
            "### 📈 Changements Détectés",
            "",
            "| Métrique | Avant | Après | Variation |",
            "|----------|-------|-------|-----------|",
        ]

        for alert in alerts:
            delta_sign = "+" if alert["delta"] > 0 else ""
            body_parts.append(
                f"| {alert['metric']} | {alert['previous']:,} | "
                f"{alert['current']:,} | {delta_sign}{alert['delta_percent']:.1f}% |"
            )

        body_parts.extend(
            [
                "",
                "### 🔍 Détails",
                "",
                "Ces changements dépassent le seuil de "
                f"{self.threshold_percent}% et peuvent indiquer:",
                "",
                "- 📈 **Augmentation**: Ajout de code, nouveaux tests, amélioration coverage",
                "- 📉 **Diminution**: Suppression de code, refactoring, nettoyage",
                "",
                "### 💡 Actions Recommandées",
                "",
                "1. Vérifier les changements dans les projets",
                "2. Examiner les commits récents",
                "3. Valider que les changements sont intentionnels",
                "",
                "---",
                f"*Généré automatiquement le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
            ]
        )

        return "\n".join(body_parts)

    def should_create_issue(self, alerts_data: dict[str, Any]) -> bool:
        """
        Détermine si une issue GitHub doit être créée.

        Args:
            alerts_data: Données des alertes

        Returns:
            True si une issue doit être créée
        """
        if not alerts_data.get("has_alerts"):
            return False

        # Créer une issue seulement si au moins une alerte est significative
        alerts = alerts_data.get("alerts", [])
        return len(alerts) > 0
