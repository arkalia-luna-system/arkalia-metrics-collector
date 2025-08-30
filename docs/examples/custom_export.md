# Export personnalisé

## Export dans tous les formats

```python
from arkalia_metrics_collector import MetricsCollector, MetricsExporter

collector = MetricsCollector(".")
metrics = collector.collect_all_metrics()

exporter = MetricsExporter(metrics)
results = exporter.export_all_formats("output/")

for format, success in results.items():
    print(f"{format}: {\"✅\" if success else \"❌\"}")
```
