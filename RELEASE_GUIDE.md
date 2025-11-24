# 🚀 Guide de Release GitHub - Arkalia Metrics Collector

## 📋 État Actuel (24 novembre 2025)

- **Version actuelle** : `1.1.0`
- **Dernier tag** : `v1.0.0`
- **Branche actuelle** : `develop`
- **Statut** : Prêt pour release `v1.1.0`

## ✅ Checklist Pré-Release

### 1. Vérifications Finales

- [x] Toutes les dates dans les fichiers MD sont à jour (24 nov 2025)
- [x] Aucune erreur de lint (ruff check passé)
- [x] Version dans `pyproject.toml` : `1.1.0`
- [x] CHANGELOG.md mis à jour avec date `2025-11-24`
- [x] Workflows GitHub Actions corrigés

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

## 🎯 Étapes pour Créer la Release GitHub

### Étape 1 : Créer le Tag

```bash
# Sur la branche main
git checkout main
git pull origin main

# Créer le tag annoté
git tag -a v1.1.0 -m "Release v1.1.0 - Intégrations Avancées

✨ Nouvelles Fonctionnalités:
- Intégration GitHub API complète
- Notifications multi-canaux (Email, Slack, Discord)
- Personnalisation avancée (labels, assignation)
- Statistiques Git
- Export REST API

🔧 Améliorations:
- Agrégation multi-projets enrichie
- Système d'alertes amélioré
- CLI enrichi avec nouvelles options
- Documentation complète mise à jour

📝 Documentation:
- Guide d'utilisation mis à jour
- FAQ enrichie
- API documentation mise à jour"

# Pousser le tag
git push origin v1.1.0
```

### Étape 2 : Créer la Release sur GitHub

1. **Aller sur GitHub** : <https://github.com/arkalia-luna-system/arkalia-metrics-collector/releases/new>

2. **Remplir les informations** :

   **Tag** : `v1.1.0`

   **Titre** : `v1.1.0 - Intégrations Avancées`

   **Description** (copier-coller ceci) :

   ```markdown
   # 🚀 Release v1.1.0 - Intégrations Avancées
   
   **Date de release** : 24 novembre 2025
   
   ## ✨ Nouvelles Fonctionnalités
   
   ### Intégration GitHub API Complète
   - Collecte automatique des stars, forks, issues, PRs
   - Option `--github-api` pour activer la collecte GitHub
   - Intégration transparente avec les métriques existantes
   
   ### Notifications Multi-Canaux
   - **Email (SMTP)** : Notifications par email personnalisables
   - **Slack** : Intégration via webhooks
   - **Discord** : Support des webhooks Discord
   - Configuration simple via variables d'environnement
   
   ### Personnalisation Avancée
   - Labels personnalisés pour les issues GitHub
   - Assignation automatique d'issues
   - Seuils configurables pour les alertes
   - Personnalisation complète des notifications
   
   ### Statistiques Git
   - Analyse des commits et contributeurs
   - Métriques de lignes de code par commit
   - Analyse de l'activité temporelle
   - Statistiques détaillées par projet
   
   ### Export REST API
   - Export vers API REST personnalisée
   - Structure prête pour Google Sheets, Notion, Airtable
   - Format JSON standardisé
   
   ## 🔧 Améliorations
   
   - **Agrégation multi-projets** : Enrichie avec métriques GitHub et Git
   - **Système d'alertes** : Amélioré avec notifications automatiques
   - **CLI enrichi** : Nouvelles options (`--github-api`, `--notify`, `--labels`, `--assignees`)
   - **Documentation** : Complète et mise à jour
   
   ## 📝 Documentation
   
   - Guide d'utilisation mis à jour avec toutes les nouvelles fonctionnalités
   - FAQ enrichie (GitHub API, notifications, Git, export REST)
   - API documentation complète
   
   ## 🔗 Liens
   
   - [Documentation complète](https://arkalia-luna-system.github.io/arkalia-metrics-collector/)
   - [Guide d'installation](https://arkalia-luna-system.github.io/arkalia-metrics-collector/guides/installation/)
   - [Guide d'utilisation](https://arkalia-luna-system.github.io/arkalia-metrics-collector/guides/usage/)
   - [CHANGELOG complet](https://github.com/arkalia-luna-system/arkalia-metrics-collector/blob/main/CHANGELOG.md)
   
   ## 📦 Installation
   
   ```bash
   pip install arkalia-metrics-collector==1.1.0
   ```

   ## 🎯 Prochaines Versions

   - **v1.2.0** (Q2 2025) : Support Jupyter Notebooks, langage Go, stockage persistant
   - **v1.3.0** (Q3 2025) : Support Rust, intégrations CI/CD avancées, système de plugins

   ---

   **Merci d'utiliser Arkalia Metrics Collector ! 🎉**

   ```text

3. **Cocher** : "Set as the latest release" (si c'est la dernière version)

4. **Cliquer** : "Publish release"

## 📊 Après la Release

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

## 🎉 Résumé

Une fois la release créée :

- ✅ Tag `v1.1.0` créé et poussé
- ✅ Release GitHub publiée
- ✅ Documentation mise à jour
- ✅ Branches synchronisées

## 📝 Notes Importantes

- **Ne jamais** créer de release directement depuis develop
- **Toujours** merger develop → main avant de créer une release
- **Vérifier** que tous les tests passent avant la release
- **S'assurer** que le CHANGELOG est à jour
- **Vérifier** que la version dans `pyproject.toml` correspond au tag

---

**Date de création de ce guide** : 24 novembre 2025
