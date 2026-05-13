# Guide de Release GitHub

Guide pour créer une release GitHub pour **Arkalia Metrics Collector**.

## État Actuel

Vérifiez l'état actuel du projet avant de créer une release :
- Version actuelle : Vérifier dans `pyproject.toml`
- Dernier tag : `git tag -l`
- Branche actuelle : Généralement `develop` ou `main`
- Statut : Vérifier que tous les tests passent

## Checklist Pré-Release

### 1. Vérifications Finales
- [ ] Toutes les dates dans les fichiers MD sont à jour
- [ ] Aucune erreur de lint (ruff check passé)
- [ ] Version dans `pyproject.toml` correspond à la release
- [ ] CHANGELOG.md mis à jour avec la date actuelle
- [ ] Workflows GitHub Actions fonctionnent correctement

### 2. Synchronisation des Branches

```bash
# Vérifier que develop et main sont synchronisés
git checkout develop
git pull origin develop
git checkout main
git pull origin main
git merge develop  # Si nécessaire
```

### 3. Tests Finaux

```bash
# Lancer les tests
pytest tests/ -v

# Vérifier le lint
ruff check .

# Vérifier les types
mypy src/arkalia_metrics_collector/
```

## Étapes pour Créer la Release GitHub

### Étape 1 : Créer le Tag

```bash
# Sur la branche main
git checkout main
git pull origin main

# Créer le tag annoté (remplacer X.Y.Z par la version)
git tag -a vX.Y.Z -m "Release vX.Y.Z - [Titre de la release]

✨ Nouvelles Fonctionnalités:
- [Liste des nouvelles fonctionnalités]

🔧 Améliorations:
- [Liste des améliorations]

📝 Documentation:
- [Liste des mises à jour de documentation]"

# Pousser le tag
git push origin vX.Y.Z
```

### Étape 2 : Créer la Release sur GitHub

1. **Aller sur GitHub** : <https://github.com/arkalia-luna-system/arkalia-metrics-collector/releases/new>

2. **Remplir les informations** :
   - **Tag** : `vX.Y.Z` (remplacer par la version)
   - **Titre** : `vX.Y.Z - [Titre de la release]`
   - **Description** : Copier le contenu du CHANGELOG.md pour cette version

3. **Cocher** : "Set as the latest release" (si c'est la dernière version)

4. **Cliquer** : "Publish release"

**Exemple de description** :

```markdown
# 🚀 Release vX.Y.Z - [Titre]

**Date de release** : [Date actuelle]

## ✨ Nouvelles Fonctionnalités
- [Liste des fonctionnalités]

## 🔧 Améliorations
- [Liste des améliorations]

## 📝 Documentation
- [Liste des mises à jour]

## 🔗 Liens
- [Documentation complète](https://arkalia-luna-system.github.io/arkalia-metrics-collector/)
- [CHANGELOG complet](https://github.com/arkalia-luna-system/arkalia-metrics-collector/blob/main/CHANGELOG.md)

## 📦 Installation
```bash
pip install arkalia-metrics-collector==X.Y.Z
```
```

## Après la Release

### 1. Mettre à jour develop

```bash
git checkout develop
git merge main
git push origin develop
```

### 2. Vérifier PyPI (si publication automatique)

Le workflow CI/CD devrait publier automatiquement sur PyPI si configuré.

### 3. Vérifier GitHub Pages

La documentation devrait être mise à jour automatiquement.

## Résumé

Une fois la release créée :
- Tag créé et poussé
- Release GitHub publiée
- Documentation mise à jour
- Branches synchronisées

## Notes Importantes

- Ne jamais créer de release directement depuis develop
- Toujours merger develop → main avant de créer une release
- Vérifier que tous les tests passent avant la release
- S'assurer que le CHANGELOG est à jour
- Vérifier que la version dans `pyproject.toml` correspond au tag
