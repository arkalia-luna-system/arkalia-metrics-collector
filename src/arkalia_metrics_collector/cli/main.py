#!/usr/bin/env python3
"""
Arkalia Metrics Collector - Interface en ligne de commande.

Interface CLI principale pour utiliser le collecteur de métriques.
"""

import sys
from typing import Optional

import click
from pathlib import Path


# Ajouter le chemin du projet pour les imports
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from arkalia_metrics_collector import (
        MetricsCollector,
        MetricsExporter,
        MetricsValidator,
    )
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    print("📍 Assurez-vous que le package est installé correctement.")
    sys.exit(1)


@click.group()
@click.version_option(version="1.0.0", prog_name="arkalia-metrics")
def cli():
    """
    Arkalia Metrics Collector - Outil professionnel de métriques Python.

    Collecte des métriques fiables sur vos projets Python en excluant
    automatiquement les venv, cache et dépendances.
    """
    pass


@cli.command()
@click.argument(
    "project_path", type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
@click.option(
    "--output", "-o", default="metrics", help="Dossier de sortie (défaut: metrics)"
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["json", "markdown", "html", "csv", "all"]),
    default="all",
    help="Format d'export (défaut: all)",
)
@click.option("--validate", "-v", is_flag=True, help="Valider les métriques collectées")
@click.option("--verbose", is_flag=True, help="Mode verbeux")
def collect(project_path: str, output: str, format: str, validate: bool, verbose: bool):
    """
    Collecte les métriques d'un projet Python.

    PROJECT_PATH: Chemin vers le projet à analyser
    """
    if verbose:
        click.echo(f"🔍 Collecte des métriques pour {project_path}...")
        click.echo(f"📁 Dossier de sortie: {output}")
        click.echo(f"📊 Format: {format}")

    try:
        # Collecter les métriques
        collector = MetricsCollector(project_path)
        metrics_data = collector.collect_all_metrics()

        if verbose:
            click.echo("✅ Métriques collectées avec succès")

        # Valider si demandé
        if validate:
            validator = MetricsValidator()
            is_valid, errors, warnings = validator.validate_metrics(metrics_data)

            if verbose:
                if errors:
                    click.echo(f"❌ Erreurs de validation: {len(errors)}")
                    for error in errors:
                        click.echo(f"   • {error}")
                if warnings:
                    click.echo(f"⚠️  Avertissements: {len(warnings)}")
                    for warning in warnings:
                        click.echo(f"   • {warning}")

                validation_report = validator.get_validation_report()
                click.echo(
                    f"📊 Score de validation: {validation_report['validation_summary']['score']}/100"
                )

        # Exporter les métriques
        exporter = MetricsExporter(metrics_data)

        if format == "all":
            results = exporter.export_all_formats(output)
            if verbose:
                for fmt, success in results.items():
                    status = "✅" if success else "❌"
                    click.echo(
                        f"{status} Export {fmt}: {'Succès' if success else 'Échec'}"
                    )
        else:
            success = False
            if format == "json":
                success = exporter.export_json(f"{output}/metrics.json")
            elif format == "markdown":
                success = exporter.export_markdown_summary(f"{output}/metrics.md")
            elif format == "html":
                success = exporter.export_html_dashboard(f"{output}/dashboard.html")
            elif format == "csv":
                success = exporter.export_csv(f"{output}/metrics.csv")

            if verbose:
                status = "✅" if success else "❌"
                click.echo(
                    f"{status} Export {format}: {'Succès' if success else 'Échec'}"
                )

        # Afficher un résumé
        summary = metrics_data.get("summary", {})
        click.echo("\n📊 Résumé des métriques:")
        click.echo(f"   🐍 Fichiers Python: {summary.get('total_python_files', 0):,}")
        click.echo(f"   📝 Lignes de code: {summary.get('lines_of_code', 0):,}")
        click.echo(f"   🧪 Tests: {summary.get('collected_tests', 0):,}")
        click.echo(f"   📚 Documentation: {summary.get('documentation_files', 0):,}")
        click.echo(f"\n💾 Métriques exportées dans: {output}/")

    except Exception as e:
        click.echo(f"❌ Erreur lors de la collecte: {e}")
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.argument(
    "project_path", type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
def validate(project_path: str):
    """
    Valide les métriques d'un projet Python.

    PROJECT_PATH: Chemin vers le projet à valider
    """
    try:
        # Collecter et valider
        collector = MetricsCollector(project_path)
        metrics_data = collector.collect_all_metrics()

        validator = MetricsValidator()
        is_valid, errors, warnings = validator.validate_metrics(metrics_data)

        # Afficher le rapport
        validation_report = validator.get_validation_report()

        click.echo(f"🔍 Validation des métriques pour {project_path}")
        click.echo(f"📊 Score: {validation_report['validation_summary']['score']}/100")
        click.echo(f"📈 Statut: {validation_report['validation_summary']['status']}")

        if errors:
            click.echo(f"\n❌ Erreurs ({len(errors)}):")
            for error in errors:
                click.echo(f"   • {error}")

        if warnings:
            click.echo(f"\n⚠️  Avertissements ({len(warnings)}):")
            for warning in warnings:
                click.echo(f"   • {warning}")

        if not errors and not warnings:
            click.echo("\n✅ Aucune erreur ou avertissement détecté !")

        # Code de sortie
        sys.exit(0 if is_valid else 1)

    except Exception as e:
        click.echo(f"❌ Erreur lors de la validation: {e}")
        sys.exit(1)


@cli.command()
@click.argument(
    "project_path", type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
@click.option("--port", "-p", default=8080, help="Port du serveur (défaut: 8080)")
def serve(project_path: str, port: int):
    """
    Lance un serveur web pour visualiser les métriques.

    PROJECT_PATH: Chemin vers le projet à analyser
    """
    try:
        # Collecter les métriques
        collector = MetricsCollector(project_path)
        metrics_data = collector.collect_all_metrics()

        # Exporter le dashboard HTML
        exporter = MetricsExporter(metrics_data)
        dashboard_path = "temp_dashboard.html"
        exporter.export_html_dashboard(dashboard_path)

        click.echo(f"🌐 Dashboard généré: {dashboard_path}")
        click.echo(f"🚀 Ouvrez {dashboard_path} dans votre navigateur")
        click.echo(
            f"💡 Pour un serveur web complet, utilisez: python -m http.server {port}"
        )

    except Exception as e:
        click.echo(f"❌ Erreur lors de la génération du dashboard: {e}")
        sys.exit(1)


if __name__ == "__main__":
    cli()
