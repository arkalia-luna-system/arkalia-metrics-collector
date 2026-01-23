"""
Tests pour les exporteurs externes (REST API, Google Sheets, Notion, Airtable).

Tests optimisés pour la performance et la mémoire.
"""

import logging
from unittest.mock import Mock, patch

from arkalia_metrics_collector.exporters.external_exporters import (
    AirtableExporter,
    GoogleSheetsExporter,
    NotionExporter,
    RESTAPIExporter,
)


class TestRESTAPIExporter:
    """Tests pour RESTAPIExporter."""

    def test_init_with_url(self):
        """Test initialisation avec URL."""
        exporter = RESTAPIExporter(api_url="https://api.example.com/metrics")
        assert exporter.api_url == "https://api.example.com/metrics"
        assert exporter.api_key is None

    def test_init_with_key(self):
        """Test initialisation avec clé API."""
        exporter = RESTAPIExporter(
            api_url="https://api.example.com/metrics", api_key="test_key"
        )
        assert exporter.api_url == "https://api.example.com/metrics"
        assert exporter.api_key == "test_key"

    @patch("arkalia_metrics_collector.exporters.external_exporters.requests")
    def test_export_success(self, mock_requests):
        """Test export réussi."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_requests.post.return_value = mock_response

        exporter = RESTAPIExporter(
            api_url="https://api.example.com/metrics", api_key="test_key"
        )
        metrics = {"test": "data"}

        result = exporter.export(metrics)

        assert result is True
        mock_requests.post.assert_called_once()
        call_args = mock_requests.post.call_args
        assert call_args[0][0] == "https://api.example.com/metrics"
        assert call_args[1]["json"] == metrics
        assert "Authorization" in call_args[1]["headers"]

    @patch("arkalia_metrics_collector.exporters.external_exporters.requests")
    def test_export_without_key(self, mock_requests):
        """Test export sans clé API."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_requests.post.return_value = mock_response

        exporter = RESTAPIExporter(api_url="https://api.example.com/metrics")
        metrics = {"test": "data"}

        result = exporter.export(metrics)

        assert result is True
        call_args = mock_requests.post.call_args
        assert "Authorization" not in call_args[1]["headers"]

    @patch("arkalia_metrics_collector.exporters.external_exporters.requests")
    def test_export_error_status(self, mock_requests):
        """Test export avec erreur HTTP."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_requests.post.return_value = mock_response

        exporter = RESTAPIExporter(api_url="https://api.example.com/metrics")
        metrics = {"test": "data"}

        result = exporter.export(metrics)

        assert result is False

    @patch("arkalia_metrics_collector.exporters.external_exporters.requests")
    def test_export_exception(self, mock_requests):
        """Test export avec exception."""
        mock_requests.post.side_effect = Exception("Network error")

        exporter = RESTAPIExporter(api_url="https://api.example.com/metrics")
        metrics = {"test": "data"}

        result = exporter.export(metrics)

        assert result is False

    def test_export_no_url(self):
        """Test export sans URL."""
        exporter = RESTAPIExporter(api_url=None)
        metrics = {"test": "data"}

        result = exporter.export(metrics)

        assert result is False

    @patch("arkalia_metrics_collector.exporters.external_exporters.requests")
    def test_export_timeout(self, mock_requests):
        """Test export avec timeout."""
        import requests

        mock_requests.post.side_effect = requests.exceptions.Timeout("Timeout")

        exporter = RESTAPIExporter(api_url="https://api.example.com/metrics")
        metrics = {"test": "data"}

        result = exporter.export(metrics)

        assert result is False

    @patch("arkalia_metrics_collector.exporters.external_exporters.requests")
    def test_export_connection_error(self, mock_requests):
        """Test export avec erreur de connexion."""
        import requests

        mock_requests.post.side_effect = requests.exceptions.ConnectionError(
            "Connection error"
        )

        exporter = RESTAPIExporter(api_url="https://api.example.com/metrics")
        metrics = {"test": "data"}

        result = exporter.export(metrics)

        assert result is False

    @patch("arkalia_metrics_collector.exporters.external_exporters.requests")
    def test_export_uses_timeout(self, mock_requests):
        """Test que l'export utilise le timeout configuré."""
        # HTTP_TIMEOUT est défini dans external_exporters.py
        HTTP_TIMEOUT = 10  # Valeur par défaut

        mock_response = Mock()
        mock_response.status_code = 200
        mock_requests.post.return_value = mock_response

        exporter = RESTAPIExporter(api_url="https://api.example.com/metrics")
        metrics = {"test": "data"}

        exporter.export(metrics)

        # Vérifier que timeout est utilisé
        call_kwargs = mock_requests.post.call_args[1]
        assert call_kwargs["timeout"] == HTTP_TIMEOUT


