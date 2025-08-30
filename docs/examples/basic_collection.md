# Collecte basique
## Exemple simple

```python
from arkalia_metrics_collector import MetricsCollector

collector = MetricsCollector(".")
metrics = collector.collect_all_metrics()
print(f"Fichiers Python: {metrics[\"summary\"][\"total_python_files\"]}")
```
