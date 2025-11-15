# 📦 Collecte Basique

Guide rapide pour démarrer avec Arkalia Metrics Collector.

## 🚀 Exemple Simple

```python
from arkalia_metrics_collector import MetricsCollector

collector = MetricsCollector(".")
metrics = collector.collect_all_metrics()
print(f"Fichiers Python: {metrics[\"summary\"][\"total_python_files\"]}")
```

## 📊 Résultat

Après exécution, vous obtenez un dictionnaire complet avec toutes les métriques de votre projet.
