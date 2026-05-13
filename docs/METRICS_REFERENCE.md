# 📊 Référence Complète des Métriques

Documentation détaillée de toutes les métriques collectées par **Arkalia Metrics Collector**.

## 🎯 Vue d'ensemble

Arkalia Metrics Collector collecte des métriques sur :
- 📁 **Structure du projet** : Fichiers, dossiers, organisation
- 🐍 **Code Python** : Modules, lignes de code, complexité
- 🧪 **Tests** : Nombre, couverture, organisation
- 📚 **Documentation** : Fichiers, types, qualité
- 🔗 **GitHub** : Stars, forks, issues, PRs, releases
- 📈 **Git** : Commits, contributeurs, activité
- 📊 **Agrégation** : Métriques multi-projets

---

## 📁 Métriques de Structure

### Fichiers Python

| Métrique | Description | Exemple |
|----------|-------------|---------|
| `total_python_files` | Nombre total de fichiers `.py` | `150` |
| `core_files` | Fichiers de code (hors tests) | `120` |
| `test_files` | Fichiers de tests | `30` |
| `lines_of_code` | Nombre total de lignes de code | `4500` |
| `empty_lines` | Lignes vides | `450` |
| `comment_lines` | Lignes de commentaires | `300` |

### Organisation

| Métrique | Description |
|----------|-------------|
| `project_structure` | Arborescence des dossiers |
| `main_modules` | Modules principaux identifiés |
| `entry_points` | Points d'entrée détectés |

---

## 🐍 Métriques Python

### Modules

| Métrique | Description |
|----------|-------------|
| `total_modules` | Nombre total de modules Python |
| `imported_modules` | Modules importés |
| `external_dependencies` | Dépendances externes détectées |

### Code

| Métrique | Description | Statut |
|----------|-------------|--------|
| `lines_of_code` | Lignes de code totales | ✅ |
| `functions` | Nombre de fonctions | ⚠️ Partiel |
| `classes` | Nombre de classes | ⚠️ Partiel |
| `complexity` | Complexité cyclomatique | 📋 Prévu |

---

## 🧪 Métriques de Tests

### Détection

| Métrique | Description |
|----------|-------------|
| `collected_tests` | Nombre de tests détectés |
| `test_files` | Fichiers de tests |
| `test_functions` | Fonctions de test |

### Couverture

| Métrique | Description | Source |
|----------|-------------|--------|
| `coverage_percentage` | Pourcentage de couverture | `coverage.xml` |
| `covered_lines` | Lignes couvertes | `coverage.xml` |
| `missing_lines` | Lignes non couvertes | `coverage.xml` |
| `branches_covered` | Branches couvertes | `coverage.xml` |

**Note** : La couverture nécessite un fichier `coverage.xml` généré par `pytest-cov` ou `coverage.py`.

---

## 📚 Métriques de Documentation

### Fichiers

| Métrique | Description |
|----------|-------------|
| `documentation_files` | Nombre de fichiers de documentation |
| `markdown_files` | Fichiers Markdown (`.md`) |
| `rst_files` | Fichiers reStructuredText (`.rst`) |
| `html_files` | Fichiers HTML (`.html`) |

### Qualité

| Métrique | Description | Statut |
|----------|-------------|--------|
| `docstrings` | Nombre de docstrings | 📋 Prévu |
| `docstring_coverage` | Couverture docstrings | 📋 Prévu |

---

## 🔗 Métriques GitHub

### Statistiques de Base

| Métrique | Description |
|----------|-------------|
| `stars` | Nombre d'étoiles |
| `forks` | Nombre de forks |
| `watchers` | Nombre de watchers |
| `open_issues` | Issues ouvertes |
| `closed_issues` | Issues fermées |
| `open_pull_requests` | Pull requests ouvertes |
| `closed_pull_requests` | Pull requests fermées |

### Activité

| Métrique | Description |
|----------|-------------|
| `last_updated` | Dernière mise à jour |
| `created_at` | Date de création |
| `pushed_at` | Dernier push |
| `releases` | Nombre de releases |

**Note** : Nécessite `--github-api` et un token GitHub.

---

## ⚙️ Métriques de Collection

### Informations de Collecte

| Métrique | Description | Statut |
|----------|-------------|--------|
| `collector_version` | Version du collecteur utilisée | ✅ |
| `python_version` | Version Python utilisée | ✅ |
| `collection_date` | Date et heure de la collecte (ISO format) | ✅ |
| `collection_time_seconds` | Temps de collecte en secondes | ✅ |

**Exemple :**
```json
{
  "collection_info": {
    "collector_version": "1.1.1",
    "python_version": "3.10.5",
    "collection_date": "2026-01-23T10:30:00",
    "collection_time_seconds": 2.345
  }
}
```

---

## 📈 Métriques Git

### Commits

