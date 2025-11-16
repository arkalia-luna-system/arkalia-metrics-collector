# 🌐 Configuration GitHub Pages - Arkalia Metrics Collector

## **📋 PRÉREQUIS**

Pour que le workflow GitHub Pages fonctionne, vous devez **activer GitHub Pages** dans les paramètres de votre repository.

## **🔧 ÉTAPES D'ACTIVATION**

### **1. Aller dans les paramètres du repository**
- Ouvrez votre repository : `https://github.com/arkalia-luna-system/arkalia-metrics-collector`
- Cliquez sur l'onglet **"Settings"** (⚙️)

### **2. Activer GitHub Pages**
- Dans le menu de gauche, cliquez sur **"Pages"**
- Dans la section **"Source"**, sélectionnez **"GitHub Actions"**
- Cliquez sur **"Save"**

### **3. Vérifier les permissions**
- Assurez-vous que le repository a les permissions nécessaires :
  - `contents: read`
  - `pages: write`
  - `id-token: write`

## **🚀 WORKFLOW AUTOMATIQUE**

Une fois GitHub Pages activé, le workflow `.github/workflows/gh-pages.yml` s'exécutera automatiquement :

- **Sur push** vers `main` ou `develop`
- **Sur pull request** vers `main`
- **Manuellement** via `workflow_dispatch`

## **📊 PROCESSUS DE DÉPLOIEMENT**

1. **Build** : Construction de la documentation avec MkDocs
2. **Vérification** : Contrôle des artifacts générés
3. **Upload** : Téléchargement des fichiers vers GitHub
4. **Déploiement** : Publication sur GitHub Pages

## **🌐 URL FINALE**

Votre documentation sera accessible à :
```
https://arkalia-luna-system.github.io/arkalia-metrics-collector/
```

## **⚠️ DÉPANNAGE**

### **Erreur "Not Found"**
- Vérifiez que GitHub Pages est activé
- Assurez-vous que la source est "GitHub Actions"

### **Erreur de permissions**
- Vérifiez les permissions du workflow
- Assurez-vous que le repository est public ou que vous avez les droits

### **Build échoue**
- Vérifiez les logs du workflow
- Assurez-vous que MkDocs fonctionne localement

## **📞 SUPPORT**

Si vous rencontrez des problèmes :
1. Vérifiez les logs des Actions GitHub
2. Consultez la documentation GitHub Pages
3. Vérifiez que tous les workflows sont à jour

---

**🎯 Objectif : Avoir une documentation professionnelle accessible en ligne !**
