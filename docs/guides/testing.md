# 🧪 Guide des Tests

**Tests complets et validation pour Arkalia Metrics Collector**

## 📊 **Vue d'ensemble des Tests**

Arkalia Metrics Collector dispose d'une suite de tests complète avec **110 tests** couvrant tous les aspects du système :

- ✅ **Tests unitaires** : Fonctionnalités individuelles
- ✅ **Tests d'intégration** : Projets externes et validation
- ✅ **Tests de performance** : Mesures de vitesse et mémoire
- ✅ **Tests CLI** : Interface en ligne de commande

## 🎯 **Types de Tests**

### 1. **Tests Unitaires** (`tests/unit/`)

#### Collecteurs (`test_metrics_collector.py`)
- Initialisation et configuration
- Collecte des métriques Python
- Collecte des tests avec pytest
- Collecte de la documentation
- Gestion des exclusions (venv, cache, etc.)
- Tests de performance sur gros projets

#### Exporteurs (`test_metrics_exporter.py`)
- Export JSON, Markdown, HTML, CSV
- Validation du contenu des exports
- Gestion des erreurs d'export
- Création automatique des dossiers
- Tests avec gros volumes de données

#### Validateurs (`test_metrics_validator.py`)
- Validation de la structure des métriques
- Validation de cohérence des données
- Validation de qualité (couverture, etc.)
- Messages d'erreur et d'avertissement
- Tests de performance sur gros datasets

#### CLI (`test_cli_main.py`)
- Commandes `collect`, `validate`, `serve`
- Options et arguments
- Gestion des erreurs
- Validation des outputs
- Tests avec chemins spéciaux

### 2. **Tests d'Intégration** (`tests/integration/`)

#### Projets Externes (`test_external_projects.py`)
- Tests sur projets simulés de différentes tailles
- Validation des métriques collectées
- Tests d'export sur projets externes
- Mesures de performance
- Gestion d'erreurs avec projets invalides
- Simulation de projets du monde réel

#### Validation des Outputs (`test_output_validation.py`)
- Validation JSON, Markdown, HTML, CSV
- Cohérence entre tous les formats
- Tests d'encodage UTF-8
- Tests avec caractères spéciaux
- Validation des permissions de fichiers
- Tests avec projets vides

### 3. **Tests de Performance** (`tests/performance/`)

#### Métriques de Performance (`test_performance_metrics.py`)
- Tests sur projets de différentes tailles :
  - **Petit** : 10-50 fichiers (< 1 seconde)
  - **Moyen** : 100-500 fichiers (< 3 secondes)
  - **Grand** : 1000+ fichiers (< 10 secondes)
- Mesures d'utilisation mémoire
- Tests de collecte concurrente
- Benchmarks de vitesse
- Tests de stress avec collecte répétée

## 🚀 **Exécution des Tests**

### Tests Complets
```bash
# Tous les tests
pytest tests/ -v

# Tests par catégorie
pytest tests/unit/ -v          # Tests unitaires
pytest tests/integration/ -v   # Tests d'intégration
pytest tests/performance/ -v   # Tests de performance
```

### Tests Spécifiques
```bash
# Tests CLI uniquement
pytest tests/unit/cli/ -v

# Tests sur projets externes
pytest tests/integration/test_external_projects.py -v

# Tests de performance
pytest tests/performance/ -v --tb=short
```

### Tests avec Couverture
```bash
# Couverture complète
pytest tests/ --cov=src/arkalia_metrics_collector --cov-report=html

# Couverture par module
pytest tests/ --cov=src/arkalia_metrics_collector.collectors --cov-report=term
```

## 📈 **Métriques de Qualité**

### Couverture de Code
- **Collecteurs** : 100% des lignes testées
- **Exporteurs** : 100% des lignes testées
- **Validateurs** : 100% des lignes testées
- **CLI** : 100% des lignes testées

### Performance
- **Collecte** : < 10 secondes pour 1000+ fichiers
- **Export** : < 5 secondes pour tous les formats
- **Validation** : < 1 seconde pour gros datasets
- **Mémoire** : < 200 MB pour projets volumineux

### Fiabilité
- **110/110 tests** passent (100% de réussite)
- **0 erreur** de linting (ruff, black, mypy)
- **0 vulnérabilité** de sécurité (bandit)
- **Tests robustes** avec gestion d'erreurs

## 🔧 **Configuration des Tests**

### Variables d'Environnement
```bash
# Mode verbeux
export PYTEST_VERBOSE=1

# Tests de performance uniquement
export PYTEST_PERFORMANCE=1

# Dossier de sortie pour tests
export TEST_OUTPUT_DIR=/tmp/arkalia_tests
```

### Fichiers de Configuration
- `pyproject.toml` : Configuration pytest
- `conftest.py` : Fixtures partagées
- `pytest.ini` : Options pytest (si nécessaire)

## 🐛 **Débogage des Tests**

### Mode Débogage
```bash
# Arrêt sur premier échec
pytest tests/ -x

# Mode interactif
pytest tests/ --pdb

# Affichage des prints
pytest tests/ -s
```

### Logs Détaillés
```bash
# Logs de collecte
pytest tests/ --log-cli-level=DEBUG

# Logs spécifiques
pytest tests/ --log-cli-level=INFO --log-cli-format="%(asctime)s [%(levelname)8s] %(message)s"
```

## 📝 **Écriture de Nouveaux Tests**

### Structure Recommandée
```python
def test_nouvelle_fonctionnalite():
    """Test de la nouvelle fonctionnalité."""
    # Arrange
    input_data = "données de test"
    expected_output = "résultat attendu"
    
    # Act
    result = ma_fonction(input_data)
    
    # Assert
    assert result == expected_output
    assert isinstance(result, str)
```

### Fixtures Disponibles
- `temp_project_dir` : Dossier de projet temporaire
- `sample_metrics_data` : Données de métriques d'exemple
- `runner` : Runner Click pour tests CLI
- `comprehensive_project` : Projet complet pour tests

### Bonnes Pratiques
1. **Noms descriptifs** : `test_collect_metrics_with_large_project`
2. **Documentation** : Docstring explicative
3. **Isolation** : Chaque test est indépendant
4. **Nettoyage** : Suppression des fichiers temporaires
5. **Assertions claires** : Messages d'erreur explicites

## 🚨 **Tests en CI/CD**

### GitHub Actions
Les tests s'exécutent automatiquement sur :
- **Python 3.8, 3.9, 3.10, 3.11**
- **Ubuntu, macOS, Windows**
- **Chaque push et PR**

### Validation Qualité
- **Ruff** : Linting et formatage
- **Black** : Formatage automatique
- **MyPy** : Vérification des types
- **Bandit** : Sécurité
- **Pytest** : Tests unitaires et intégration

## 📊 **Rapports de Tests**

### Rapport HTML
```bash
pytest tests/ --html=reports/test_report.html --self-contained-html
```

### Rapport JUnit
```bash
pytest tests/ --junitxml=reports/junit.xml
```

### Rapport de Couverture
```bash
pytest tests/ --cov=src/ --cov-report=html --cov-report=term
```

## 🎯 **Prochaines Étapes**

1. **Tests E2E** : Tests complets bout en bout
2. **Tests de Charge** : Performance sous charge
3. **Tests de Compatibilité** : Différentes versions Python
4. **Tests de Sécurité** : Validation des entrées malveillantes

---

**🚀 [Retour à la documentation](../index.md) | 📝 [Voir les tests sur GitHub](https://github.com/arkalia-luna-system/arkalia-metrics-collector/tree/main/tests)**
