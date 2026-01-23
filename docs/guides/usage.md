# Guide d'Utilisation

Guide complet pour utiliser **Arkalia Metrics Collector** avec tous les exemples et cas d'usage.

## Premiers pas

### Collecte basique

```python
from arkalia_metrics_collector import MetricsCollector

# Créer un collecteur
collector = MetricsCollector("./mon-projet")

# Collecter toutes les métriques
metrics = collector.collect_all_metrics()

# Afficher le résumé
print(f"Fichiers Python: {metrics['summary']['total_python_files']}")
print(f"Lignes de code: {metrics['summary']['lines_of_code']}")
print(f"Tests: {metrics['summary']['collected_tests']}")
```

### Collecte sélective

```python
# Collecter seulement les métriques Python
python_metrics = collector.collect_python_metrics()

# Collecter seulement les tests
test_metrics = collector.collect_test_metrics()

# Collecter seulement la documentation
doc_metrics = collector.collect_documentation_metrics()
```

## Configuration

### Exclusion de fichiers

```python
collector = MetricsCollector("./mon-projet")

# Ajouter des patterns d'exclusion
collector.exclude_patterns.add("*.tmp")
collector.exclude_patterns.add("backup/")
```

## Export des métriques

### Export simple

```python
from arkalia_metrics_collector import MetricsExporter

# Créer un exporteur
exporter = MetricsExporter(metrics_data)

# Exporter en différents formats
exporter.export_json("metrics.json")
exporter.export_markdown_summary("metrics.md")
exporter.export_html_dashboard("dashboard.html")
exporter.export_csv("metrics.csv")
exporter.export_yaml("metrics.yaml")
```

### Export en lot

```python
# Exporter dans tous les formats
results = exporter.export_all_formats("output/")

# Vérifier les résultats
for format, success in results.items():
    print(f"{format}: {'✅' if success else '❌'}")
```

## Validation des métriques

### Validation basique

```python
from arkalia_metrics_collector import MetricsValidator

# Créer un validateur
validator = MetricsValidator()

# Valider les métriques
is_valid, errors, warnings = validator.validate_metrics(metrics_data)

if is_valid:
    print("✅ Métriques valides!")
else:
    print(f"❌ {len(errors)} erreurs détectées")
    for error in errors:
        print(f"  - {error}")
```

### Rapport de validation

```python
# Obtenir un rapport détaillé
report = validator.get_validation_report()

print(f"Score: {report['validation_summary']['score']}/100")
print(f"Statut: {report['validation_summary']['status']}")
```

## Interface en ligne de commande

### Collecte

```bash
# Collecte complète
arkalia-metrics collect ./mon-projet

# Collecte avec validation
arkalia-metrics collect ./mon-projet --validate

# Collecte avec export spécifique
arkalia-metrics collect ./mon-projet --format json --output results/

# Export depuis un fichier JSON
arkalia-metrics export metrics.json --format yaml --output exports/

# Export dans tous les formats
arkalia-metrics export metrics.json --format all

# Mode verbeux
arkalia-metrics collect ./mon-projet --verbose
```

### Validation

```bash
# Valider un projet
arkalia-metrics validate ./mon-projet

# Afficher le score de validation
arkalia-metrics validate ./mon-projet --verbose
```

### Serveur web

```bash
# Générer un dashboard HTML
arkalia-metrics serve ./mon-projet

# Spécifier le port
arkalia-metrics serve ./mon-projet --port 9000
```

## Métriques disponibles

### Structure des données

```json
{
  "timestamp": "2025-11-24T00:00:00",
  "project_root": "/chemin/vers/projet",
  "collection_info": {
    "collector_version": "1.1.0",
    "python_version": "3.10.0",
    "collection_date": "2025-11-24T00:00:00"
  },
  "python_files": {
    "count": 25,
    "core_files": 20,
    "test_files": 5,
    "total_lines": 1500
  },
  "test_metrics": {
    "collected_tests_count": 45,
    "test_files_count": 5
  },
  "documentation_metrics": {
    "documentation_files": 3
  },
  "summary": {
    "total_python_files": 25,
    "lines_of_code": 1500,
    "collected_tests": 45,
    "documentation_files": 3
  }
}
```

