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
[![CI](https://github.com/arkalia-luna-system/arkalia-metrics-collector/actions/workflows/ci.yml/badge.svg)](https://github.com/arkalia-luna-system/arkalia-metrics-collector/actions)
[![Codecov](https://codecov.io/gh/arkalia-luna-system/arkalia-metrics-collector/branch/main/graph/badge.svg)](https://codecov.io/gh/arkalia-luna-system/arkalia-metrics-collector)

## 📋 Description

**Arkalia Metrics Collector** est un outil professionnel et complet pour collecter, analyser et visualiser les métriques de vos projets Python. Il offre une analyse automatique du code source, des tests, de la documentation, du coverage, et des métriques GitHub, avec export multi-format et dashboard interactif.

## 📊 **Métriques du Projet** *(Mises à jour automatiquement)*

<div align="center">

| **Composant** | **Valeur** | **Statut** | **Vérifié** |
|:-------------:|:---------:|:----------:|:------------:|
| **🐍 Fichiers Python** | `23 modules` | ![Actif](https://img.shields.io/badge/status-active-brightgreen) | ✅ **COMPTÉS** |
| **📝 Lignes de Code** | `5,841 lignes` | ![Maintenu](https://img.shields.io/badge/status-maintained-blue) | ✅ **MESURÉES** |
| **🧪 Tests** | `120 tests` | ![Testé](https://img.shields.io/badge/status-tested-green) | ✅ **COLLECTÉS** |
| **📚 Documentation** | `56 fichiers` | ![Complet](https://img.shields.io/badge/status-complete-yellow) | ✅ **ORGANISÉS** |

</div>

*Métriques collectées automatiquement le 2026-04-17 par le Collecteur de Métriques Arkalia*

## 📊 **Métriques Globales** *(Mise à jour automatique)*

<div align="center">

| **Projet** | **Modules** | **Lignes** | **Tests** | **Coverage** |
|:-----------|:-----------:|:----------:|:---------:|:------------:|
| **arkalia-aria** | `0` | `0` | `0` | `N/A` |
| **arkalia-cia** | `0` | `0` | `0` | `N/A` |
| **arkalia-luna-logo** | `0` | `0` | `0` | `N/A` |
| **arkalia-luna-pro** | `0` | `0` | `0` | `N/A` |
| **arkalia-metrics-collector** | `0` | `0` | `0` | `N/A` |
| **arkalia-quest** | `0` | `0` | `0` | `N/A` |
| **base-template** | `0` | `0` | `0` | `N/A` |
| **bbia-branding** | `0` | `0` | `0` | `N/A` |
| **bbia-reachy-sim** | `0` | `0` | `0` | `N/A` |
| **github-profile-arkalia** | `0` | `0` | `0` | `N/A` |
| **ia-pipeline** | `0` | `0` | `0` | `N/A` |
| **nours-interface** | `0` | `0` | `0` | `N/A` |
| **TOTAL** | **`0`** | **`0`** | **`0`** | **N/A** |

</div>

*Métriques collectées automatiquement le 2026-04-17T02:58:02.339823*

## ✨ Features

- 🚀 **Exclusion automatique** des venv, cache, dépendances
- 📊 **Métriques intelligentes** : code, tests, sécurité, qualité
- 🎨 **Export multi-format** : JSON, Markdown, HTML, CSV, YAML
- 🔧 **CLI professionnel** avec configuration flexible
- 🌐 **Dashboard web** interactif et responsive
- 🔗 **Intégration GitHub API complète** : stars, forks, issues, PRs, releases (option `--github-api`)
- 📈 **Agrégation multi-projets** : coverage global, métriques agrégées
- 🏷️ **Génération de badges** : Shields.io, Codecov, GitHub Actions
- 📋 **Tableaux README automatiques** : métriques sourcées et vérifiables
- 📊 **Support Coverage automatique** : parsing coverage.xml, calcul global
- 📅 **Comparaison temporelle** : historique des métriques, rapports d'évolution
- 🔄 **Automatisation CI/CD** : mise à jour quotidienne via GitHub Actions
- 🧪 **Tests complets** : 110 tests unitaires, intégration et performance
- 🌐 **Tests sur projets externes** avec validation automatique
- 📧 **Notifications multi-canaux** : Email (SMTP), Slack, Discord
- 🎯 **Personnalisation avancée** : labels personnalisés, assignation d'issues, seuils configurables
- 📊 **Statistiques Git** : commits, lignes, contributeurs, activité temporelle
- 🌐 **Export vers services externes** : REST API, Google Sheets, Notion, Airtable (structure prête)

## 🚀 Installation

```bash
# Installation depuis le repository
git clone https://github.com/arkalia-luna-system/arkalia-metrics-collector.git
cd arkalia-metrics-collector
pip install -e .

# Ou installation directe (quand publié sur PyPI)
pip install arkalia-metrics-collector
```

## 📖 Usage

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

# Génère :
# - aggregated_metrics.json : métriques agrégées
# - README_TABLE.md : tableau récapitulatif pour README
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

### Export depuis fichier JSON

```bash
# Exporter dans un format spécifique
arkalia-metrics export metrics.json --format yaml

# Exporter dans tous les formats
arkalia-metrics export metrics.json --format all --output exports/
```

### Comparaison temporelle

```bash
# Générer un rapport d'évolution
arkalia-metrics aggregate projects.json --evolution --json --readme-table

# Désactiver l'historique si nécessaire
arkalia-metrics aggregate projects.json --no-history
```

### Alertes et notifications

```bash
# Vérifier les changements significatifs
arkalia-metrics alerts metrics/aggregated_metrics.json

# Avec seuil personnalisé
arkalia-metrics alerts metrics/aggregated_metrics.json --threshold 15.0

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
arkalia-metrics export --help
arkalia-metrics github --help
arkalia-metrics aggregate --help
arkalia-metrics badges --help
arkalia-metrics alerts --help
```

## 🏗️ Architecture

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

## 🔧 Configuration

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

## 📊 Exemples de Sortie

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

### Export Markdown

```markdown
## 📊 Métriques du Projet

| Métrique | Valeur |
|----------|---------|
| Fichiers Python | 150 |
| Lignes de Code | 4,500 |
| Tests | 30 |
| Couverture | 85.5% |
```

## 🚀 Projets Utilisant Arkalia Metrics

- [Athalia Core](https://github.com/arkalia-luna-system/ia-pipeline) - Framework IA Enterprise
- [Arkalia Quest](https://github.com/arkalia-luna-system/arkalia-quest) - Jeu éducatif IA
- [BBIA Simulation](https://github.com/arkalia-luna-system/bbia-sim) - Simulation robotique

## 🎯 Pourquoi Choisir Arkalia Metrics Collector ?

### vs Autres Outils de Métriques

| Feature | Arkalia Metrics | pytest-cov | radon | bandit | Autres |
|---------|-----------------|------------|-------|--------|--------|
| **Installation simple** | ✅ `pip install` | ✅ | ✅ | ✅ | ⚠️ Configuration complexe |
| **Multi-format export** | ✅ JSON/HTML/MD/CSV | ❌ HTML uniquement | ❌ Texte | ❌ JSON | ⚠️ Format propriétaire |
| **Dashboard intégré** | ✅ Responsive | ❌ | ❌ | ❌ | 💰 Payant |
| **Exclusions intelligentes** | ✅ Auto venv/cache | ⚠️ Manuel | ⚠️ Manuel | ⚠️ Manuel | ❌ |
| **CLI unifiée** | ✅ Une commande | ❌ Multiples outils | ❌ | ❌ | ❌ |
| **CI/CD ready** | ✅ GitHub Actions | ⚠️ Configuration | ❌ | ⚠️ | ⚠️ |

### 🎯 Avantages Clés

- **🚀 Rapidité** : Métriques complètes en < 30 secondes
- **🔧 Modularité** : Collectors/Exporters/Validators séparés
- **🛡️ Sécurité** : Aucun code source collecté
- **📱 Responsive** : Dashboard mobile-friendly
- **🔄 Évolutif** : Architecture plugin-ready

## ⚠️ Limitations & Scope

### ❌ **Pas (encore) supporté**

- **Langages** : JavaScript, TypeScript, Go, Rust
- **Notebooks** : Jupyter .ipynb (prévu v1.2)
- **Métriques avancées** : Complexité cyclomatique détaillée
- **Base de données** : Stockage persistant des métriques

### 🎯 **Scope volontaire**

- **Focus Python** : Spécialisé pour l'écosystème Python
- **Métriques statiques** : Pas d'analyse runtime
- **Local-first** : Pas de télémétrie ou cloud obligatoire
- **Sans dépendances lourdes** : Reste léger et rapide

### 🔮 **Roadmap**

| Version | Features Prévues | Timeline |
|---------|------------------|----------|
| **v1.2** | Jupyter notebooks + Go support + Complexité cyclomatique | Q2 2025 |
| **v1.3** | Plugins système + Rust support | Q3 2025 |

## 🤝 Contributing

**Nous recherchons activement des contributeurs !** 🎯

### 🟢 **Issues "Help Wanted"**

- 📚 Amélioration documentation
- 🧪 Tests sur nouveaux projets Python
- 🎨 Templates de configuration
- 🌍 Traductions (anglais, espagnol)

### 🚀 **Features Recherchées**

- Support JavaScript/TypeScript
- Métriques de complexité avancées
- Intégration SonarQube/CodeClimate
- Dashboard temps réel

### 📋 **Guide Complet**

Voir [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) pour :

- Setup développement
- Standards de code
- Process de review
- Types de contributions

**Contribution rapide :** Testez sur votre projet et signalez les améliorations !

## 📄 License

MIT License - voir [LICENSE](LICENSE) pour plus de détails

## 📚 Documentation

- 📖 **[Guide Complet](docs/)** - Installation, usage, exemples
- ❓ **[FAQ](docs/FAQ.md)** - Questions fréquentes
- 🔒 **[Sécurité](docs/SECURITY.md)** - Politique de sécurité
- 🤝 **[Contribution](docs/CONTRIBUTING.md)** - Guide contributeur

## 👨‍💻 Auteur

## Arkalia Luna System

- GitHub: [@arkalia-luna-system](https://github.com/arkalia-luna-system)
- Portfolio: [arkalia-luna-system.github.io](https://arkalia-luna-system.github.io)

---

<div align="center">

### ⭐ Si ce projet vous aide, donnez-lui une étoile ! ⭐

</div>
