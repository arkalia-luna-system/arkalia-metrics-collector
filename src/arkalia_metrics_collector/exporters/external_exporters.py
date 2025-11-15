#!/usr/bin/env python3
"""
Exporteurs vers services externes.

Support pour :
- Google Sheets
- Notion
- Airtable
- API REST personnalisée
"""

import logging
from typing import Any

try:
    import requests
except ImportError:
    requests = None

logger = logging.getLogger(__name__)


class GoogleSheetsExporter:
    """Exporteur vers Google Sheets via API."""

    def __init__(self, spreadsheet_id: str | None = None) -> None:
        """
        Initialise l'exporteur Google Sheets.

        Args:
            spreadsheet_id: ID de la feuille Google Sheets
        """
        self.spreadsheet_id = spreadsheet_id

    def export(self, metrics: dict[str, Any]) -> bool:
        """
        Exporte les métriques vers Google Sheets.

        Args:
            metrics: Métriques à exporter

        Returns:
            True si l'export a réussi
        """
        # Note: Nécessite l'API Google Sheets
        # Pour l'instant, retourne False car nécessite une configuration complexe
        logger.warning(
            "Export Google Sheets nécessite une configuration API. "
            "Utilisez l'export CSV et importez-le manuellement."
        )
        return False


class NotionExporter:
    """Exporteur vers Notion via API."""

    def __init__(
        self,
        notion_token: str | None = None,
        database_id: str | None = None,
    ) -> None:
        """
        Initialise l'exporteur Notion.

        Args:
            notion_token: Token d'API Notion
            database_id: ID de la base de données Notion
        """
        self.notion_token = notion_token
        self.database_id = database_id

    def export(self, metrics: dict[str, Any]) -> bool:
        """
        Exporte les métriques vers Notion.

        Args:
            metrics: Métriques à exporter

        Returns:
            True si l'export a réussi
        """
        if not self.notion_token or not self.database_id:
            logger.warning(
                "NOTION_TOKEN et NOTION_DATABASE_ID requis pour l'export Notion"
            )
            return False

        if requests is None:
            logger.warning("requests n'est pas installé")
            return False

        # Note: Nécessite l'API Notion
        # Pour l'instant, retourne False car nécessite une configuration complexe
        logger.warning(
            "Export Notion nécessite une configuration API. "
            "Utilisez l'export JSON et importez-le manuellement."
        )
        return False


class AirtableExporter:
    """Exporteur vers Airtable via API."""

    def __init__(
        self,
        api_key: str | None = None,
        base_id: str | None = None,
        table_name: str | None = None,
    ) -> None:
        """
        Initialise l'exporteur Airtable.

        Args:
            api_key: Clé API Airtable
            base_id: ID de la base Airtable
            table_name: Nom de la table
        """
        self.api_key = api_key
        self.base_id = base_id
        self.table_name = table_name

    def export(self, metrics: dict[str, Any]) -> bool:
        """
        Exporte les métriques vers Airtable.

        Args:
            metrics: Métriques à exporter

        Returns:
            True si l'export a réussi
        """
        if not all([self.api_key, self.base_id, self.table_name]):
            logger.warning(
                "AIRTABLE_API_KEY, AIRTABLE_BASE_ID et AIRTABLE_TABLE_NAME requis"
            )
            return False

        if requests is None:
            logger.warning("requests n'est pas installé")
            return False

        # Note: Nécessite l'API Airtable
        # Pour l'instant, retourne False car nécessite une configuration complexe
        logger.warning(
            "Export Airtable nécessite une configuration API. "
            "Utilisez l'export JSON et importez-le manuellement."
        )
        return False


class RESTAPIExporter:
    """Exporteur vers une API REST personnalisée."""

    def __init__(self, api_url: str | None = None, api_key: str | None = None) -> None:
        """
        Initialise l'exporteur API REST.

        Args:
            api_url: URL de l'API REST
            api_key: Clé API (optionnel)
        """
        self.api_url = api_url
        self.api_key = api_key

    def export(self, metrics: dict[str, Any]) -> bool:
        """
        Exporte les métriques vers l'API REST.

        Args:
            metrics: Métriques à exporter

        Returns:
            True si l'export a réussi
        """
        if not self.api_url:
            logger.warning("API_URL requis pour l'export REST")
            return False

        if requests is None:
            logger.warning("requests n'est pas installé")
            return False

        try:
            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            response = requests.post(
                self.api_url, json=metrics, headers=headers, timeout=10
            )

            if response.status_code in (200, 201):
                logger.info(f"Métriques exportées vers {self.api_url}")
                return True
            else:
                logger.error(f"Erreur API REST: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"Erreur lors de l'export REST: {e}")
            return False
