# 📤 Export Personnalisé

Guide pour exporter vos métriques dans différents formats.

## 🎯 Export Multi-Format

Exportez vos métriques dans tous les formats disponibles (JSON, Markdown, HTML, CSV, YAML) :

```python
from arkalia_metrics_collector import MetricsCollector, MetricsExporter

collector = MetricsCollector(".")
metrics = collector.collect_all_metrics()

exporter = MetricsExporter(metrics)
results = exporter.export_all_formats("output/")

for format, success in results.items():
    print(f"{format}: {'✅' if success else '❌'}")
```

## 📋 Formats Disponibles

- **JSON** : Structure complète pour intégration
- **Markdown** : Documentation formatée
- **HTML** : Dashboard interactif
- **CSV** : Analyse dans Excel/Sheets
- **YAML** : Configuration et scripts
