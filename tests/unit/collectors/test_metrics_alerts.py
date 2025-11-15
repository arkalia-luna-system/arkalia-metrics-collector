#!/usr/bin/env python3
"""
Tests unitaires pour MetricsAlerts.
"""

from pathlib import Path
from tempfile import TemporaryDirectory

from arkalia_metrics_collector.collectors.metrics_alerts import MetricsAlerts
from arkalia_metrics_collector.collectors.metrics_history import MetricsHistory


class TestMetricsAlerts:
    """Tests pour MetricsAlerts."""

    def test_init(self):
        """Test l'initialisation de MetricsAlerts."""
        alerts = MetricsAlerts(threshold_percent=15.0)
        assert alerts.threshold_percent == 15.0
        assert alerts.history is not None

    def test_check_significant_changes_no_history(self):
        """Test la vérification sans historique."""
        with TemporaryDirectory() as tmpdir:
            alerts = MetricsAlerts(history_dir=str(Path(tmpdir) / "history"))
            current_metrics = {
                "aggregated": {
                    "total_modules": 1000,
                    "total_lines_of_code": 50000,
                    "total_tests": 200,
                },
                "collection_date": "2025-01-01T00:00:00",
            }

            result = alerts.check_significant_changes(current_metrics)
            assert result["has_alerts"] is False
            assert "Aucun historique" in result["message"]

    def test_check_significant_changes_with_history(self):
        """Test la vérification avec historique."""
        with TemporaryDirectory() as tmpdir:
            history_dir = Path(tmpdir) / "history"
            history_dir.mkdir()

            # Créer un historique
            history = MetricsHistory(str(history_dir))
            previous_metrics = {
                "aggregated": {
                    "total_modules": 1000,
                    "total_lines_of_code": 50000,
                    "total_tests": 200,
                    "total_documentation_files": 50,
                    "global_coverage": 75.0,
                },
                "collection_date": "2025-01-01T00:00:00",
            }
            history.save_metrics(previous_metrics)

            # Métriques actuelles avec changement significatif (>10%)
            current_metrics = {
                "aggregated": {
                    "total_modules": 1200,  # +20%
                    "total_lines_of_code": 50000,  # Pas de changement
                    "total_tests": 180,  # -10% (seuil)
                    "total_documentation_files": 50,  # Pas de changement
                    "global_coverage": 75.0,  # Pas de changement
                },
                "collection_date": "2025-01-02T00:00:00",
            }

            alerts = MetricsAlerts(threshold_percent=10.0, history_dir=str(history_dir))
            result = alerts.check_significant_changes(current_metrics)

            assert result["has_alerts"] is True
            assert len(result["alerts"]) >= 1

            # Vérifier que l'alerte pour modules est présente
            modules_alert = next(
                (a for a in result["alerts"] if a["metric_key"] == "total_modules"),
                None,
            )
            assert modules_alert is not None
            assert modules_alert["delta_percent"] > 10.0

    def test_generate_alert_message(self):
        """Test la génération du message d'alerte."""
        alerts = MetricsAlerts()
        alerts_data = {
            "has_alerts": True,
            "previous_date": "2025-01-01",
            "current_date": "2025-01-02",
            "alerts": [
                {
                    "metric": "Modules Python",
                    "metric_key": "total_modules",
                    "previous": 1000,
                    "current": 1200,
                    "delta": 200,
                    "delta_percent": 20.0,
                    "type": "increase",
                    "threshold": 10.0,
                }
            ],
        }

        message = alerts.generate_alert_message(alerts_data)
        assert "Alertes Métriques" in message
        assert "Modules Python" in message
        assert "1,000" in message or "1000" in message  # Formatage avec virgules
        assert "1,200" in message or "1200" in message
        assert "20.0" in message

    def test_create_github_issue_body(self):
        """Test la génération du corps d'issue GitHub."""
        alerts = MetricsAlerts()
        alerts_data = {
            "has_alerts": True,
            "previous_date": "2025-01-01",
            "current_date": "2025-01-02",
            "alerts": [
                {
                    "metric": "Modules Python",
                    "metric_key": "total_modules",
                    "previous": 1000,
                    "current": 1200,
                    "delta": 200,
                    "delta_percent": 20.0,
                    "type": "increase",
                    "threshold": 10.0,
                }
            ],
        }

        body = alerts.create_github_issue_body(alerts_data)
        assert "Alertes Métriques" in body
        assert "Modules Python" in body
        assert "| Métrique |" in body
        assert "1,000" in body or "1000" in body  # Formatage avec virgules
        assert "1,200" in body or "1200" in body

    def test_should_create_issue(self):
        """Test la décision de création d'issue."""
        alerts = MetricsAlerts()

        # Avec alertes
        alerts_data_with = {
            "has_alerts": True,
            "alerts": [{"metric": "Test"}],
        }
        assert alerts.should_create_issue(alerts_data_with) is True

        # Sans alertes
        alerts_data_without = {
            "has_alerts": False,
            "alerts": [],
        }
        assert alerts.should_create_issue(alerts_data_without) is False
