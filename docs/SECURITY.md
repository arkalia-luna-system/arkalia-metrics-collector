# 🔒 Security Policy

## 🛡️ Sécurité et Confidentialité

### Ce qui est collecté ✅

**Arkalia Metrics Collector** ne collecte que des **métriques techniques publiques** :

- 📊 **Métadonnées de fichiers** : nombre, extensions, lignes de code
- 🧪 **Résultats de tests** : nombre de tests, couverture (sans le contenu)
- 📚 **Statistiques documentation** : nombre et types de fichiers
- 🏗️ **Structure du projet** : arborescence des dossiers (pas le contenu)

### Ce qui n'est JAMAIS collecté ❌

- ❌ **Code source** ou contenu des fichiers
- ❌ **Données personnelles** ou informations sensibles
- ❌ **Secrets, clés API** ou variables d'environnement
- ❌ **Historique Git** ou informations de commits
- ❌ **Données réseau** ou informations système
- ❌ **Fichiers de configuration** avec des valeurs

### 🔐 Exclusions Automatiques

Le collecteur **exclut automatiquement** :

```
- .env, .venv, venv/         # Variables d'environnement
- .git/                      # Historique Git
- __pycache__/               # Cache Python
- node_modules/              # Dépendances JS
- .pytest_cache/            # Cache de tests
- htmlcov/                   # Rapports de couverture
- logs/                      # Fichiers de logs
```

### 🚨 Signaler une Vulnérabilité

Si vous découvrez une vulnérabilité de sécurité :

1. **NE PAS** créer d'issue publique
2. **Envoyez un email** à : `security@arkalia-luna.com`
3. **Incluez** :
   - Description détaillée de la vulnérabilité
   - Étapes pour reproduire le problème
   - Impact potentiel
   - Version affectée

### ⏱️ Temps de Réponse

- **Accusé de réception** : 24-48 heures
- **Évaluation initiale** : 72 heures
- **Correction** : 7-14 jours selon la criticité

### 🏆 Reconnaissance

Les chercheurs en sécurité qui signalent des vulnérabilités responsables seront mentionnés dans :
- Fichier `CREDITS.md`
- Release notes de la version corrigée
- Page de remerciements (si souhaité)

### 📋 Versions Supportées

| Version | Support Sécurité |
|---------|------------------|
| 1.0.x   | ✅ Support complet |
| 0.9.x   | ⚠️ Correctifs critiques uniquement |
| < 0.9   | ❌ Non supporté |

### 🔍 Audit de Sécurité

- **Bandit** : Scan automatique à chaque commit
- **Safety** : Vérification des dépendances
- **Pip-audit** : Audit des packages installés
- **GitHub Dependabot** : Alertes de sécurité automatiques

---

**Merci de nous aider à maintenir Arkalia Metrics Collector sécurisé ! 🛡️**
