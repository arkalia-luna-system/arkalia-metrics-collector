# 📤 API Reference - Exporters

Documentation complète des exporteurs de métriques d'**Arkalia Metrics Collector**.

## 🎯 Vue d'ensemble

Les exporteurs permettent d'exporter les métriques dans différents formats :
- **MetricsExporter** : Export multi-format (JSON, Markdown, HTML, CSV, YAML)
- **BadgesGenerator** : Génération de badges automatiques
- **InteractiveDashboardGenerator** : Dashboard interactif HTML
- **RESTAPIExporter** : Export vers API REST
- **GoogleSheetsExporter** : Export vers Google Sheets (structure prête)
- **NotionExporter** : Export vers Notion (structure prête)
- **AirtableExporter** : Export vers Airtable (structure prête)

## 📦 MetricsExporter

Exporteur principal pour tous les formats.

### Import

```python
from arkalia_metrics_collector import MetricsExporter
```

### Initialisation

```python
exporter = MetricsExporter(metrics_data: dict[str, Any])
```

### Méthodes d'export

#### `export_json(output_path: str | Path) -> bool`

Exporte les métriques en JSON.

**Exemple :**
```python
exporter.export_json("metrics.json")
```

#### `export_markdown_summary(output_path: str | Path) -> bool`

Exporte un résumé Markdown formaté.

#### `export_html_dashboard(output_path: str | Path) -> bool`

Exporte un dashboard HTML interactif.

**Note :** Utilise automatiquement `InteractiveDashboardGenerator` si les métriques sont agrégées.

#### `export_csv(output_path: str | Path) -> bool`

Exporte les métriques en CSV.

#### `export_yaml(output_path: str | Path) -> bool`

Exporte les métriques en YAML.

**Note :** Nécessite PyYAML (`pip install pyyaml`). Si PyYAML n'est pas installé, retourne False avec un message d'avertissement.

**Exemple :**
```python
exporter.export_yaml("metrics.yaml")
```

#### `export_all_formats(output_dir: str | Path) -> dict[str, bool]`

Exporte dans tous les formats disponibles.

**Retour :** Dictionnaire avec le statut de chaque format :
```python
{
    'json': True,
    'markdown': True,
    'html': True,
    'csv': True,
    'yaml': True
}
```

**Exemple :**
```python
results = exporter.export_all_formats("output/")
for format, success in results.items():
    print(f"{format}: {'✅' if success else '❌'}")
```

---

## 🏷️ BadgesGenerator

Générateur de badges automatiques.

### Import

```python
from arkalia_metrics_collector import BadgesGenerator
```

### Initialisation

```python
generator = BadgesGenerator()
```

### Méthodes statiques

#### `generate_shields_badge(label: str, message: str, color: str = "blue", style: str = "flat", logo: str | None = None) -> str`

Génère un badge Shields.io.

**Exemple :**
```python
badge_url = generator.generate_shields_badge(
    label="Python Modules",
    message="52,320",
    color="blue",
    logo="python"
)
```

#### `generate_codecov_badge(owner: str, repo: str, branch: str = "main") -> str`

Génère un badge Codecov.

#### `generate_github_actions_badge(owner: str, repo: str, workflow: str = "ci") -> str`

Génère un badge GitHub Actions.

#### `generate_pypi_badge(package_name: str) -> str`

Génère un badge PyPI.

### Méthodes d'instance

#### `generate_metrics_badges(metrics: dict[str, Any], github_owner: str | None = None, github_repo: str | None = None) -> str`

Génère tous les badges de métriques (modules, LOC, tests, coverage, CI, Codecov).

#### `generate_status_badges(github_owner: str | None = None, github_repo: str | None = None, pypi_name: str | None = None, license_name: str = "MIT") -> str`

Génère les badges de statut (license, Python, stars, PyPI).

#### `generate_all_badges(metrics: dict[str, Any], github_owner: str | None = None, github_repo: str | None = None, pypi_name: str | None = None, license_name: str = "MIT") -> str`

Génère tous les badges (statut + métriques).

---

## 🎨 InteractiveDashboardGenerator

Générateur de dashboard interactif HTML.

### Import

```python
from arkalia_metrics_collector.exporters.interactive_dashboard import InteractiveDashboardGenerator
```

### Initialisation

```python
generator = InteractiveDashboardGenerator()
```

### Méthodes principales

#### `generate(metrics: dict[str, Any], output_path: str | Path, historical_data: list[dict] | None = None) -> None`

Génère un dashboard HTML interactif.

**Paramètres :**
- `metrics` : Métriques à visualiser (simple ou agrégées)
- `output_path` : Chemin de sortie
- `historical_data` : Données historiques pour graphiques d'évolution (optionnel)

