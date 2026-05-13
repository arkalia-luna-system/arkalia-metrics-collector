# 📋 RÉSUMÉ DES WORKFLOWS GITHUB ACTIONS

## **🚀 WORKFLOWS ACTIFS**

### **1. CI (`ci.yml`)**
- **Objectif** : Tests multi-plateforme, qualité, sécurité, build
- **Permissions** : `contents: read` uniquement
- **Déclencheurs** : Push sur main/develop, PR, manuel
- **Pas de déploiement GitHub Pages**

### **2. GitHub Pages (`gh-pages.yml`)**
- **Objectif** : Déploiement automatique de la documentation
- **Permissions** : `contents: read`, `pages: write`, `id-token: write`
- **Déclencheurs** : Push sur main/develop, PR, manuel
- **Utilise** : `actions/deploy-pages@v4`

### **3. Test GitHub Pages (`test-pages.yml`)**
- **Objectif** : Test simple de GitHub Pages
- **Permissions** : `contents: read`, `pages: write`, `id-token: write`
- **Déclencheurs** : Manuel uniquement
- **Utilise** : `actions/deploy-pages@v4`

### **4. Sécurité (`security.yml`)**
- **Objectif** : Scan de sécurité automatisé
- **Permissions** : `contents: read`, `security-events: write`
- **Déclencheurs** : Push sur main/develop, PR, manuel
- **Pas de déploiement GitHub Pages**

## **🔒 PERMISSIONS PAR WORKFLOW**

| Workflow | contents | pages | id-token | security-events |
|----------|----------|-------|----------|-----------------|
| CI | ✅ read | ❌ | ❌ | ❌ |
| GitHub Pages | ✅ read | ✅ write | ✅ write | ❌ |
| Test Pages | ✅ read | ✅ write | ✅ write | ❌ |
| Sécurité | ✅ read | ❌ | ❌ | ✅ write |

## **🎯 RÉPARTITION DES RESPONSABILITÉS**

- **CI** : Tests, qualité, build (pas de déploiement)
- **GitHub Pages** : Documentation en ligne
- **Test Pages** : Test de GitHub Pages
- **Sécurité** : Audit de sécurité

## **⚠️ POINTS D'ATTENTION**

1. **Pas de conflit de permissions** entre workflows
2. **GitHub Pages** géré uniquement par les workflows dédiés
3. **CI/CD** se concentre sur la qualité et les tests
4. **Sécurité** indépendante des autres workflows

## **🚀 UTILISATION**

- **Développement normal** : CI + Sécurité
- **Documentation** : GitHub Pages automatique
- **Test GitHub Pages** : Manuel si nécessaire