## Intégration GitHub API

### Collecte des métriques GitHub

```python
from arkalia_metrics_collector import GitHubCollector

# Créer un collecteur GitHub (token optionnel)
collector = GitHubCollector(github_token="YOUR_TOKEN")

# Collecter les métriques d'un dépôt
metrics = collector.collect_repo_metrics("owner", "repo")

if metrics:
    stats = metrics.get("stats", {})
    print(f"⭐ Stars: {stats.get('stars', 0)}")
    print(f"🍴 Forks: {stats.get('forks', 0)}")
    print(f"📝 Open Issues: {stats.get('open_issues', 0)}")
```

### Collecte de plusieurs dépôts

```python
# Collecter plusieurs dépôts
repos = [
    {"owner": "arkalia-luna-system", "repo": "arkalia-metrics-collector"},
    {"owner": "arkalia-luna-system", "repo": "athalia"},
]

aggregated = collector.collect_multiple_repos(repos)
print(f"Total stars: {aggregated['aggregated']['total_stars']}")
```

### Intégration dans l'agrégation multi-projets

```bash
# Activer la collecte GitHub API lors de l'agrégation
arkalia-metrics aggregate projects.json --github-api --json
```

Les métriques GitHub seront automatiquement incluses dans `aggregated_metrics.json`.

## Statistiques de Contribution Git

### Collecte des statistiques Git

```python
from arkalia_metrics_collector import GitContributions

# Créer un collecteur Git
git_collector = GitContributions("/chemin/vers/projet")

# Collecter les statistiques (30 derniers jours par défaut)
contributions = git_collector.collect_contributions(days=30)

if contributions:
    print(f"Total commits: {contributions['total_commits']}")
    print(f"Commits récents (30j): {contributions['recent_commits']}")
    print(f"Lignes ajoutées: {contributions['lines']['added']}")
    print(f"Lignes supprimées: {contributions['lines']['deleted']}")
    print(f"Fichiers modifiés: {contributions['files_changed']}")
    
    # Top contributeurs
    for contrib in contributions['contributors'][:5]:
        print(f"  {contrib['name']}: {contrib['commits']} commits")
```

Les statistiques Git sont automatiquement collectées lors de l'agrégation multi-projets.

## Agrégation Multi-Projets

### Collecte et agrégation

```python
from arkalia_metrics_collector import MultiProjectAggregator

aggregator = MultiProjectAggregator()

# Collecter plusieurs projets
aggregator.collect_project("projet1", "/path/to/project1")
aggregator.collect_project("projet2", "/path/to/project2")

# Agréger les métriques
aggregated = aggregator.aggregate_metrics()

print(f"Total modules: {aggregated['aggregated']['total_modules']}")
print(f"Total lignes: {aggregated['aggregated']['total_lines_of_code']}")
print(f"Coverage global: {aggregated['aggregated']['global_coverage']}%")
```

### Génération de tableau README

```python
# Générer un tableau Markdown pour README
table = aggregator.generate_readme_table()
print(table)
```

### Chargement depuis JSON

```python
# Charger depuis un fichier JSON
aggregator.load_from_json("projects_metrics.json")
aggregated = aggregator.aggregate_metrics()
```

## Export vers formats multiples

### Export depuis fichier JSON

```bash
# Exporter dans tous les formats
arkalia-metrics export metrics.json --format all

# Export spécifique (JSON, Markdown, HTML, CSV, YAML)
arkalia-metrics export metrics.json --format yaml

# Export vers API REST
arkalia-metrics export metrics.json \
  --rest-api https://api.example.com/metrics \
  --api-key YOUR_API_KEY
```

### Export programmatique

```python
from arkalia_metrics_collector import MetricsExporter
from arkalia_metrics_collector.exporters.external_exporters import RESTAPIExporter

# Charger les métriques
import json
with open("metrics.json") as f:
    metrics_data = json.load(f)

# Exporter
exporter = MetricsExporter(metrics_data)
exporter.export_yaml("metrics.yaml")

# Export vers API REST
rest_exporter = RESTAPIExporter(
    api_url="https://api.example.com/metrics",
    api_key="YOUR_KEY"
)
rest_exporter.export(metrics_data)
```