**Fonctionnalités :**
- 📊 Graphiques Chart.js (modules, lignes, tests, overview)
- 📈 Graphiques d'évolution temporelle (si historique disponible)
- 🔍 Tableaux interactifs avec tri et filtrage
- 📤 Export JSON/CSV
- 📱 Interface responsive

**Exemple :**
```python
from arkalia_metrics_collector.exporters.interactive_dashboard import InteractiveDashboardGenerator

generator = InteractiveDashboardGenerator()
generator.generate(metrics, "dashboard.html", historical_data=history)
```

---

## 🌐 RESTAPIExporter

Exporteur vers API REST.

### Import

```python
from arkalia_metrics_collector.exporters.external_exporters import RESTAPIExporter
```

### Initialisation

```python
exporter = RESTAPIExporter(
    api_url: str,
    api_key: str | None = None,
    headers: dict[str, str] | None = None
)
```

### Méthodes principales

#### `export(metrics: dict[str, Any]) -> bool`

Exporte les métriques vers l'API REST.

**Exemple :**
```python
exporter = RESTAPIExporter(
    api_url="https://api.example.com/metrics",
    api_key="YOUR_API_KEY"
)
success = exporter.export(metrics)
```

---

## 📊 Exporteurs Externes (Structure Prête)

Les exporteurs suivants ont une structure prête mais nécessitent l'implémentation complète des méthodes `export()` :

### GoogleSheetsExporter

```python
from arkalia_metrics_collector.exporters.external_exporters import GoogleSheetsExporter

exporter = GoogleSheetsExporter(
    spreadsheet_id: str,
    credentials_path: str | None = None
)
# exporter.export(metrics)  # À implémenter
```

### NotionExporter

```python
from arkalia_metrics_collector.exporters.external_exporters import NotionExporter

exporter = NotionExporter(
    notion_token: str,
    database_id: str
)
# exporter.export(metrics)  # À implémenter
```

### AirtableExporter

```python
from arkalia_metrics_collector.exporters.external_exporters import AirtableExporter

exporter = AirtableExporter(
    base_id: str,
    table_name: str,
    api_key: str
)
# exporter.export(metrics)  # À implémenter
```

**Note :** Ces exporteurs sont prêts pour l'implémentation. Voir [CONTRIBUTING.md](../CONTRIBUTING.md) pour contribuer.

---

## 💡 Exemples d'utilisation

### Export complet

```python
from arkalia_metrics_collector import MetricsExporter

exporter = MetricsExporter(metrics)

# Export individuel
exporter.export_json("metrics.json")
exporter.export_yaml("metrics.yaml")

# Export tous formats
results = exporter.export_all_formats("output/")
```

### Export avec dashboard interactif

```python
from arkalia_metrics_collector import MetricsExporter

exporter = MetricsExporter(aggregated_metrics)
exporter.export_html_dashboard("dashboard.html")
# Génère automatiquement un dashboard interactif si métriques agrégées
```

### Export vers API REST

```python
from arkalia_metrics_collector.exporters.external_exporters import RESTAPIExporter

exporter = RESTAPIExporter(
    api_url="https://api.example.com/metrics",
    api_key="YOUR_KEY"
)
exporter.export(metrics)
```

### Génération de badges

```python
from arkalia_metrics_collector import BadgesGenerator, MetricsCollector

collector = MetricsCollector(".")
metrics = collector.collect_all_metrics()

generator = BadgesGenerator()
badges = generator.generate_all_badges(
    metrics,
    github_owner="arkalia-luna-system",
    github_repo="arkalia-metrics-collector",
    pypi_name="arkalia-metrics-collector"
)

print(badges)
```

### Utilisation via CLI

```bash
# Export depuis fichier JSON
arkalia-metrics export metrics.json --format yaml

# Export tous formats
arkalia-metrics export metrics.json --format all --output exports/

# Export vers API REST
arkalia-metrics export metrics.json \
  --rest-api https://api.example.com/metrics \
  --api-key YOUR_KEY
```

---

## 📋 Formats de sortie

### JSON
- Structure complète des métriques
- Format standard et lisible
- Facile à parser programmatiquement

### Markdown
- Résumé formaté pour documentation
- Tableaux et sections organisées
- Compatible GitHub/GitLab

### HTML
- Dashboard interactif avec Chart.js
- Graphiques d'évolution
- Tableaux interactifs
- Export JSON/CSV intégré

### CSV
- Format tabulaire
- Compatible Excel/Google Sheets
- Facile à analyser

### YAML
- Format lisible et structuré
- Compatible avec outils DevOps
- Nécessite PyYAML

---

**📚 [Retour à l'API](../index.md) | [Collectors](collectors.md) | [Validators](validators.md)**
