#!/usr/bin/env python3
"""
Arkalia Metrics Collector - Interface en ligne de commande.

Interface CLI principale pour utiliser le collecteur de métriques.
"""

import json
import logging
import sys
import traceback
from pathlib import Path
from typing import Any

import click

# Constantes
DEFAULT_SERVER_PORT = 8080


def _validate_and_normalize_path(project_path: str) -> Path:
    """
    Valide et normalise un chemin de projet.

    Args:
        project_path: Chemin vers le projet

    Returns:
        Path normalisé et validé

    Raises:
        InvalidProjectPathError: Si le chemin est invalide
        ProjectNotFoundError: Si le projet n'existe pas
    """
    normalized_path = Path(project_path).resolve()
    if not normalized_path.exists():
        raise ProjectNotFoundError(f"Le projet n'existe pas: {project_path}")
    if not normalized_path.is_dir():
        raise InvalidProjectPathError(
            f"Le chemin n'est pas un répertoire: {project_path}"
        )
    return normalized_path


# Ajouter le chemin du projet pour les imports
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Logger pour le module CLI
logger = logging.getLogger(__name__)

try:
    from arkalia_metrics_collector import (
        BadgesGenerator,
        GitHubCollector,
        InvalidProjectPathError,
        MetricsCollector,
        MetricsExporter,
        MetricsValidator,
        MultiProjectAggregator,
        ProjectNotFoundError,
    )
    from arkalia_metrics_collector.collectors.github_issues import GitHubIssues
    from arkalia_metrics_collector.collectors.metrics_alerts import MetricsAlerts
except ImportError as e:
    # Utiliser click.echo pour les erreurs d'import
    # car logger pourrait ne pas être configuré
    click.echo(f"❌ Erreur d'import: {e}", err=True)
    click.echo("📍 Assurez-vous que le package est installé correctement.", err=True)
    sys.exit(1)


