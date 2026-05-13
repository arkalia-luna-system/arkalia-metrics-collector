# Arkalia Metrics Collector 🚀

> **Collecteur de métriques universel et professionnel pour projets Python**  
> Analyse automatique de code, tests, documentation, coverage, et métriques GitHub. Export multi-format (JSON, Markdown, HTML, CSV, YAML), dashboard interactif, agrégation multi-projets, et intégration CI/CD complète.

![License](https://img.shields.io/badge/License-MIT-blue?style=flat)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat&logo=python)
[![Stars](https://img.shields.io/github/stars/arkalia-luna-system/arkalia-metrics-collector?style=flat&logo=github)](https://github.com/arkalia-luna-system/arkalia-metrics-collector)
[![PyPI](https://img.shields.io/pypi/v/arkalia-metrics-collector?logo=pypi&logoColor=white)](https://pypi.org/project/arkalia-metrics-collector/)

[![Modules](https://img.shields.io/badge/Python%20Modules-52,320-blue?style=flat&logo=python)](https://github.com/arkalia-luna-system/arkalia-metrics-collector)
[![LOC](https://img.shields.io/badge/Lines%20of%20Code-24,790,076-green?style=flat)](https://github.com/arkalia-luna-system/arkalia-metrics-collector)
[![Tests](https://img.shields.io/badge/Tests-11,204-purple?style=flat)](https://github.com/arkalia-luna-system/arkalia-metrics-collector)
[![CI](https://github.com/arkalia-luna-system/arkalia-metrics-collector/actions/workflows/ci-matrix.yml/badge.svg)](https://github.com/arkalia-luna-system/arkalia-metrics-collector/actions)
[![Codecov](https://codecov.io/gh/arkalia-luna-system/arkalia-metrics-collector/branch/main/graph/badge.svg)](https://codecov.io/gh/arkalia-luna-system/arkalia-metrics-collector)

## 📋 Description

**Arkalia Metrics Collector** est un outil professionnel pour collecter, analyser et visualiser les métriques de vos projets Python. Il offre une analyse automatique du code source, des tests, de la documentation, du coverage, et des métriques GitHub, avec export multi-format et dashboard interactif.

## Métriques du Projet

<div align="center">

| Composant | Valeur | Statut |
|:---------|:------:|:------:|
| Fichiers Python | 23 modules | Actif |
| Lignes de Code | 5,841 lignes | Maintenu |
| Tests | 120 tests | Testé |
| Documentation | 56 fichiers | Complet |

</div>

*Dernière mise à jour : 23 janvier 2026*

## 📊 Métriques Globales

<div align="center">

| **Projet** | **Modules** | **Lignes** | **Tests** |
|:-----------|:-----------:|:----------:|:---------:|
| **arkalia-aria** | `6,082` | `3,764,289` | `2,218` |
| **arkalia-cia** | `3,419` | `1,251,969` | `230` |
| **arkalia-luna-logo** | `17,671` | `6,946,020` | `2,230` |
| **arkalia-luna-pro** | `208` | `46,471` | `95` |
| **arkalia-metrics-collector** | `23` | `5,841` | `120` |
| **arkalia-quest** | `118` | `74,490` | `79` |
| **athalia-dev-setup** | `168` | `86,370` | `196` |
| **base-template** | `3,303` | `928,195` | `429` |
| **bbia-branding** | `11` | `2,411` | `2` |
| **bbia-reachy-sim** | `21,282` | `11,682,651` | `5,605` |
| **github-profile-arkalia** | `4` | `1,257` | `0` |
| **nours-interface** | `31` | `112` | `0` |
| **TOTAL** | **`52,320`** | **`24,790,076`** | **`11,204`** |

</div>

*Dernière mise à jour : 23 janvier 2026*

## Fonctionnalités

- 🚀 **Exclusion automatique** des venv, cache, dépendances
- 📊 **Métriques intelligentes** : code, tests, sécurité, qualité
- 🎨 **Export multi-format** : JSON, Markdown, HTML, CSV, YAML
- 🔧 **CLI professionnel** avec configuration flexible
- 🌐 **Dashboard web** interactif et responsive
- 🔗 **Intégration GitHub API** : stars, forks, issues, PRs, releases
- 📈 **Agrégation multi-projets** : coverage global, métriques agrégées
- 🏷️ **Génération de badges** : Shields.io, Codecov, GitHub Actions
- 📋 **Tableaux README automatiques** : métriques sourcées et vérifiables
- 📊 **Support Coverage automatique** : parsing coverage.xml, calcul global
- 📅 **Comparaison temporelle** : historique des métriques, rapports d'évolution
- 🔄 **Automatisation CI/CD** : mise à jour quotidienne via GitHub Actions
- 🧪 **Tests complets** : tests unitaires, intégration et performance
- 📧 **Notifications multi-canaux** : Email (SMTP), Slack, Discord
- 📊 **Statistiques Git** : commits, lignes, contributeurs, activité temporelle
- 🌐 **Export vers services externes** : REST API (✅), Google Sheets, Notion, Airtable (📋 prévu)

## Installation

```bash
# Installation depuis le repository
git clone https://github.com/arkalia-luna-system/arkalia-metrics-collector.git
cd arkalia-metrics-collector
pip install -e .

# Ou installation directe (quand publié sur PyPI)
pip install arkalia-metrics-collector
```

## Usage

### Collecte basique

```bash
# Collecte simple
arkalia-metrics collect .

# Avec validation
arkalia-metrics collect . --validate

# Export spécifique
arkalia-metrics collect . --format markdown --output reports/
```

### Métriques GitHub

```bash
# Collecter les métriques GitHub d'un dépôt
arkalia-metrics github owner repo --token YOUR_TOKEN

# Avec export automatique
arkalia-metrics github arkalia-luna-system arkalia-metrics-collector --output metrics/
```

### Agrégation multi-projets

```bash
# Créer un fichier projects.json
echo '{"projects": [{"name": "projet1", "path": "/path/to/project1"}, {"name": "projet2", "path": "/path/to/project2"}]}' > projects.json

# Agréger les métriques
arkalia-metrics aggregate projects.json --readme-table --json
```

### Génération de badges

```bash
# Générer des badges depuis les métriques
arkalia-metrics badges metrics/metrics.json \
  --github-owner arkalia-luna-system \
  --github-repo arkalia-metrics-collector \
  --pypi-name arkalia-metrics-collector \
  --output badges.md
```

### Alertes et notifications

```bash
# Vérifier les changements significatifs
arkalia-metrics alerts metrics/aggregated_metrics.json

# Créer une issue GitHub si alertes détectées
arkalia-metrics alerts metrics/aggregated_metrics.json --create-issue \
  --github-owner arkalia-luna-system \
  --github-repo arkalia-metrics-collector

# Envoyer des notifications (Email, Slack, Discord)
arkalia-metrics alerts metrics/aggregated_metrics.json --notify
```

### Aide complète

```bash
arkalia-metrics --help
arkalia-metrics collect --help
arkalia-metrics validate --help
arkalia-metrics serve --help
```

## Architecture

```text
arkalia-metrics-collector/
├── src/arkalia_metrics_collector/
│   ├── collectors/          # Collecteurs de métriques
│   ├── exporters/           # Exporteurs multi-format
│   ├── validators/          # Validation des données
│   └── cli/                 # Interface en ligne de commande
├── config/                  # Templates de configuration
├── templates/               # Templates d'export
└── docs/                    # Documentation complète
```

## Configuration

Créez un fichier `arkalia-metrics.yaml` dans votre projet :

```yaml
project:
  name: "Mon Projet"
  type: "application"
  
exclusions:
  - "**/venv/**"
  - "**/.venv/**"
  - "**/__pycache__/**"
  - "**/.pytest_cache/**"
  - "**/node_modules/**"
  
metrics:
  - code_complexity
  - test_coverage
  - security_scan
  - documentation_quality
```

## Exemples de Sortie

### Métriques JSON

```json
{
  "project": "Mon Projet",
  "timestamp": "2025-08-30T14:36:00",
  "metrics": {
    "python_files": {
      "count": 150,
      "core_files": 120,
      "test_files": 30,
      "total_lines": 4500
    },
    "tests": {
      "count": 30,
      "coverage": 85.5
    }
  }
}
```

## 🎯 Pourquoi Choisir Arkalia Metrics Collector ?

### vs Autres Outils de Métriques

| Feature | Arkalia Metrics | pytest-cov | radon | bandit |
|---------|-----------------|------------|-------|--------|
| **Installation simple** | ✅ `pip install` | ✅ | ✅ | ✅ |
| **Multi-format export** | ✅ JSON/HTML/MD/CSV | ❌ HTML uniquement | ❌ Texte | ❌ JSON |
| **Dashboard intégré** | ✅ Responsive | ❌ | ❌ | ❌ |
| **Exclusions intelligentes** | ✅ Auto venv/cache | ⚠️ Manuel | ⚠️ Manuel | ⚠️ Manuel |
| **CLI unifiée** | ✅ Une commande | ❌ Multiples outils | ❌ | ❌ |
| **CI/CD ready** | ✅ GitHub Actions | ⚠️ Configuration | ❌ | ⚠️ |

### 🎯 Avantages Clés

- **🚀 Rapidité** : Métriques complètes en < 30 secondes
- **🔧 Modularité** : Collectors/Exporters/Validators séparés
- **🛡️ Sécurité** : Aucun code source collecté
- **📱 Responsive** : Dashboard mobile-friendly
- **🔄 Évolutif** : Architecture plugin-ready

## ⚠️ Limitations & Scope

### ❌ Pas (encore) supporté

- **Langages** : JavaScript, TypeScript, Go, Rust
- **Notebooks** : Jupyter .ipynb (prévu v1.2)
- **Métriques avancées** : Complexité cyclomatique détaillée
- **Base de données** : Stockage persistant des métriques

### 🎯 Scope volontaire

- **Focus Python** : Spécialisé pour l'écosystème Python
- **Métriques statiques** : Pas d'analyse runtime
- **Local-first** : Pas de télémétrie ou cloud obligatoire
- **Sans dépendances lourdes** : Reste léger et rapide

### 🔮 Roadmap

Consultez les [issues GitHub](https://github.com/arkalia-luna-system/arkalia-metrics-collector/issues) pour suivre les fonctionnalités prévues et les améliorations à venir.

## 🤝 Contributing

Les contributions sont les bienvenues ! Consultez [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) pour :

- Setup développement
- Standards de code
- Process de review
- Types de contributions

## 📄 License

MIT License - voir [LICENSE](LICENSE) pour plus de détails

## 📚 Documentation

- 📖 **[Guide Complet](docs/)** - Installation, usage, exemples
- ❓ **[FAQ](docs/FAQ.md)** - Questions fréquentes
- 🔒 **[Sécurité](docs/SECURITY.md)** - Politique de sécurité
- 🤝 **[Contribution](docs/CONTRIBUTING.md)** - Guide contributeur

## Auteur

**Arkalia Luna System**

- GitHub: [@arkalia-luna-system](https://github.com/arkalia-luna-system)
- Portfolio: [arkalia-luna-system.github.io](https://arkalia-luna-system.github.io)

---

<div align="center">

Si ce projet vous aide, donnez-lui une étoile sur GitHub.

</div>
