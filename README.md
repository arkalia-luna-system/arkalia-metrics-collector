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

## 🤝 Contributing

Les contributions sont les bienvenues ! 

1. Fork le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📄 License

MIT License - voir [LICENSE](LICENSE) pour plus de détails

## 👨‍💻 Auteur

**Arkalia Luna System**
- GitHub: [@arkalia-luna-system](https://github.com/arkalia-luna-system)
- Portfolio: [arkalia-luna-system.github.io](https://arkalia-luna-system.github.io)

---

<div align="center">

**⭐ Si ce projet vous aide, donnez-lui une étoile ! ⭐**

</div>
