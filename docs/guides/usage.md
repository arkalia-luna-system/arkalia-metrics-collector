# 📖 Guide d'Utilisation

Guide complet pour utiliser **Arkalia Metrics Collector** avec tous les exemples et cas d'usage.

## 🚀 Premiers pas

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

## 🔧 Configuration

### Exclusion de fichiers

```python
collector = MetricsCollector("./mon-projet")

# Ajouter des patterns d'exclusion
collector.exclude_patterns.add("*.tmp")
collector.exclude_patterns.add("backup/")

# Vérifier l'exclusion
is_excluded = collector._is_excluded(Path("./backup/file.py"))
```

## 📤 Export des métriques

### Export simple

```python
from arkalia_metrics_collector import MetricsExporter

# Créer un exporteur
exporter = MetricsExporter(metrics_data)

# Exporter en JSON
exporter.export_json("metrics.json")

# Exporter en Markdown
exporter.export_markdown_summary("metrics.md")

# Exporter en HTML
exporter.export_html_dashboard("dashboard.html")

# Exporter en CSV
exporter.export_csv("metrics.csv")

# Exporter en YAML
exporter.export_yaml("metrics.yaml")
```

### Export en lot

```python
# Exporter dans tous les formats (JSON, Markdown, HTML, CSV, YAML)
results = exporter.export_all_formats("output/")

# Vérifier les résultats
for format, success in results.items():
    print(f"{format}: {'✅' if success else '❌'}")
# Résultat: {'json': True, 'markdown': True, 'html': True, 'csv': True, 'yaml': True}
```

## ✅ Validation des métriques

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

## 🖥️ Interface en ligne de commande

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

## 🔍 Métriques disponibles

### Structure des données

```json
{
  "timestamp": "2024-01-01T00:00:00",
  "project_root": "/chemin/vers/projet",
  "collection_info": {
    "collector_version": "1.1.0",
    "python_version": "3.10.0",
    "collection_date": "2024-01-01T00:00:00"
  },
  "python_files": {
    "count": 25,
    "core_files": 20,
    "test_files": 5,
    "total_lines": 1500,
    "files_list": ["main.py", "utils.py", ...]
  },
  "test_metrics": {
    "collected_tests_count": 45,
    "test_files_count": 5,
    "test_files": ["test_main.py", ...]
  },
  "documentation_metrics": {
    "documentation_files": 3,
    "documentation_list": ["README.md", "docs/", ...]
  },
  "summary": {
    "total_python_files": 25,
    "lines_of_code": 1500,
    "collected_tests": 45,
    "documentation_files": 3
  }
}
```

## 🌐 Tests sur Projets Externes

### Collecte sur Projets Réels

```bash
# Analyser un projet externe
arkalia-metrics collect /path/to/external-project --validate

# Générer tous les formats
arkalia-metrics collect /path/to/external-project --format all --output reports/

# Mode verbeux pour debug
arkalia-metrics collect /path/to/external-project --verbose
```

### Validation des Métriques

```bash
# Validation complète
arkalia-metrics validate /path/to/project

# Validation avec rapport détaillé
arkalia-metrics validate /path/to/project --verbose
```

### Serveur de Visualisation

```bash
# Lancer le serveur de dashboard
arkalia-metrics serve /path/to/project --port 8080

# Ouvrir http://localhost:8080 dans le navigateur
```

## 🧪 Tests et Validation

### Tests Automatisés

```bash
# Exécuter tous les tests
pytest tests/ -v

# Tests spécifiques
pytest tests/integration/test_external_projects.py -v
pytest tests/performance/test_performance_metrics.py -v
pytest tests/unit/cli/test_cli_main.py -v
```

### Validation de Qualité

```bash
# Vérification complète
ruff check .
black --check .
mypy src/
bandit -r src/
```

## 🎯 Cas d'usage avancés

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

### Surveillance continue

```python
import schedule
import time
from arkalia_metrics_collector import MetricsCollector, MetricsExporter

def collect_daily_metrics():
    collector = MetricsCollector("./mon-projet")
    metrics = collector.collect_all_metrics()
    
    exporter = MetricsExporter(metrics)
    exporter.export_json(f"metrics_{time.strftime('%Y%m%d')}.json")

# Planifier la collecte quotidienne
schedule.every().day.at("09:00").do(collect_daily_metrics)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## 🔗 Intégration GitHub API

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
    print(f"👀 Watchers: {stats.get('watchers', 0)}")
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

Les métriques GitHub seront automatiquement incluses dans `aggregated_metrics.json` :
- `github_metrics.total_stars` : Total des stars
- `github_metrics.total_forks` : Total des forks
- `github_metrics.total_watchers` : Total des watchers
- `github_metrics.total_open_issues` : Total des issues ouvertes

## 📊 Statistiques de Contribution Git

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

### Intégration automatique

Les statistiques Git sont automatiquement collectées lors de l'agrégation multi-projets et incluses dans `aggregated_metrics.json` :
- `git_contributions.total_commits` : Total des commits
- `git_contributions.recent_commits_30d` : Commits des 30 derniers jours
- `git_contributions.lines.added` : Lignes ajoutées
- `git_contributions.lines.deleted` : Lignes supprimées
- `git_contributions.top_contributors` : Top 10 contributeurs

## 📈 Agrégation Multi-Projets

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
```

### Génération de tableau README

```python
# Générer un tableau Markdown pour README
table = aggregator.generate_readme_table()
print(table)
```

## 📤 Export vers formats multiples

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

# Charger les métriques
import json
with open("metrics.json") as f:
    metrics_data = json.load(f)

# Exporter
exporter = MetricsExporter(metrics_data)

# Export YAML
exporter.export_yaml("metrics.yaml")

# Export vers API REST
from arkalia_metrics_collector.exporters.external_exporters import RESTAPIExporter
rest_exporter = RESTAPIExporter(
    api_url="https://api.example.com/metrics",
    api_key="YOUR_KEY"
)
rest_exporter.export(metrics_data)
```

## 🚨 Système d'alertes et notifications

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
  --labels "metrics,automated,alerts,urgent" \
  --assignees "user1,user2" \
  --threshold 20.0
```

### Notifications multi-canaux

```bash
# Activer les notifications (Email, Slack, Discord)
arkalia-metrics alerts metrics/aggregated_metrics.json --notify

# Avec création d'issue
arkalia-metrics alerts metrics/aggregated_metrics.json \
  --notify \
  --create-issue
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

## 📈 Agrégation Multi-Projets

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

## 🏷️ Génération de Badges

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
