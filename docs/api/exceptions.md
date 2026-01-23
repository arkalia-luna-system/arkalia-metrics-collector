# API Reference - Exceptions

Documentation complète des exceptions personnalisées d'**Arkalia Metrics Collector**.

## Vue d'ensemble

Arkalia Metrics Collector utilise une hiérarchie d'exceptions personnalisées pour une meilleure gestion d'erreurs et un debugging facilité.

## Hiérarchie des Exceptions

```
ArkaliaMetricsError (base)
├── CollectionError
│   ├── ProjectNotFoundError
│   └── InvalidProjectPathError
├── ExportError
├── ValidationError
├── GitHubAPIError
│   ├── GitHubRateLimitError
│   └── GitHubAuthenticationError
├── ConfigurationError
└── CoverageParseError
```

## Exceptions de Base

### ArkaliaMetricsError

Exception de base pour toutes les erreurs du collecteur.

```python
from arkalia_metrics_collector import ArkaliaMetricsError

try:
    # Code qui peut lever une exception
    pass
except ArkaliaMetricsError as e:
    print(f"Erreur Arkalia Metrics: {e}")
```

## Exceptions de Collecte

### CollectionError

Erreur lors de la collecte de métriques.

```python
from arkalia_metrics_collector import CollectionError

try:
    collector = MetricsCollector("./projet")
    metrics = collector.collect_all_metrics()
except CollectionError as e:
    print(f"Erreur de collecte: {e}")
```

### ProjectNotFoundError

Erreur lorsque le projet n'est pas trouvé.

```python
from arkalia_metrics_collector import ProjectNotFoundError

try:
    collector = MetricsCollector("/chemin/inexistant")
except ProjectNotFoundError as e:
    print(f"Projet non trouvé: {e}")
```

### InvalidProjectPathError

Erreur lorsque le chemin du projet est invalide.

```python
from arkalia_metrics_collector import InvalidProjectPathError

try:
    collector = MetricsCollector("/chemin/invalide")
except InvalidProjectPathError as e:
    print(f"Chemin invalide: {e}")
```

## Exceptions d'Export

### ExportError

Erreur lors de l'export des métriques.

```python
from arkalia_metrics_collector import ExportError

try:
    exporter = MetricsExporter(metrics)
    exporter.export_json("output.json")
except ExportError as e:
    print(f"Erreur d'export: {e}")
```

## Exceptions de Validation

### ValidationError

Erreur lors de la validation des métriques.

```python
from arkalia_metrics_collector import ValidationError

try:
    validator = MetricsValidator()
    validator.validate_metrics(metrics)
except ValidationError as e:
    print(f"Erreur de validation: {e}")
```

## Exceptions GitHub API

### GitHubAPIError

Erreur lors de l'utilisation de l'API GitHub.

```python
from arkalia_metrics_collector import GitHubAPIError

try:
    collector = GitHubCollector(token)
    metrics = collector.collect_repo_metrics("owner", "repo")
except GitHubAPIError as e:
    print(f"Erreur GitHub API: {e}")
```

### GitHubRateLimitError

Erreur lorsque la limite de taux GitHub est atteinte.

```python
from arkalia_metrics_collector import GitHubRateLimitError

try:
    collector = GitHubCollector(token)
    metrics = collector.collect_repo_metrics("owner", "repo")
except GitHubRateLimitError as e:
    print(f"Limite de taux atteinte: {e}")
    # Attendre avant de réessayer
```

### GitHubAuthenticationError

Erreur d'authentification GitHub.

```python
from arkalia_metrics_collector import GitHubAuthenticationError

try:
    collector = GitHubCollector(token)
    metrics = collector.collect_repo_metrics("owner", "repo")
except GitHubAuthenticationError as e:
    print(f"Erreur d'authentification: {e}")
    # Vérifier le token
```

## Exceptions de Configuration

### ConfigurationError

Erreur de configuration.

```python
from arkalia_metrics_collector import ConfigurationError

try:
    # Code utilisant la configuration
    pass
except ConfigurationError as e:
    print(f"Erreur de configuration: {e}")
```

## Exceptions de Coverage

### CoverageParseError

Erreur lors du parsing du fichier coverage.xml.

```python
from arkalia_metrics_collector import CoverageParseError

try:
    coverage = CoverageParser.parse_coverage_xml("coverage.xml")
except CoverageParseError as e:
    print(f"Erreur de parsing coverage: {e}")
```

## Gestion des Exceptions

### Exemple Complet

```python
from arkalia_metrics_collector import (
    MetricsCollector,
    ProjectNotFoundError,
    InvalidProjectPathError,
    CollectionError,
    GitHubCollector,
    GitHubAPIError,
    GitHubRateLimitError,
    GitHubAuthenticationError,
)

# Collecte de métriques
try:
    collector = MetricsCollector("./mon-projet")
    metrics = collector.collect_all_metrics()
except ProjectNotFoundError:
    print("Le projet n'existe pas")
except InvalidProjectPathError:
    print("Le chemin est invalide")
except CollectionError as e:
    print(f"Erreur lors de la collecte: {e}")

# Collecte GitHub
try:
    github = GitHubCollector(token)
    repo_metrics = github.collect_repo_metrics("owner", "repo")
except GitHubAuthenticationError:
    print("Token GitHub invalide")
except GitHubRateLimitError as e:
    print(f"Limite de taux: {e}")
    # Attendre et réessayer
except GitHubAPIError as e:
    print(f"Erreur API: {e}")
```

## Bonnes Pratiques

1. **Capturer les exceptions spécifiques** : Utilisez les exceptions les plus spécifiques possibles
2. **Gérer les erreurs appropriément** : Différentes exceptions nécessitent différentes actions
3. **Logger les exceptions** : Utilisez `logger.exception()` pour logger avec traceback
4. **Messages d'erreur clairs** : Les exceptions incluent des messages descriptifs

---

**Pour plus d'informations, consultez la [documentation complète](../README.md).**
