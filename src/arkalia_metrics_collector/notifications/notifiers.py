#!/usr/bin/env python3
"""
Système de notifications pour les alertes métriques.

Support pour :
- Email (SMTP)
- Slack (webhook)
- Discord (webhook)
"""

import logging
import os

try:
    import requests  # type: ignore[import-untyped]
except ImportError:
    requests = None

logger = logging.getLogger(__name__)


class EmailNotifier:
    """Notificateur par email via SMTP."""

    def __init__(
        self,
        smtp_server: str | None = None,
        smtp_port: int = 587,
        username: str | None = None,
        password: str | None = None,
        from_email: str | None = None,
        to_emails: list[str] | None = None,
    ) -> None:
        """
        Initialise le notificateur email.

        Args:
            smtp_server: Serveur SMTP (ou variable SMTP_SERVER)
            smtp_port: Port SMTP (défaut: 587)
            username: Nom d'utilisateur (ou variable SMTP_USERNAME)
            password: Mot de passe (ou variable SMTP_PASSWORD)
            from_email: Email expéditeur (ou variable SMTP_FROM)
            to_emails: Liste des emails destinataires (ou variable SMTP_TO)
        """
        self.smtp_server = smtp_server or os.getenv("SMTP_SERVER")
        self.smtp_port = smtp_port
        self.username = username or os.getenv("SMTP_USERNAME")
        self.password = password or os.getenv("SMTP_PASSWORD")
        self.from_email = from_email or os.getenv("SMTP_FROM")
        self.to_emails = to_emails or (
            os.getenv("SMTP_TO", "").split(",") if os.getenv("SMTP_TO") else []
        )

    def send(self, subject: str, body: str) -> bool:
        """
        Envoie un email.

        Args:
            subject: Sujet de l'email
            body: Corps de l'email

        Returns:
            True si l'envoi a réussi
        """
        if not all(
            [
                self.smtp_server,
                self.username,
                self.password,
                self.from_email,
                self.to_emails,
            ]
        ):
            logger.warning("Configuration SMTP incomplète. Email non envoyé.")
            return False

        # Vérifications de type pour mypy (après la vérification ci-dessus)
        assert self.smtp_server is not None  # nosec B101
        assert self.username is not None  # nosec B101
        assert self.password is not None  # nosec B101
        assert self.from_email is not None  # nosec B101
        assert self.to_emails is not None  # nosec B101

        try:
            import smtplib
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText

            msg = MIMEMultipart()
            msg["From"] = self.from_email
            msg["To"] = ", ".join(self.to_emails)
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "html"))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)
            server.quit()

            logger.info(f"Email envoyé à {', '.join(self.to_emails)}")
            return True

        except Exception as e:
            logger.error(f"Erreur lors de l'envoi d'email: {e}")
            return False


class SlackNotifier:
    """Notificateur Slack via webhook."""

    def __init__(self, webhook_url: str | None = None) -> None:
        """
        Initialise le notificateur Slack.

        Args:
            webhook_url: URL du webhook Slack (ou variable SLACK_WEBHOOK_URL)
        """
        self.webhook_url = webhook_url or os.getenv("SLACK_WEBHOOK_URL")

    def send(self, message: str, title: str = "🚨 Alertes Métriques") -> bool:
        """
        Envoie un message Slack.

        Args:
            message: Message à envoyer
            title: Titre du message

        Returns:
            True si l'envoi a réussi
        """
        if not self.webhook_url:
            logger.warning("SLACK_WEBHOOK_URL non défini. Message non envoyé.")
            return False

        if requests is None:
            logger.warning("requests n'est pas installé. Message Slack non envoyé.")
            return False

        try:
            payload = {
                "text": title,
                "blocks": [
                    {
                        "type": "header",
                        "text": {"type": "plain_text", "text": title},
                    },
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": message},
                    },
                ],
            }

            response = requests.post(self.webhook_url, json=payload, timeout=10)

            if response.status_code == 200:
                logger.info("Message Slack envoyé")
                return True
            else:
                logger.error(f"Erreur Slack: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"Erreur lors de l'envoi Slack: {e}")
            return False


class DiscordNotifier:
    """Notificateur Discord via webhook."""

    def __init__(self, webhook_url: str | None = None) -> None:
        """
        Initialise le notificateur Discord.

        Args:
            webhook_url: URL du webhook Discord (ou variable DISCORD_WEBHOOK_URL)
        """
        self.webhook_url = webhook_url or os.getenv("DISCORD_WEBHOOK_URL")

    def send(self, message: str, title: str = "🚨 Alertes Métriques") -> bool:
        """
        Envoie un message Discord.

        Args:
            message: Message à envoyer
            title: Titre du message

        Returns:
            True si l'envoi a réussi
        """
        if not self.webhook_url:
            logger.warning("DISCORD_WEBHOOK_URL non défini. Message non envoyé.")
            return False

        if requests is None:
            logger.warning("requests n'est pas installé. Message Discord non envoyé.")
            return False

        try:
            # Discord limite à 2000 caractères
            content = message[:1900] if len(message) > 1900 else message

            payload = {
                "embeds": [
                    {
                        "title": title,
                        "description": content,
                        "color": 15158332,  # Rouge pour alertes
                    }
                ]
            }

            response = requests.post(self.webhook_url, json=payload, timeout=10)

            if response.status_code in (200, 204):
                logger.info("Message Discord envoyé")
                return True
            else:
                logger.error(f"Erreur Discord: {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"Erreur lors de l'envoi Discord: {e}")
            return False
