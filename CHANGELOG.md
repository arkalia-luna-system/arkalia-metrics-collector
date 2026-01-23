# 📝 Changelog

Toutes les modifications notables de ce projet seront documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/), et ce projet adhère à [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1] - 2026-01-23

### Corrections et Améliorations

#### Sécurité
- Protection des tokens GitHub : masquage dans les logs et messages d'erreur
- Gestion sécurisée des exceptions : ne plus exposer les détails d'erreurs contenant des informations sensibles

#### Qualité du Code
- Remplacement des `print()` par `logger` : standardisation dans `metrics_exporter.py` et `interactive_dashboard.py`
- Optimisation des imports : centralisation de `json`, `logging`, `traceback` au niveau module dans `cli/main.py`
- Correction bug critique : fonction `aggregate()` corrigée (boucle exécutée uniquement si nécessaire)
- Amélioration typage : ajout de type hints manquants, correction dans `github_issues.py`
- Exceptions personnalisées : création du module `exceptions.py` avec hiérarchie complète d'exceptions
- Refactoring validation des chemins : fonction centralisée `_validate_and_normalize_path()` pour éliminer la duplication
- Extraction de constantes : port serveur, codes HTTP, timeout extraits en constantes
- Métriques de performance : temps de collecte mesuré automatiquement dans `collect_all_metrics()`
- Cache persistant GitHub API : cache avec fichier JSON et TTL configurable
- Retry avec backoff exponentiel : gestion robuste des erreurs temporaires GitHub API
- Progress bar : barre de progression avec tqdm pour collecte de fichiers Python (option `--progress`)
- Tests exporteurs externes : tests améliorés pour Google Sheets, Notion, Airtable avec validation complète
- Extraction constantes GitHub collector : toutes les valeurs magiques extraites en constantes nommées
- Amélioration gestion exceptions cache : exceptions spécifiques (OSError, IOError, JSONDecodeError) au lieu de Exception générique

#### Documentation
- Audit complet mis à jour avec toutes les corrections du 23 janvier 2026
- Mise à jour des dates et versions dans tous les fichiers de documentation
- Allègement des fichiers markdown pour améliorer la lisibilité

## [1.1.0] - 2025-11-24

### ✨ Phase 3 : Intégrations Avancées

#### 🚀 Nouvelles Fonctionnalités
- **Intégration GitHub API complète** : Collecte automatique stars, forks, issues, PRs (option `--github-api`)
- **Notifications multi-canaux** : Support Email (SMTP), Slack, Discord via webhooks
- **Personnalisation avancée** : Labels personnalisés, assignation d'issues, seuils configurables
- **Statistiques Git** : Analyse commits, lignes, contributeurs, activité temporelle
- **Export REST API** : Export vers API REST personnalisée
- **Structure exporteurs externes** : Google Sheets, Notion, Airtable (prêt pour implémentation)

#### 🔧 Améliorations
- Agrégation multi-projets enrichie avec métriques GitHub et Git
- Système d'alertes amélioré avec notifications
- CLI enrichi avec nouvelles options (`--github-api`, `--notify`, `--labels`, `--assignees`)
- Documentation complète mise à jour
- Correction duplication de code : Refactoring CLI
- Correction erreurs MyPy : Typage amélioré pour imports conditionnels
- Dependabot configuré : Mise à jour automatique des dépendances

#### 🧪 Tests
- **16 nouveaux tests** : Tests complets pour exporteurs externes (REST API, Google Sheets, Notion, Airtable)
- Couverture améliorée pour les exporteurs externes

#### 📝 Documentation
- Guide d'utilisation mis à jour avec toutes les nouvelles fonctionnalités
- FAQ enrichie (GitHub API, notifications, Git, export REST)
- API documentation mise à jour
- **Référence Métriques** : Nouveau document `docs/METRICS_REFERENCE.md`
- **Audit Complet 2025** : Analyse exhaustive du projet
- **CONTRIBUTORS.md** : Fichier créé pour reconnaître les contributeurs

## [1.0.0] - 2025-09-13

### 🎉 Version Initiale - Production Ready

#### ✨ Ajouts
- **Core Features**
  - 📊 Collecteur de métriques Python automatique
  - 🎨 Export multi-format : JSON, Markdown, HTML, CSV
  - 🌐 Dashboard web interactif avec TailwindCSS
  - 🔧 Interface CLI professionnelle (`collect`, `validate`, `serve`)
  - 🛡️ Exclusions intelligentes automatiques (venv, cache, node_modules)

- **Architecture Technique**
  - 🏗️ Modules séparés : collectors, exporters, validators, cli
  - ✅ 120 tests automatisés avec couverture complète
  - 🔒 Sécurité validée : 0 vulnérabilité (Bandit scan)
  - 🎯 Support Python 3.8, 3.9, 3.10, 3.11, 3.12
  - 🌍 Compatible Windows, macOS, Linux

- **Documentation Complète**
  - 📚 Guide utilisateur et développeur
  - 🔒 Politique de sécurité et confidentialité
  - 🤝 Guide de contribution détaillé
  - ❓ FAQ avec 20+ questions/réponses
  - 💡 Exemples d'utilisation et templates

- **CI/CD & Qualité**
  - 🚀 4 workflows GitHub Actions complets
  - 🎨 Formatage automatique (Black, Ruff)
  - 📋 Validation des types (MyPy)
  - 🔍 Tests multi-plateforme et multi-version Python
  - 📈 Rapports de couverture automatiques

#### 🎯 Métriques Collectées
- Fichiers Python (core vs tests)
- Lignes de code totales
- Tests détectés via pytest
- Documentation (Markdown, RST, HTML)
- Structure des projets

#### 🏆 Projets Validés
- ✅ Athalia Core (Framework IA)
- ✅ Arkalia Quest (Jeu éducatif)
- ✅ BBIA Simulation (Robotique)
- ✅ Auto-test sur arkalia-metrics-collector

### 🔮 Prochaines Versions

#### [1.2.0] - Prévu Q2 2025
- 📓 Support Jupyter Notebooks
- 🚀 Support langage Go
- 💾 Stockage persistant des métriques
- 📊 Métriques de complexité cyclomatique

#### [1.3.0] - Prévu Q3 2025
- ⚙️ Support Rust
- 🤖 Intégrations CI/CD avancées
- 🔌 Système de plugins extensible

---

## 📋 Format des Versions

- **Major** (X.0.0) : Changements incompatibles
- **Minor** (0.X.0) : Nouvelles fonctionnalités compatibles
- **Patch** (0.0.X) : Corrections de bugs

## 🎯 Types de Changements

- **✨ Ajouts** : Nouvelles fonctionnalités
- **🔧 Modifications** : Changements de fonctionnalités existantes
- **🗑️ Suppressions** : Fonctionnalités supprimées
- **🐛 Corrections** : Corrections de bugs
- **🔒 Sécurité** : Correctifs de sécurité
- **📚 Documentation** : Améliorations de la documentation
- **⚡ Performance** : Améliorations de performance

---

**🚀 [Voir toutes les releases](https://github.com/arkalia-luna-system/arkalia-metrics-collector/releases)**
