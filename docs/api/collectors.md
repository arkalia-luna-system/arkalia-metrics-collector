# 📊 API Reference - Collectors

Documentation complète des collecteurs de métriques d'**Arkalia Metrics Collector**.

## 🎯 Vue d'ensemble

Les collecteurs sont responsables de la collecte des métriques depuis différents sources :
- **MetricsCollector** : Collecte de métriques Python (code, tests, documentation)
- **GitHubCollector** : Collecte de métriques GitHub (stars, forks, issues, PRs)
- **CoverageParser** : Parsing des fichiers coverage.xml
- **MultiProjectAggregator** : Agrégation de métriques multi-projets
- **MetricsHistory** : Gestion de l'historique des métriques
- **MetricsAlerts** : Détection d'alertes et notifications
- **GitHubIssues** : Création et gestion d'issues GitHub
- **GitContributions** : Statistiques Git (commits, lignes, contributeurs)

## 📦 MetricsCollector

Collecteur principal pour les métriques Python.

### Import

```python
from arkalia_metrics_collector import MetricsCollector
```

### Initialisation

```python
collector = MetricsCollector(
    project_root: str | Path,
    exclude_patterns: set[str] | None = None
)
```

### Méthodes principales

#### `collect_all_metrics() -> dict[str, Any]`

Collecte toutes les métriques du projet.

**Retour :** Dictionnaire avec :
- `summary` : Résumé des métriques
- `python_metrics` : Métriques Python (modules, lignes, etc.)
- `test_metrics` : Métriques de tests (nombre, coverage si disponible)
- `documentation_metrics` : Métriques de documentation

**Exemple :**
```python
collector = MetricsCollector("./mon-projet")
metrics = collector.collect_all_metrics()
print(f"Modules: {metrics['summary']['total_python_files']}")
print(f"Lignes: {metrics['summary']['lines_of_code']}")
```

#### `collect_python_metrics() -> dict[str, Any]`

Collecte uniquement les métriques Python.

#### `collect_test_metrics() -> dict[str, Any]`

Collecte les métriques de tests (détection automatique via pytest).

**Note :** Si un fichier `coverage.xml` est trouvé, le coverage est automatiquement inclus.

#### `collect_documentation_metrics() -> dict[str, Any]`

Collecte les métriques de documentation (Markdown, RST, HTML).

---

## 🌐 GitHubCollector

Collecteur de métriques GitHub via l'API.

### Import

```python
from arkalia_metrics_collector import GitHubCollector
```

### Initialisation

```python
collector = GitHubCollector(
    token: str | None = None,  # Token GitHub (ou variable GITHUB_TOKEN)
    cache_dir: str | Path = ".github_cache"
)
```

### Méthodes principales

#### `collect_repository_metrics(owner: str, repo: str) -> dict[str, Any]`

Collecte les métriques d'un dépôt GitHub.

**Retour :**
- `stars` : Nombre d'étoiles
- `forks` : Nombre de forks
- `watchers` : Nombre de watchers
- `open_issues` : Issues ouvertes
- `open_pull_requests` : PRs ouvertes
- `releases` : Nombre de releases
- `last_update` : Dernière mise à jour

**Exemple :**
```python
collector = GitHubCollector(token="ghp_...")
metrics = collector.collect_repository_metrics("arkalia-luna-system", "arkalia-metrics-collector")
print(f"Stars: {metrics['stars']}")
```

#### `collect_issues(owner: str, repo: str) -> list[dict]`

Collecte les issues d'un dépôt.

#### `collect_pull_requests(owner: str, repo: str) -> list[dict]`

Collecte les pull requests d'un dépôt.

---

## 📊 CoverageParser

Parser pour les fichiers coverage.xml (format Cobertura).

### Import

```python
from arkalia_metrics_collector import CoverageParser
```

### Méthodes statiques

#### `parse_coverage_xml(coverage_path: str | Path) -> dict[str, Any] | None`

Parse un fichier coverage.xml et extrait les métriques.

**Retour :**
- `coverage_percentage` : Pourcentage de coverage
- `branch_coverage` : Coverage des branches
- `lines_covered` : Lignes couvertes
- `lines_valid` : Lignes valides
- `branches_covered` : Branches couvertes
- `branches_valid` : Branches valides

**Exemple :**
```python
coverage = CoverageParser.parse_coverage_xml("coverage.xml")
if coverage:
    print(f"Coverage: {coverage['coverage_percentage']}%")
```

#### `find_coverage_file(project_root: str | Path) -> Path | None`

Cherche un fichier coverage.xml dans le projet (racine, htmlcov/, tests/).

#### `get_coverage_for_project(project_root: str | Path) -> dict[str, Any] | None`

Récupère le coverage pour un projet en cherchant coverage.xml automatiquement.

---

## 📈 MultiProjectAggregator

Agrégateur de métriques multi-projets.

### Import

```python
from arkalia_metrics_collector import MultiProjectAggregator
```

### Initialisation

```python
aggregator = MultiProjectAggregator(
    enable_history: bool = True,  # Activer l'historique
    enable_github: bool = False,  # Activer collecte GitHub
    history_dir: str | Path = "metrics/history"
)
```

### Méthodes principales

#### `collect_project(name: str, path: str | Path, github_url: str | None = None) -> None`

Collecte les métriques d'un projet et les ajoute à l'agrégation.

