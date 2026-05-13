# 📊 Configuration Codecov

Ce document explique comment Codecov est configuré pour **Arkalia Metrics Collector**.

## ✅ Configuration Actuelle

### 1. Fichier de Configuration

Le fichier `.codecov.yml` à la racine du projet configure :
- **Seuil de coverage** : 80% minimum
- **Branches suivies** : `main` et `develop`
- **Ignorer** : tests, venv, cache, archives
- **Flags** : `unittests` pour le code source

### 2. Intégration CI/CD

Le workflow `.github/workflows/ci.yml` inclut :

```yaml
- name: "Upload Coverage"
  uses: codecov/codecov-action@v6
  with:
    files: ./coverage.xml
    flags: unittests
    name: codecov-umbrella
    fail_ci_if_error: false
```

### 3. Badge Codecov

Le badge est automatiquement généré dans le README :

```markdown
[![Codecov](https://codecov.io/gh/arkalia-luna-system/arkalia-metrics-collector/branch/main/graph/badge.svg)](https://codecov.io/gh/arkalia-luna-system/arkalia-metrics-collector)
```

## 🔧 Configuration GitHub

**Note** : Pour les repositories publics, aucun token n'est nécessaire. L'action Codecov fonctionne automatiquement.

## 📈 Vérification

### Vérifier le Coverage

1. **Sur Codecov** : https://codecov.io/gh/arkalia-luna-system/arkalia-metrics-collector
2. **Dans le README** : Le badge affiche le coverage actuel
3. **Localement** : `pytest tests/ --cov=arkalia_metrics_collector --cov-report=html`

### Rapports Locaux

```bash
# Générer coverage.xml
pytest tests/ --cov=arkalia_metrics_collector --cov-report=xml

# Générer rapport HTML
pytest tests/ --cov=arkalia_metrics_collector --cov-report=html
open htmlcov/index.html
```

## 🎯 Objectifs de Coverage

- **Minimum** : 80% (configuré dans `.codecov.yml`)
- **Cible** : 85%+
- **Actuel** : Voir badge Codecov dans README

## 📝 Notes

- Le coverage est calculé uniquement sur `src/arkalia_metrics_collector/`
- Les fichiers de tests sont exclus du calcul
- Les fichiers temporaires (venv, cache, etc.) sont ignorés
- Le coverage est mis à jour automatiquement à chaque push sur `main` ou `develop`