| Métrique | Description |
|----------|-------------|
| `total_commits` | Nombre total de commits |
| `commits_last_month` | Commits du dernier mois |
| `commits_last_year` | Commits de la dernière année |

### Contributeurs

| Métrique | Description |
|----------|-------------|
| `contributors` | Nombre de contributeurs |
| `contributors_list` | Liste des contributeurs |
| `top_contributors` | Top contributeurs |

### Activité

| Métrique | Description |
|----------|-------------|
| `lines_added` | Lignes ajoutées |
| `lines_deleted` | Lignes supprimées |
| `files_changed` | Fichiers modifiés |

---

## 📊 Métriques Agrégées

### Multi-Projets

| Métrique | Description |
|----------|-------------|
| `total_projects` | Nombre de projets |
| `total_modules` | Total de modules (tous projets) |
| `total_lines_of_code` | Total de lignes (tous projets) |
| `total_tests` | Total de tests (tous projets) |
| `average_coverage` | Couverture moyenne |
| `total_stars` | Total d'étoiles GitHub |
| `total_forks` | Total de forks GitHub |

### Évolution

| Métrique | Description |
|----------|-------------|
| `delta_modules` | Variation de modules |
| `delta_lines` | Variation de lignes |
| `delta_tests` | Variation de tests |
| `delta_percent` | Pourcentage de variation |

---

## 🎯 Métriques Avancées (À venir)

Ces métriques sont prévues pour les versions futures. Consultez les [issues GitHub](https://github.com/arkalia-luna-system/arkalia-metrics-collector/issues) pour suivre l'avancement.

### Complexité
- Complexité cyclomatique
- Complexité cognitive
- Indice de maintenabilité

### Performance
- ✅ **Temps de collecte** : `collection_time_seconds` dans `collection_info` (implémenté)
- Utilisation mémoire (prévu)
- Taille des exports (prévu)

### Sécurité
- Vulnérabilités détectées
- Problèmes de sécurité
- Audit des dépendances

---

## 📋 Format JSON des Métriques

### Structure Complète

```json
{
  "project": "nom-du-projet",
  "timestamp": "2025-11-24T10:00:00",
  "summary": {
    "total_python_files": 150,
    "lines_of_code": 4500,
    "collected_tests": 30,
    "documentation_files": 25
  },
  "python_metrics": {
    "files": {
      "count": 150,
      "core_files": 120,
      "test_files": 30
    },
    "lines": {
      "total": 4500,
      "empty": 450,
      "comments": 300
    }
  },
  "test_metrics": {
    "count": 30,
    "coverage": {
      "percentage": 85.5,
      "covered_lines": 3800,
      "missing_lines": 700
    }
  },
  "documentation_metrics": {
    "files": 25,
    "markdown": 20,
    "rst": 5
  },
  "github_metrics": {
    "stats": {
      "stars": 100,
      "forks": 25,
      "open_issues": 5
    }
  },
  "git_metrics": {
    "commits": {
      "total": 500,
      "last_month": 50
    },
    "contributors": 10
  }
}
```

---

## 🔍 Comment Accéder aux Métriques

### Via CLI

```bash
# Collecte simple
arkalia-metrics collect . --format json

# Avec GitHub API
arkalia-metrics collect . --github-api --format json

# Agrégation multi-projets
arkalia-metrics aggregate projects.json --json
```

### Via Python

```python
from arkalia_metrics_collector import MetricsCollector

collector = MetricsCollector(".")
metrics = collector.collect_all_metrics()

# Accéder aux métriques
print(f"Modules: {metrics['summary']['total_python_files']}")
print(f"Lignes: {metrics['summary']['lines_of_code']}")
print(f"Tests: {metrics['summary']['collected_tests']}")
```

---

## 📊 Métriques Disponibles par Format

| Format | Métriques Disponibles |
|--------|----------------------|
| **JSON** | ✅ Toutes les métriques |
| **Markdown** | ✅ Résumé formaté |
| **HTML** | ✅ Dashboard interactif |
| **CSV** | ✅ Métriques principales |
| **YAML** | ✅ Toutes les métriques |

---

## 🎯 Bonnes Pratiques

### Collecte Efficace
1. **Exclure les dossiers inutiles** : Configurez `arkalia-metrics.yaml`
2. **Utiliser le cache** : Les métriques GitHub sont mises en cache
3. **Collecte incrémentale** : Utilisez l'historique pour comparer

### Interprétation
1. **Métriques relatives** : Comparez avec des projets similaires
2. **Évolution temporelle** : Utilisez l'historique pour suivre les tendances
3. **Seuils personnalisés** : Configurez les alertes selon vos besoins

---

## 📚 Références

- [Guide d'utilisation](guides/usage.md)
- [API Collectors](api/collectors.md)
- [FAQ](FAQ.md)

---

**Version** : 1.1.1 | **Dernière mise à jour** : 23 janvier 2026