**Paramètres :**
- `name` : Nom du projet
- `path` : Chemin vers le projet
- `github_url` : URL GitHub (optionnel, pour collecte GitHub)

#### `aggregate_metrics() -> dict[str, Any]`

Agrège toutes les métriques collectées.

**Retour :**
- `aggregated` : Métriques agrégées (total_modules, total_lines_of_code, etc.)
- `projects` : Liste des projets avec leurs métriques
- `github_metrics` : Métriques GitHub agrégées (si activé)
- `git_contributions` : Statistiques Git agrégées (si activé)

#### `generate_readme_table() -> str`

Génère un tableau Markdown pour README avec les métriques par projet.

#### `export_aggregated_json(output_path: str | Path) -> None`

Exporte les métriques agrégées en JSON.

#### `get_evolution_report() -> str | None`

Génère un rapport d'évolution Markdown (nécessite l'historique).

---

## 📅 MetricsHistory

Gestion de l'historique des métriques agrégées.

### Import

```python
from arkalia_metrics_collector import MetricsHistory
```

### Initialisation

```python
history = MetricsHistory(history_dir: str | Path = "metrics/history")
```

### Méthodes principales

#### `save_metrics(metrics: dict[str, Any]) -> None`

Sauvegarde les métriques avec un timestamp.

#### `get_latest_metrics() -> dict[str, Any] | None`

Récupère les dernières métriques sauvegardées.

#### `compare_metrics(current: dict, previous: dict) -> dict[str, Any]`

Compare les métriques actuelles avec les précédentes.

**Retour :**
- `deltas` : Différences absolues
- `percentages` : Différences en pourcentage
- `has_changes` : True si changements détectés

#### `generate_evolution_report() -> str | None`

Génère un rapport d'évolution Markdown.

---

## 🚨 MetricsAlerts

Détection d'alertes et notifications.

### Import

```python
from arkalia_metrics_collector import MetricsAlerts
```

### Initialisation

```python
alerts = MetricsAlerts(
    threshold_percent: float = 10.0,  # Seuil de changement (10%)
    enable_notifications: bool = False,
    custom_labels: list[str] | None = None,
    assignees: list[str] | None = None,
    history_dir: str | Path = "metrics/history"
)
```

### Méthodes principales

#### `check_significant_changes(current_metrics: dict[str, Any]) -> dict[str, Any]`

Vérifie les changements significatifs.

**Retour :**
- `has_alerts` : True si alertes détectées
- `alerts` : Liste des alertes
- `message` : Message formaté

#### `generate_alert_message(alerts: list[dict]) -> str`

Génère un message d'alerte formaté.

#### `create_github_issue_body(alerts: list[dict]) -> str`

Génère le corps d'une issue GitHub.

#### `send_notifications(alerts_data: dict[str, Any]) -> dict[str, bool]`

Envoie les notifications (Email, Slack, Discord).

---

## 🔧 GitHubIssues

Création et gestion d'issues GitHub.

### Import

```python
from arkalia_metrics_collector.collectors.github_issues import GitHubIssues
```

### Initialisation

```python
issues = GitHubIssues(
    owner: str,
    repo: str,
    token: str | None = None
)
```

### Méthodes principales

#### `create_issue(title: str, body: str, labels: list[str] | None = None, assignees: list[str] | None = None) -> dict | None`

Crée une issue GitHub.

#### `check_existing_issues(title_pattern: str) -> list[dict]`

Vérifie les issues existantes correspondant à un pattern.

---

## 📊 GitContributions

Statistiques Git (commits, lignes, contributeurs).

### Import

```python
from arkalia_metrics_collector import GitContributions
```

### Initialisation

```python
contributions = GitContributions(project_root: str | Path)
```

### Méthodes principales

#### `collect_contributions() -> dict[str, Any]`

Collecte les statistiques Git.

**Retour :**
- `total_commits` : Nombre total de commits
- `recent_commits` : Commits récents (30 jours)
- `lines_added` : Lignes ajoutées
- `lines_deleted` : Lignes supprimées
- `files_changed` : Fichiers modifiés
- `top_contributors` : Top contributeurs

---

## 💡 Exemples d'utilisation

### Collecte complète avec coverage

```python
from arkalia_metrics_collector import MetricsCollector, CoverageParser

collector = MetricsCollector("./mon-projet")
metrics = collector.collect_all_metrics()

# Coverage automatique si coverage.xml existe
coverage = CoverageParser.get_coverage_for_project("./mon-projet")
if coverage:
    metrics['test_metrics']['coverage_percentage'] = coverage['coverage_percentage']
```

### Agrégation multi-projets avec GitHub

```python
from arkalia_metrics_collector import MultiProjectAggregator

aggregator = MultiProjectAggregator(enable_github=True)

aggregator.collect_project(
    "projet1",
    "/path/to/project1",
    github_url="https://github.com/owner/project1"
)

aggregated = aggregator.aggregate_metrics()
print(f"Total modules: {aggregated['aggregated']['total_modules']}")
```

### Système d'alertes

```python
from arkalia_metrics_collector import MetricsAlerts

alerts = MetricsAlerts(
    threshold_percent=15.0,
    enable_notifications=True,
    custom_labels=["metrics", "automated"]
)

alerts_data = alerts.check_significant_changes(current_metrics)
if alerts_data.get("has_alerts"):
    alerts.send_notifications(alerts_data)
```

---

**📚 [Retour à l'API](../index.md) | [Exporters](exporters.md) | [Validators](validators.md)**
