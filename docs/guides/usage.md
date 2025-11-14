# 📖 Utilisation

**Guide complet d'utilisation d'Arkalia Metrics Collector**

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
```

### Export en lot

```python
# Exporter dans tous les formats
results = exporter.export_all_formats("output/")

# Vérifier les résultats
for format, success in results.items():
    print(f"{format}: {'✅' if success else '❌'}")
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
    "collector_version": "1.0.0",
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
    message="550+",
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
