# Arkalia Metrics Collector

CLI perso pour collecter des métriques sur des projets Python (fichiers, tests, docs, exports).

> **Note (août 2026)** : d’anciens badges / tableaux affichaient des totaux absurdes
> (des millions de lignes) — erreur d’agrégation, **pas** la taille réelle de ce dépôt.
> Ce README a été corrigé pour rester factuel.

![License](https://img.shields.io/badge/License-MIT-blue?style=flat)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat&logo=python)
[![CI](https://github.com/arkalia-luna-system/arkalia-metrics-collector/actions/workflows/ci.yml/badge.svg)](https://github.com/arkalia-luna-system/arkalia-metrics-collector/actions)

## Description

Outil d’analyse locale : scanner un repo Python, exporter des métriques
(JSON / Markdown / HTML / CSV / YAML). Utile pour un suivi perso multi-projets.
Ce n’est **pas** une plateforme « enterprise » ni un SaaS.

## Ordre de grandeur de **ce** dépôt

| Composant | Ordre de grandeur |
|-----------|-------------------|
| Modules Python | ~dizaines |
| Tests | ~centaine |
| Rôle | Outillage perso |

*(Les chiffres exacts évoluent — se fier à `pytest` / CI, pas à d’anciens badges.)*

## Ancienne section « métriques globales »

~~Tableaux multi-projets avec des millions de LOC~~ — **retirés** (non fiables).

## Fonctionnalités

- Exclusion venv / cache / dépendances
- Métriques code / tests / docs
- Export JSON, Markdown, HTML, CSV, YAML
- CLI + option dashboard local
- Intégration GitHub API (optionnelle)
- CI GitHub Actions

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
