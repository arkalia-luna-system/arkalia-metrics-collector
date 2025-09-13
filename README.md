# Arkalia Metrics Collector 🚀

[![PyPI version](https://badge.fury.io/py/arkalia-metrics-collector.svg)](https://badge.fury.io/py/arkalia-metrics-collector)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Collecteur de métriques universel et professionnel pour projets Python**

## 📊 **Métriques du Projet** *(Mises à jour automatiquement)*

<div align="center">

| **Composant** | **Valeur** | **Statut** | **Vérifié** |
|:-------------:|:---------:|:----------:|:------------:|
| **🐍 Fichiers Python** | `14 modules` | ![Actif](https://img.shields.io/badge/status-active-brightgreen) | ✅ **COMPTÉS** |
| **📝 Lignes de Code** | `2,368 lignes` | ![Maintenu](https://img.shields.io/badge/status-maintained-blue) | ✅ **MESURÉES** |
| **🧪 Tests** | `62 tests` | ![Testé](https://img.shields.io/badge/status-tested-green) | ✅ **COLLECTÉS** |
| **📚 Documentation** | `193 fichiers` | ![Complet](https://img.shields.io/badge/status-complete-yellow) | ✅ **ORGANISÉS** |

</div>

*Métriques collectées automatiquement le 2025-08-31 13:00 par le Collecteur de Métriques Arkalia*

## ✨ Features

- 🚀 **Exclusion automatique** des venv, cache, dépendances
- 📊 **Métriques intelligentes** : code, tests, sécurité, qualité
- 🎨 **Export multi-format** : JSON, Markdown, HTML, CSV
- 🔧 **CLI professionnel** avec configuration flexible
- 🌐 **Dashboard web** interactif et responsive
- 🔗 **Intégration GitHub** automatique
- 📈 **Évolution temporelle** des métriques

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

```bash
# Collecte simple
arkalia-metrics collect .

# Avec configuration personnalisée
arkalia-metrics collect . --config my_config.yaml

# Export spécifique
arkalia-metrics collect . --format markdown --output reports/

# Afficher l'aide
arkalia-metrics --help
```

## 🏗️ Architecture

```
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
- **API REST** : Endpoints temps réel (prévu v1.1)

### 🎯 **Scope volontaire**

- **Focus Python** : Spécialisé pour l'écosystème Python
- **Métriques statiques** : Pas d'analyse runtime
- **Local-first** : Pas de télémétrie ou cloud obligatoire
- **Sans dépendances lourdes** : Reste léger et rapide

### 🔮 **Roadmap**

| Version | Features Prévues | Timeline |
|---------|------------------|----------|
| **v1.1** | API REST + JavaScript support | Q1 2025 |
| **v1.2** | Jupyter notebooks + Go support | Q2 2025 |
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

**Arkalia Luna System**
- GitHub: [@arkalia-luna-system](https://github.com/arkalia-luna-system)
- Portfolio: [arkalia-luna-system.github.io](https://arkalia-luna-system.github.io)

---

<div align="center">

**⭐ Si ce projet vous aide, donnez-lui une étoile ! ⭐**

</div>
