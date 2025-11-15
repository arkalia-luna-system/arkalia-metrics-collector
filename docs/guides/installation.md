# 📦 Installation

## Prérequis

- **Python** : 3.8 ou supérieur (testé sur 3.8, 3.9, 3.10, 3.11, 3.12)
- **pip** : Gestionnaire de paquets Python
- **Git** : Pour cloner le repository (optionnel)

## 🚀 Installation depuis PyPI (recommandé)

```bash
pip install arkalia-metrics-collector
```

## 🔧 Installation depuis les sources

```bash
# Cloner le repository
git clone https://github.com/arkalia-luna-system/arkalia-metrics-collector.git
cd arkalia-metrics-collector

# Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# ou
.venv\\Scripts\\activate  # Windows

# Installer en mode développement
pip install -e ".[dev]"
```

## ✅ Vérification de l'installation

```bash
# Vérifier l'installation
python -c "from arkalia_metrics_collector import MetricsCollector; print('✅ Installation réussie!')"

# Tester la CLI
arkalia-metrics --help
```

## 🔧 Dépendances de développement

Pour contribuer au projet :

```bash
pip install -e ".[dev]"
```

**Outils inclus :**
- **pytest** : Tests unitaires et d'intégration
- **ruff** : Linter et formateur
- **black** : Formateur de code
- **isort** : Tri des imports
- **mypy** : Vérification de types
- **mkdocs** : Documentation

## 🐛 Résolution de problèmes

### Erreur d'import
```bash
# Vérifier l'environnement virtuel
which python
pip list | grep arkalia
```

### Erreur de permissions
```bash
# Utiliser --user si nécessaire
pip install --user arkalia-metrics-collector
```

### Version Python incompatible
```bash
# Vérifier la version
python --version
# Utiliser pyenv ou conda pour changer de version
```