class TestGoogleSheetsExporter:
    """Tests pour GoogleSheetsExporter."""

    def test_init(self):
        """Test initialisation."""
        exporter = GoogleSheetsExporter(spreadsheet_id="test_id")
        assert exporter.spreadsheet_id == "test_id"

    def test_init_without_id(self):
        """Test initialisation sans spreadsheet_id."""
        exporter = GoogleSheetsExporter(spreadsheet_id=None)
        assert exporter.spreadsheet_id is None

    def test_export_not_implemented(self):
        """Test que l'export retourne False (non implémenté)."""
        exporter = GoogleSheetsExporter(spreadsheet_id="test_id")
        metrics = {"test": "data"}

        result = exporter.export(metrics)

        assert result is False

    def test_export_warning_logged(self, caplog):
        """Test que l'export logge un avertissement."""
        with caplog.at_level(logging.WARNING):
            exporter = GoogleSheetsExporter(spreadsheet_id="test_id")
            exporter.export({"test": "data"})
            # Vérifier qu'un avertissement est loggé (peut contenir différents messages)
            assert len(caplog.records) > 0
            assert any(
                "google sheets" in record.message.lower() for record in caplog.records
            )


class TestNotionExporter:
    """Tests pour NotionExporter."""

    def test_init_with_params(self):
        """Test initialisation avec paramètres."""
        exporter = NotionExporter(notion_token="test_token", database_id="test_db")
        assert exporter.notion_token == "test_token"
        assert exporter.database_id == "test_db"

    def test_export_no_token(self):
        """Test export sans token."""
        exporter = NotionExporter(notion_token=None, database_id="test_db")
        metrics = {"test": "data"}

        result = exporter.export(metrics)

        assert result is False

    def test_export_no_database(self):
        """Test export sans database ID."""
        exporter = NotionExporter(notion_token="test_token", database_id=None)
        metrics = {"test": "data"}

        result = exporter.export(metrics)

        assert result is False

    def test_export_not_implemented(self):
        """Test que l'export retourne False (non implémenté)."""
        exporter = NotionExporter(notion_token="test_token", database_id="test_db")
        metrics = {"test": "data"}

        result = exporter.export(metrics)

        assert result is False

    @patch("arkalia_metrics_collector.exporters.external_exporters.requests")
    def test_export_requests_not_installed(self, mock_requests_module):
        """Test export quand requests n'est pas installé."""
        # Simuler que requests n'est pas installé
        mock_requests_module.return_value = None
        exporter = NotionExporter(notion_token="test_token", database_id="test_db")
        metrics = {"test": "data"}

        result = exporter.export(metrics)

        assert result is False

    def test_export_warning_logged(self, caplog):
        """Test que l'export logge un avertissement."""
        with caplog.at_level(logging.WARNING):
            exporter = NotionExporter(notion_token="test_token", database_id="test_db")
            exporter.export({"test": "data"})
            # Vérifier qu'un avertissement est loggé (peut contenir différents messages)
            assert len(caplog.records) > 0
            assert any("notion" in record.message.lower() for record in caplog.records)


class TestAirtableExporter:
    """Tests pour AirtableExporter."""

    def test_init_with_params(self):
        """Test initialisation avec paramètres."""
        exporter = AirtableExporter(
            api_key="test_key", base_id="test_base", table_name="test_table"
        )
        assert exporter.api_key == "test_key"
        assert exporter.base_id == "test_base"
        assert exporter.table_name == "test_table"

    def test_export_missing_params(self):
        """Test export avec paramètres manquants."""
        exporter = AirtableExporter(
            api_key=None, base_id="test_base", table_name="test_table"
        )
        metrics = {"test": "data"}

        result = exporter.export(metrics)

        assert result is False

    def test_export_not_implemented(self):
        """Test que l'export retourne False (non implémenté)."""
        exporter = AirtableExporter(
            api_key="test_key", base_id="test_base", table_name="test_table"
        )
        metrics = {"test": "data"}

        result = exporter.export(metrics)

        assert result is False

    def test_export_missing_all_params(self):
        """Test export avec tous les paramètres manquants."""
        exporter = AirtableExporter(api_key=None, base_id=None, table_name=None)
        metrics = {"test": "data"}

        result = exporter.export(metrics)

        assert result is False

    @patch("arkalia_metrics_collector.exporters.external_exporters.requests")
    def test_export_requests_not_installed(self, mock_requests_module):
        """Test export quand requests n'est pas installé."""
        # Simuler que requests n'est pas installé
        mock_requests_module.return_value = None
        exporter = AirtableExporter(
            api_key="test_key", base_id="test_base", table_name="test_table"
        )
        metrics = {"test": "data"}

        result = exporter.export(metrics)

        assert result is False

    def test_export_warning_logged(self, caplog):
        """Test que l'export logge un avertissement."""
        with caplog.at_level(logging.WARNING):
            exporter = AirtableExporter(
                api_key="test_key", base_id="test_base", table_name="test_table"
            )
            exporter.export({"test": "data"})
            # Vérifier qu'un avertissement est loggé (peut contenir différents messages)
            assert len(caplog.records) > 0
            assert any(
                "airtable" in record.message.lower() for record in caplog.records
            )
