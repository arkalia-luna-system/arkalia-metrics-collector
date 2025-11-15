# 🎨 Guide du Dashboard Interactif

Le dashboard interactif d'**Arkalia Metrics Collector** offre une visualisation complète et interactive de vos métriques avec des graphiques, tableaux et export de données.

## 🎯 Vue d'ensemble

Le dashboard permet de :
- 📊 Visualiser les métriques avec des graphiques Chart.js
- 📈 Comparer l'évolution temporelle des métriques
- 🔍 Filtrer et rechercher dans les projets
- 📤 Exporter les données (JSON, CSV)
- 📱 Interface responsive et mobile-friendly

## 🚀 Génération du Dashboard

### Depuis la ligne de commande

```bash
# Générer un dashboard depuis des métriques agrégées
arkalia-metrics export metrics/aggregated_metrics.json --format html --output dashboard/

# Ou utiliser directement l'exporteur
arkalia-metrics collect /chemin/vers/projet --format html
```

### Depuis Python

```python
from arkalia_metrics_collector import MetricsExporter
import json

# Charger les métriques
with open("metrics/aggregated_metrics.json") as f:
    metrics = json.load(f)

# Générer le dashboard
exporter = MetricsExporter(metrics)
exporter.export_html_dashboard("dashboard.html")
```

## 📈 Fonctionnalités du Dashboard

### 1. **Métriques Principales**

Le dashboard affiche quatre cartes principales :
- 📦 **Fichiers Python** : Nombre total de modules
- 📝 **Lignes de Code** : Total de lignes de code
- 🧪 **Tests** : Nombre total de tests
- 📚 **Documentation** : Fichiers de documentation

### 2. **Graphiques d'Évolution**

Si un historique est disponible, le dashboard génère automatiquement des graphiques Chart.js :

- **Évolution des Modules** : Graphique linéaire montrant la croissance des modules Python
- **Évolution des Lignes de Code** : Suivi de la croissance du code
- **Évolution des Tests** : Progression du nombre de tests
- **Vue d'Ensemble** : Graphique en barres comparant modules et tests

### 3. **Tableau Interactif des Projets**

Pour les métriques agrégées multi-projets :

- **Tri par colonne** : Cliquez sur les en-têtes pour trier
- **Filtre de recherche** : Recherchez un projet par nom
- **Colonnes** : Projet, Modules, Lignes, Tests, Coverage

### 4. **Export de Données**

Le dashboard permet d'exporter les métriques :
- **Export JSON** : Télécharge les métriques complètes en JSON
- **Export CSV** : Exporte un résumé en format CSV

## 🌐 Déploiement sur GitHub Pages

Le dashboard est automatiquement déployé sur GitHub Pages lors des mises à jour.

### Accès au Dashboard

Une fois déployé, le dashboard est accessible à :
```
https://arkalia-luna-system.github.io/arkalia-metrics-collector/dashboard/
```

### Génération Automatique

Le workflow GitHub Actions génère automatiquement le dashboard :
1. Lors des push sur `main` ou `develop`
2. Lors des mises à jour automatiques des métriques
3. Manuellement via `workflow_dispatch`

## 🔧 Configuration

### Personnaliser le Dashboard

Le dashboard peut être personnalisé en modifiant :
- `src/arkalia_metrics_collector/exporters/interactive_dashboard.py`
- Styles CSS dans le template HTML
- Configuration Chart.js pour les graphiques

### Historique des Métriques

Pour activer les graphiques d'évolution :
1. Assurez-vous que l'historique est activé lors de l'agrégation
2. Les métriques sont sauvegardées dans `metrics/history/`
3. Le dashboard charge automatiquement les 10 dernières entrées

## 📊 Exemple d'Utilisation

### Dashboard pour un Projet Unique

```bash
# Collecter les métriques
arkalia-metrics collect /chemin/vers/projet --output metrics/

# Générer le dashboard
arkalia-metrics export metrics/metrics.json --format html --output dashboard/
```

### Dashboard pour Projets Multiples

```bash
# Agréger les métriques
arkalia-metrics aggregate projects.json --json --output metrics/

# Générer le dashboard
arkalia-metrics export metrics/aggregated_metrics.json --format html --output dashboard/
```

## 🎨 Personnalisation Avancée

### Modifier les Couleurs

Les couleurs du dashboard sont définies avec Tailwind CSS. Modifiez les classes dans le template HTML :

```html
<!-- Exemple : Changer la couleur des modules -->
<div class="bg-gradient-to-br from-blue-600 to-blue-800">
```

### Ajouter des Graphiques

Pour ajouter de nouveaux graphiques, modifiez la méthode `_generate_charts_script` dans `interactive_dashboard.py`.

## 🐛 Dépannage

### Dashboard Vide

Si le dashboard est vide :
1. Vérifiez que les métriques sont chargées correctement
2. Vérifiez la console du navigateur pour les erreurs JavaScript
3. Assurez-vous que Chart.js est chargé correctement

### Graphiques Non Affichés

Si les graphiques ne s'affichent pas :
1. Vérifiez que l'historique existe dans `metrics/history/`
2. Vérifiez que les données historiques sont au bon format
3. Vérifiez la console pour les erreurs Chart.js

## 📚 Ressources

- [Documentation Chart.js](https://www.chartjs.org/docs/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [GitHub Pages](https://docs.github.com/en/pages)