@click.group()
@click.version_option(version="1.1.1", prog_name="arkalia-metrics")
def cli() -> None:
    """
    Arkalia Metrics Collector - Outil professionnel de métriques Python.

    Collecte des métriques fiables sur vos projets Python en excluant
    automatiquement les venv, cache et dépendances.
    """


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
    type=click.Choice(["json", "markdown", "html", "csv", "yaml", "all"]),
    default="all",
    help="Format d'export (défaut: all)",
)
@click.option("--validate", "-v", is_flag=True, help="Valider les métriques collectées")
@click.option("--verbose", is_flag=True, help="Mode verbeux")
@click.option(
    "--progress",
    is_flag=True,
    help="Afficher une barre de progression pour les opérations longues",
)
def collect(
    project_path: str,
    output: str,
    format: str,  # noqa: A002
    validate: bool,
    verbose: bool,
    progress: bool,
) -> None:
    """
    Collecte les métriques d'un projet Python.

    PROJECT_PATH: Chemin vers le projet à analyser
    """
    if verbose:
        click.echo(f"🔍 Collecte des métriques pour {project_path}...")
        click.echo(f"📁 Dossier de sortie: {output}")
        click.echo(f"📊 Format: {format}")

    try:
        # Validation et normalisation du chemin
        try:
            normalized_path = _validate_and_normalize_path(project_path)
        except (InvalidProjectPathError, ProjectNotFoundError) as e:
            click.echo(f"❌ {e}")
            sys.exit(1)

        # Collecter les métriques
        collector = MetricsCollector(str(normalized_path), show_progress=progress)
        if progress:
            click.echo("📊 Collecte des métriques en cours...")
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
                score = validation_report["validation_summary"]["score"]
                click.echo(f"📊 Score de validation: {score}/100")

        # Exporter les métriques
        exporter = MetricsExporter(metrics_data)

        if format == "all":
            formats_to_export = ["json", "markdown", "html", "csv", "yaml"]
            if progress:
                with click.progressbar(
                    formats_to_export,
                    label="📤 Export des formats",
                    show_eta=True,
                ) as formats:
                    results = {}
                    for fmt in formats:
                        if fmt == "json":
                            results[fmt] = exporter.export_json(
                                f"{output}/metrics.json"
                            )
                        elif fmt == "markdown":
                            results[fmt] = exporter.export_markdown_summary(
                                f"{output}/metrics.md"
                            )
                        elif fmt == "html":
                            results[fmt] = exporter.export_html_dashboard(
                                f"{output}/dashboard.html"
                            )
                        elif fmt == "csv":
                            results[fmt] = exporter.export_csv(f"{output}/metrics.csv")
                        elif fmt == "yaml":
                            results[fmt] = exporter.export_yaml(
                                f"{output}/metrics.yaml"
                            )
            else:
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
            elif format == "yaml":
                success = exporter.export_yaml(f"{output}/metrics.yaml")

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
            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.argument(
    "project_path", type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
def validate(project_path: str) -> None:
    """
    Valide les métriques d'un projet Python.

    PROJECT_PATH: Chemin vers le projet à valider
    """
    try:
        # Validation et normalisation du chemin
        try:
            normalized_path = _validate_and_normalize_path(project_path)
        except (InvalidProjectPathError, ProjectNotFoundError) as e:
            click.echo(f"❌ {e}")
            sys.exit(1)

        # Collecter et valider
        collector = MetricsCollector(str(normalized_path))
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
@click.option(
    "--port",
    "-p",
    default=DEFAULT_SERVER_PORT,
    help=f"Port du serveur (défaut: {DEFAULT_SERVER_PORT})",
)
def serve(project_path: str, port: int) -> None:
    """
    Lance un serveur web pour visualiser les métriques.

    PROJECT_PATH: Chemin vers le projet à analyser
    """
    try:
        # Validation et normalisation du chemin
        try:
            normalized_path = _validate_and_normalize_path(project_path)
        except (InvalidProjectPathError, ProjectNotFoundError) as e:
            click.echo(f"❌ {e}")
            sys.exit(1)

        # Collecter les métriques
        collector = MetricsCollector(str(normalized_path), show_progress=False)
        metrics_data = collector.collect_all_metrics()

        # Exporter le dashboard HTML dans un dossier temporaire
        import tempfile

        temp_dir = Path(tempfile.mkdtemp(prefix="arkalia_metrics_"))
        dashboard_path = temp_dir / "dashboard.html"
        exporter = MetricsExporter(metrics_data)
        exporter.export_html_dashboard(str(dashboard_path))

        click.echo(f"🌐 Dashboard généré: {dashboard_path}")
        click.echo(f"🚀 Ouvrez {dashboard_path} dans votre navigateur")
        click.echo(
            f"💡 Pour un serveur web complet, utilisez: "
            f"cd {temp_dir} && python -m http.server {port}"
        )
        click.echo(f"📁 Dossier temporaire: {temp_dir}")

    except Exception as e:
        click.echo(f"❌ Erreur lors de la génération du dashboard: {e}")
        sys.exit(1)


@cli.command()
@click.argument("owner", required=False)
@click.argument("repo", required=False)
@click.option("--token", "-t", help="Token GitHub (ou variable GITHUB_TOKEN)")
@click.option("--output", "-o", default="metrics", help="Dossier de sortie")
@click.option(
    "--multiple",
    "-m",
    help=(
        "Fichier JSON avec liste de dépôts à collecter "
        '(format: [{"owner": "...", "repo": "..."}])'
    ),
)
@click.option("--verbose", is_flag=True, help="Mode verbeux")
def github(
    owner: str | None,
    repo: str | None,
    token: str | None,
    output: str,
    multiple: str | None,
    verbose: bool,
):
    """
    Collecte les métriques GitHub d'un ou plusieurs dépôts.

    OWNER: Propriétaire du dépôt (organisation ou utilisateur)
    REPO: Nom du dépôt

    Ou utilisez --multiple pour collecter plusieurs dépôts depuis un fichier JSON.
    """
    if multiple:
        # Mode collecte multiple
        if verbose:
            click.echo(f"🔍 Collecte des métriques GitHub depuis {multiple}...")

        try:
            with open(multiple, encoding="utf-8") as f:
                repos_list = json.load(f)

            if not isinstance(repos_list, list):
                click.echo("❌ Le fichier JSON doit contenir une liste de dépôts")
                sys.exit(1)

            collector = GitHubCollector(token)
            metrics = collector.collect_multiple_repos(repos_list)

            if not metrics or not metrics.get("repositories"):
                click.echo("❌ Impossible de collecter les métriques GitHub")
                sys.exit(1)

            # Exporter en JSON
            output_path = Path(output)
            output_path.mkdir(parents=True, exist_ok=True)
            json_file = output_path / "github_multiple_repos.json"

            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(metrics, f, indent=2, ensure_ascii=False)

            if verbose:
                agg = metrics.get("aggregated", {})
                click.echo("✅ Métriques collectées:")
                click.echo(f"   📦 Dépôts: {agg.get('total_repos', 0)}")
                click.echo(f"   ⭐ Total Stars: {agg.get('total_stars', 0):,}")
                click.echo(f"   🍴 Total Forks: {agg.get('total_forks', 0):,}")
                click.echo(f"   👀 Total Watchers: {agg.get('total_watchers', 0):,}")

            click.echo(f"\n💾 Métriques exportées dans: {json_file}")

        except Exception:
            # Ne pas exposer les détails de l'erreur qui pourraient contenir des tokens
            click.echo("❌ Erreur lors de la collecte GitHub")
            if verbose:
                # Logger seulement le type d'erreur, pas le message complet
                logger.debug(
                    "Erreur GitHub (détails masqués pour sécurité)", exc_info=True
                )
            sys.exit(1)
    else:
        # Mode collecte simple
        if not owner or not repo:
            click.echo("❌ OWNER et REPO sont requis (ou utilisez --multiple)")
            click.echo("💡 Utilisez: arkalia-metrics github owner repo")
            sys.exit(1)

        if verbose:
            click.echo(f"🔍 Collecte des métriques GitHub pour {owner}/{repo}...")

        try:
            collector = GitHubCollector(token)
            repo_metrics: dict[str, Any] | None = collector.collect_repo_metrics(
                owner, repo
            )

            if repo_metrics is None:
                click.echo("❌ Impossible de collecter les métriques GitHub")
                click.echo("💡 Vérifiez que le dépôt existe et est accessible")
                sys.exit(1)

            # Exporter en JSON
            output_path = Path(output)
            output_path.mkdir(parents=True, exist_ok=True)
            json_file = output_path / f"github_{owner}_{repo}.json"

            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(repo_metrics, f, indent=2, ensure_ascii=False)

            if verbose:
                stats = repo_metrics.get("stats", {})
                click.echo("✅ Métriques collectées:")
                click.echo(f"   ⭐ Stars: {stats.get('stars', 0):,}")
                click.echo(f"   🍴 Forks: {stats.get('forks', 0):,}")
                click.echo(f"   👀 Watchers: {stats.get('watchers', 0):,}")
                click.echo(f"   📝 Open Issues: {stats.get('open_issues', 0):,}")

            click.echo(f"\n💾 Métriques exportées dans: {json_file}")

        except Exception:
            # Ne pas exposer les détails de l'erreur qui pourraient contenir des tokens
            click.echo("❌ Erreur lors de la collecte GitHub")
            if verbose:
                # Logger seulement le type d'erreur, pas le message complet
                logger.debug(
                    "Erreur GitHub (détails masqués pour sécurité)", exc_info=True
                )
            sys.exit(1)


@cli.command()
@click.argument(
    "projects_file", type=click.Path(exists=True, file_okay=True, dir_okay=False)
)
@click.option("--output", "-o", default="metrics", help="Dossier de sortie")
@click.option("--readme-table", is_flag=True, help="Générer un tableau README")
@click.option("--json", "export_json", is_flag=True, help="Exporter en JSON")
@click.option("--evolution", is_flag=True, help="Générer un rapport d'évolution")
@click.option(
    "--no-history", is_flag=True, help="Désactiver la sauvegarde de l'historique"
)
@click.option(
    "--github-api",
    is_flag=True,
    help="Activer la collecte GitHub API (nécessite GITHUB_TOKEN)",
)
@click.option(
    "--load-from-json",
    is_flag=True,
    help="Charger les métriques depuis un fichier JSON existant au lieu de collecter",
)
@click.option("--verbose", is_flag=True, help="Mode verbeux")
@click.option(
    "--progress",
    is_flag=True,
    help="Afficher une barre de progression pour les opérations longues",
)
def aggregate(
    projects_file: str,
    output: str,
    readme_table: bool,
    export_json: bool,
    evolution: bool,
    no_history: bool,
    github_api: bool,
    load_from_json: bool,
    verbose: bool,
    progress: bool,
):
    """
    Agrège les métriques de plusieurs projets.

    PROJECTS_FILE: Fichier JSON avec la liste des projets
                   Format: {"projects": [{"name": "...", "path": "..."}]}
                   Ou fichier JSON avec métriques déjà collectées si --load-from-json
    """
    if verbose:
        click.echo(f"🔍 Agrégation des métriques depuis {projects_file}...")

    try:
        aggregator = MultiProjectAggregator(
            enable_history=not no_history,
            enable_github=github_api,
            show_progress=progress,
        )

        # Si on charge depuis JSON, utiliser load_from_json
        if load_from_json:
            if verbose:
                click.echo("📂 Chargement des métriques depuis JSON...")
            success = aggregator.load_from_json(projects_file)
            if not success:
                click.echo(
                    "❌ Impossible de charger les métriques depuis le fichier JSON"
                )
                sys.exit(1)
            if verbose:
                click.echo("✅ Métriques chargées avec succès")
        else:
            # Charger la configuration des projets
            with open(projects_file, encoding="utf-8") as f:
                config = json.load(f)

            projects = config.get("projects", [])
            if not projects:
                click.echo("❌ Aucun projet trouvé dans le fichier")
                sys.exit(1)

            # Collecter les métriques de chaque projet
            if progress:
                # Type ignore nécessaire car click.progressbar retourne un type complexe
                project_iter: Any = click.progressbar(
                    projects,
                    label="📦 Collecte des projets",
                    show_eta=True,
                    item_show_func=lambda p: (
                        f"Collecte de {p.get('name', '')}" if p else None
                    ),
                )
                with project_iter as project_list:
                    for project in project_list:
                        name = project.get("name", "")
                        path = project.get("path", "")
                        github_url = project.get("github", "")

                        if not name or not path:
                            continue

                        if verbose:
                            click.echo(f"\n   📦 Collecte de {name}...")
                            if github_api and github_url:
                                click.echo(f"      🔗 GitHub: {github_url}")

                        metrics = aggregator.collect_project(name, path, github_url)
                        if metrics is None:
                            click.echo(f"   ⚠️  Impossible de collecter {name}")
                            continue
            else:
                for project in projects:
                    name = project.get("name", "")
                    path = project.get("path", "")
                    github_url = project.get("github", "")

                    if not name or not path:
                        continue

                    if verbose:
                        click.echo(f"   📦 Collecte de {name}...")
                        if github_api and github_url:
                            click.echo(f"      🔗 GitHub: {github_url}")

                    metrics = aggregator.collect_project(name, path, github_url)
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

        if evolution:
            evolution_file = output_path / "EVOLUTION_REPORT.md"
            evolution_report = aggregator.get_evolution_report()
            evolution_file.write_text(evolution_report, encoding="utf-8")
            click.echo(f"📈 Rapport d'évolution généré dans: {evolution_file}")
            if verbose and aggregator.history:
                # Afficher un résumé
                comparison = aggregator.history.compare_metrics(aggregated)
                if comparison and comparison.get("has_previous"):
                    deltas = comparison.get("deltas", {})
                    click.echo("\n📊 Résumé de l'évolution:")
                    for metric, delta_data in deltas.items():
                        if delta_data.get("delta") is not None:
                            delta = delta_data["delta"]
                            delta_pct = delta_data.get("delta_percent", 0)
                            trend = "📈" if delta > 0 else "📉" if delta < 0 else "➡️"
                            metric_name = metric.replace("_", " ").title()
                            click.echo(
                                f"   {trend} {metric_name}: "
                                f"{delta:+,.0f} ({delta_pct:+.1f}%)"
                            )

    except Exception as e:
        click.echo(f"❌ Erreur lors de l'agrégation: {e}")
        if verbose:
            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.argument(
    "metrics_file", type=click.Path(exists=True, file_okay=True, dir_okay=False)
)
@click.option(
    "--format",
    "-f",
    type=click.Choice(["json", "markdown", "html", "csv", "yaml", "all"]),
    default="all",
    help="Format d'export (défaut: all)",
)
@click.option("--output", "-o", default="metrics", help="Dossier de sortie")
@click.option(
    "--rest-api",
    help="URL de l'API REST pour export (nécessite API_KEY si authentification)",
)
@click.option("--api-key", help="Clé API pour export REST")
@click.option("--verbose", is_flag=True, help="Mode verbeux")
def export(
    metrics_file: str,
    format: str,
    output: str,
    rest_api: str | None,
    api_key: str | None,
    verbose: bool,
):
    """
    Exporte des métriques depuis un fichier JSON dans différents formats.

    METRICS_FILE: Fichier JSON contenant les métriques à exporter
    """
    if verbose:
        click.echo(f"📤 Export des métriques depuis {metrics_file}...")
        click.echo(f"📁 Dossier de sortie: {output}")
        click.echo(f"📊 Format: {format}")

    try:
        # Charger les métriques
        with open(metrics_file, encoding="utf-8") as f:
            metrics_data = json.load(f)

        # Exporter
        exporter = MetricsExporter(metrics_data)

        output_path = Path(output)
        output_path.mkdir(parents=True, exist_ok=True)

        if format == "all":
            results = exporter.export_all_formats(str(output_path))
            if verbose:
                for fmt, success in results.items():
                    status = "✅" if success else "❌"
                    click.echo(
                        f"{status} Export {fmt}: {'Succès' if success else 'Échec'}"
                    )
            click.echo(f"\n💾 Métriques exportées dans: {output_path}")
        else:
            success = False
            if format == "json":
                success = exporter.export_json(str(output_path / "metrics.json"))
            elif format == "markdown":
                success = exporter.export_markdown_summary(
                    str(output_path / "metrics.md")
                )
            elif format == "html":
                success = exporter.export_html_dashboard(
                    str(output_path / "dashboard.html")
                )
            elif format == "csv":
                success = exporter.export_csv(str(output_path / "metrics.csv"))
            elif format == "yaml":
                success = exporter.export_yaml(str(output_path / "metrics.yaml"))

            if verbose:
                status = "✅" if success else "❌"
                click.echo(
                    f"{status} Export {format}: {'Succès' if success else 'Échec'}"
                )

            if success:
                click.echo(f"💾 Métriques exportées dans: {output_path}")

        # Export REST API si demandé
        if rest_api:
            try:
                from arkalia_metrics_collector.exporters.external_exporters import (
                    RESTAPIExporter,
                )

                rest_exporter = RESTAPIExporter(api_url=rest_api, api_key=api_key)
                rest_success = rest_exporter.export(metrics_data)

                if verbose:
                    status = "✅" if rest_success else "❌"
                    result_msg = "Succès" if rest_success else "Échec"
                    click.echo(f"{status} Export REST API: {result_msg}")

                if rest_success:
                    click.echo(f"🌐 Métriques exportées vers: {rest_api}")
                else:
                    click.echo(
                        "⚠️  Échec de l'export REST API. Vérifiez l'URL et les clés API."
                    )
            except Exception as e:
                click.echo(f"❌ Erreur lors de l'export REST API: {e}")
                if verbose:
                    traceback.print_exc()

    except Exception as e:
        click.echo(f"❌ Erreur lors de l'export: {e}")
        if verbose:
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
            traceback.print_exc()
        sys.exit(1)


@cli.command()
@click.argument(
    "metrics_file", type=click.Path(exists=True, file_okay=True, dir_okay=False)
)
@click.option(
    "--threshold",
    "-t",
    default=10.0,
    type=float,
    help="Seuil de changement significatif en % (défaut: 10.0)",
)
@click.option(
    "--create-issue",
    is_flag=True,
    help="Créer une issue GitHub si des alertes sont détectées",
)
@click.option(
    "--notify",
    is_flag=True,
    help="Envoyer des notifications (email, Slack, Discord)",
)
@click.option(
    "--github-owner",
    default="arkalia-luna-system",
    help="Propriétaire du repository GitHub",
)
@click.option(
    "--github-repo",
    default="arkalia-metrics-collector",
    help="Nom du repository GitHub",
)
@click.option(
    "--labels",
    help="Labels personnalisés pour les issues GitHub (séparés par des virgules)",
)
@click.option(
    "--assignees",
    help="Utilisateurs à assigner aux issues GitHub (séparés par des virgules)",
)
@click.option("--verbose", is_flag=True, help="Mode verbeux")
def alerts(
    metrics_file: str,
    threshold: float,
    create_issue: bool,
    notify: bool,
    labels: str | None,
    assignees: str | None,
    github_owner: str,
    github_repo: str,
    verbose: bool,
):
    """
    Vérifie les changements significatifs dans les métriques et génère des alertes.

    METRICS_FILE: Fichier JSON contenant les métriques à analyser
    """
    if verbose:
        click.echo(f"🔍 Analyse des alertes depuis {metrics_file}...")
        click.echo(f"   📊 Seuil: {threshold}%")

    try:
        # Charger les métriques
        with open(metrics_file, encoding="utf-8") as f:
            metrics_data = json.load(f)

        # Parser les labels et assignees
        custom_labels = (
            [label.strip() for label in labels.split(",") if label.strip()]
            if labels
            else None
        )
        assignees_list = (
            [a.strip() for a in assignees.split(",") if a.strip()]
            if assignees
            else None
        )

        # Initialiser le système d'alertes
        alerts_system = MetricsAlerts(
            threshold_percent=threshold,
            enable_notifications=notify,
            custom_labels=custom_labels,
            assignees=assignees_list,
        )

        # Vérifier les changements significatifs
        alerts_data = alerts_system.check_significant_changes(metrics_data)

        if alerts_data.get("has_alerts"):
            click.echo("\n🚨 ALERTES DÉTECTÉES:")
            click.echo("=" * 50)
            click.echo(alerts_system.generate_alert_message(alerts_data))

            # Vérifier si une issue doit être créée
            should_create = alerts_system.should_create_issue(alerts_data)

            if create_issue and should_create:
                if verbose:
                    click.echo("\n📝 Création d'une issue GitHub...")

                issue_body = alerts_system.create_github_issue_body(alerts_data)
                issue_title = "🚨 Alertes Métriques - Changements Significatifs"

                # Vérifier si une issue similaire existe déjà
                github_issues = GitHubIssues()
                existing_issue = github_issues.check_existing_issue(
                    github_owner, github_repo, issue_title
                )

                if existing_issue:
                    issue_num = existing_issue.get("number")
                    click.echo(f"ℹ️  Issue similaire déjà ouverte: #{issue_num}")
                    click.echo(f"   🔗 {existing_issue.get('html_url', '')}")
                    if verbose:
                        click.echo("\n💡 Mise à jour de l'issue existante...")
                        # Pour l'instant, on affiche juste le contenu
                        click.echo("\n📋 Contenu pour mise à jour:")
                        click.echo("-" * 50)
                        click.echo(issue_body)
                else:
                    # Créer une nouvelle issue
                    issue_data = github_issues.create_issue(
                        owner=github_owner,
                        repo=github_repo,
                        title=issue_title,
                        body=issue_body,
                        labels=alerts_system.custom_labels,
                        assignees=alerts_system.assignees,
                    )

                    if issue_data:
                        click.echo(f"✅ Issue créée: #{issue_data.get('number')}")
                        click.echo(f"   🔗 {issue_data.get('html_url', '')}")
                    else:
                        click.echo("❌ Échec de la création de l'issue")
                        click.echo("💡 Vérifiez que GITHUB_TOKEN est défini")
                        if verbose:
                            click.echo("\n📋 Contenu de l'issue:")
                            click.echo("-" * 50)
                            click.echo(issue_body)

            # Envoyer les notifications si activées
            if notify:
                if verbose:
                    click.echo("\n📧 Envoi des notifications...")
                notification_results = alerts_system.send_notifications(alerts_data)
                for channel, success in notification_results.items():
                    status = "✅" if success else "❌"
                    click.echo(f"   {status} {channel.capitalize()}")

            return 1  # Code de sortie pour indiquer des alertes
        else:
            click.echo("✅ Aucune alerte détectée")
            if verbose:
                click.echo(f"   ℹ️  Aucun changement significatif (seuil: {threshold}%)")
            return 0

    except FileNotFoundError:
        click.echo(f"❌ Fichier non trouvé: {metrics_file}")
        sys.exit(1)
    except Exception:
        # Ne pas exposer les détails de l'erreur
        # qui pourraient contenir des informations sensibles
        click.echo("❌ Erreur lors de l'analyse")
        if verbose:
            logger.debug(
                "Erreur lors de l'analyse (détails masqués pour sécurité)",
                exc_info=True,
            )
        sys.exit(1)


if __name__ == "__main__":
    cli()
