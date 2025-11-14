#!/usr/bin/env python3
"""
Arkalia Metrics Collector - Interface en ligne de commande.

Interface CLI principale pour utiliser le collecteur de métriques.
"""

import sys
from pathlib import Path

import click

# Ajouter le chemin du projet pour les imports
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from arkalia_metrics_collector import (
        BadgesGenerator,
        GitHubCollector,
        MetricsCollector,
        MetricsExporter,
        MetricsValidator,
        MultiProjectAggregator,
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


@cli.command()
@click.argument("owner")
@click.argument("repo")
@click.option("--token", "-t", help="Token GitHub (ou variable GITHUB_TOKEN)")
@click.option("--output", "-o", default="metrics", help="Dossier de sortie")
@click.option("--verbose", is_flag=True, help="Mode verbeux")
def github(owner: str, repo: str, token: str | None, output: str, verbose: bool):
    """
    Collecte les métriques GitHub d'un dépôt.

    OWNER: Propriétaire du dépôt (organisation ou utilisateur)
    REPO: Nom du dépôt
    """
    if verbose:
        click.echo(f"🔍 Collecte des métriques GitHub pour {owner}/{repo}...")

    try:
        collector = GitHubCollector(token)
        metrics = collector.collect_repo_metrics(owner, repo)

        if metrics is None:
            click.echo("❌ Impossible de collecter les métriques GitHub")
            click.echo("💡 Vérifiez que le dépôt existe et est accessible")
            sys.exit(1)

        # Exporter en JSON
        output_path = Path(output)
        output_path.mkdir(parents=True, exist_ok=True)
        json_file = output_path / f"github_{owner}_{repo}.json"

        import json

        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2, ensure_ascii=False)

        if verbose:
            stats = metrics.get("stats", {})
            click.echo("✅ Métriques collectées:")
            click.echo(f"   ⭐ Stars: {stats.get('stars', 0):,}")
            click.echo(f"   🍴 Forks: {stats.get('forks', 0):,}")
            click.echo(f"   👀 Watchers: {stats.get('watchers', 0):,}")
            click.echo(f"   📝 Open Issues: {stats.get('open_issues', 0):,}")

        click.echo(f"\n💾 Métriques exportées dans: {json_file}")

    except Exception as e:
        click.echo(f"❌ Erreur lors de la collecte GitHub: {e}")
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.argument(
    "projects_file", type=click.Path(exists=True, file_okay=True, dir_okay=False)
)
@click.option("--output", "-o", default="metrics", help="Dossier de sortie")
@click.option("--readme-table", is_flag=True, help="Générer un tableau README")
@click.option("--json", "export_json", is_flag=True, help="Exporter en JSON")
@click.option("--verbose", is_flag=True, help="Mode verbeux")
def aggregate(
    projects_file: str,
    output: str,
    readme_table: bool,
    export_json: bool,
    verbose: bool,
):
    """
    Agrège les métriques de plusieurs projets.

    PROJECTS_FILE: Fichier JSON avec la liste des projets
                   Format: {"projects": [{"name": "...", "path": "..."}]}
    """
    if verbose:
        click.echo(f"🔍 Agrégation des métriques depuis {projects_file}...")

    try:
        import json

        # Charger la configuration des projets
        with open(projects_file, encoding="utf-8") as f:
            config = json.load(f)

        projects = config.get("projects", [])
        if not projects:
            click.echo("❌ Aucun projet trouvé dans le fichier")
            sys.exit(1)

        aggregator = MultiProjectAggregator()

        # Collecter les métriques de chaque projet
        for project in projects:
            name = project.get("name", "")
            path = project.get("path", "")

            if not name or not path:
                continue

            if verbose:
                click.echo(f"   📦 Collecte de {name}...")

            metrics = aggregator.collect_project(name, path)
            if metrics is None:
                click.echo(f"   ⚠️  Impossible de collecter {name}")
                continue

        # Agréger les métriques
        aggregated = aggregator.aggregate_metrics()
        agg_data = aggregated.get("aggregated", {})

        if verbose:
            click.echo("\n✅ Métriques agrégées:")
            click.echo(f"   📦 Projets: {agg_data.get('total_projects', 0)}")
            click.echo(f"   🐍 Modules: {agg_data.get('total_modules', 0):,}")
            click.echo(f"   📝 Lignes: {agg_data.get('total_lines_of_code', 0):,}")
            click.echo(f"   🧪 Tests: {agg_data.get('total_tests', 0):,}")

        # Exporter
        output_path = Path(output)
        output_path.mkdir(parents=True, exist_ok=True)

        if export_json:
            json_file = output_path / "aggregated_metrics.json"
            aggregator.export_aggregated_json(json_file)
            click.echo(f"\n💾 Métriques agrégées exportées dans: {json_file}")

        if readme_table:
            table = aggregator.generate_readme_table()
            table_file = output_path / "README_TABLE.md"
            with open(table_file, "w", encoding="utf-8") as f:
                f.write(table)
            click.echo(f"📊 Tableau README généré dans: {table_file}")

    except Exception as e:
        click.echo(f"❌ Erreur lors de l'agrégation: {e}")
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.argument(
    "metrics_file", type=click.Path(exists=True, file_okay=True, dir_okay=False)
)
@click.option("--output", "-o", default="badges.md", help="Fichier de sortie")
@click.option("--github-owner", help="Propriétaire GitHub")
@click.option("--github-repo", help="Dépôt GitHub")
@click.option("--pypi-name", help="Nom du package PyPI")
@click.option("--license", "license_name", default="MIT", help="Nom de la licence")
@click.option("--verbose", is_flag=True, help="Mode verbeux")
def badges(
    metrics_file: str,
    output: str,
    github_owner: str | None,
    github_repo: str | None,
    pypi_name: str | None,
    license_name: str,
    verbose: bool,
):
    """
    Génère des badges automatiques pour README.

    METRICS_FILE: Fichier JSON avec les métriques du projet
    """
    if verbose:
        click.echo(f"🎨 Génération des badges depuis {metrics_file}...")

    try:
        import json

        with open(metrics_file, encoding="utf-8") as f:
            metrics = json.load(f)

        generator = BadgesGenerator()
        badges_content = generator.generate_all_badges(
            metrics,
            github_owner,
            github_repo,
            pypi_name,
            license_name,
        )

        with open(output, "w", encoding="utf-8") as f:
            f.write(badges_content)

        if verbose:
            click.echo("✅ Badges générés:")
            click.echo("   📊 Badges de métriques")
            click.echo("   🏷️  Badges de statut")

        click.echo(f"\n💾 Badges exportés dans: {output}")

    except Exception as e:
        click.echo(f"❌ Erreur lors de la génération des badges: {e}")
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    cli()