## Système d'alertes et notifications

### Vérification des alertes

```bash
# Vérifier les changements significatifs (seuil par défaut: 10%)
arkalia-metrics alerts metrics/aggregated_metrics.json

# Avec seuil personnalisé
arkalia-metrics alerts metrics/aggregated_metrics.json --threshold 15.0
```

### Création automatique d'issues GitHub

```bash
# Créer une issue GitHub si des alertes sont détectées
arkalia-metrics alerts metrics/aggregated_metrics.json \
  --create-issue \
  --github-owner arkalia-luna-system \
  --github-repo arkalia-metrics-collector

# Avec personnalisation
arkalia-metrics alerts metrics/aggregated_metrics.json \
  --create-issue \
  --labels "metrics,automated,alerts" \
  --assignees "user1,user2" \
  --threshold 20.0
```

### Notifications multi-canaux

```bash
# Activer les notifications (Email, Slack, Discord)
arkalia-metrics alerts metrics/aggregated_metrics.json --notify
```

### Configuration des notifications

#### Email (SMTP)

```bash
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USERNAME="your-email@gmail.com"
export SMTP_PASSWORD="your-password"
export SMTP_FROM="your-email@gmail.com"
export SMTP_TO="recipient1@example.com,recipient2@example.com"
```

#### Slack

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

#### Discord

```bash
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/YOUR/WEBHOOK/URL"
```

### Utilisation programmatique

```python
from arkalia_metrics_collector import MetricsAlerts
from arkalia_metrics_collector.notifications import EmailNotifier, SlackNotifier

# Initialiser le système d'alertes
alerts = MetricsAlerts(
    threshold_percent=15.0,
    enable_notifications=True,
    custom_labels=["metrics", "automated"],
    assignees=["user1"]
)

# Vérifier les changements
alerts_data = alerts.check_significant_changes(current_metrics)

if alerts_data.get("has_alerts"):
    # Envoyer les notifications
    results = alerts.send_notifications(alerts_data)
    print(f"Email: {results.get('email', False)}")
    print(f"Slack: {results.get('slack', False)}")
```

## Génération de Badges

### Badges automatiques

```python
from arkalia_metrics_collector import BadgesGenerator, MetricsCollector

# Collecter les métriques
collector = MetricsCollector(".")
metrics = collector.collect_all_metrics()

# Générer les badges
generator = BadgesGenerator()
badges = generator.generate_all_badges(
    metrics,
    github_owner="arkalia-luna-system",
    github_repo="arkalia-metrics-collector",
    pypi_name="arkalia-metrics-collector",
    license_name="MIT",
)

print(badges)
```

### Badges personnalisés

```python
# Badge Shields.io personnalisé
badge_url = generator.generate_shields_badge(
    label="Python Modules",
    message="52,320",
    color="blue",
    logo="python",
)

# Badge Codecov
codecov_badge = generator.generate_codecov_badge(
    owner="arkalia-luna-system",
    repo="arkalia-metrics-collector",
    branch="main",
)

# Badge GitHub Actions
actions_badge = generator.generate_github_actions_badge(
    owner="arkalia-luna-system",
    repo="arkalia-metrics-collector",
    workflow="ci",
)
```

## Cas d'usage avancés

### Intégration CI/CD

```yaml
# .github/workflows/metrics.yml
name: Collect Metrics
on: [push, pull_request]

jobs:
  metrics:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Collect Metrics
        run: |
          pip install arkalia-metrics-collector
          arkalia-metrics collect . --format json --output metrics/
      - name: Upload Metrics
        uses: actions/upload-artifact@v3
        with:
          name: project-metrics
          path: metrics/
```

### Collecte programmée

```python
from arkalia_metrics_collector import MetricsCollector, MetricsExporter
from datetime import datetime

def collect_metrics():
    collector = MetricsCollector("./mon-projet")
    metrics = collector.collect_all_metrics()
    
    exporter = MetricsExporter(metrics)
    timestamp = datetime.now().strftime('%Y%m%d')
    exporter.export_json(f"metrics_{timestamp}.json")
```

---

**Pour plus d'informations, consultez la [documentation complète](../README.md) et la [FAQ](../FAQ.md).**
