# Validation des métriques

## Validation basique

```python
from arkalia_metrics_collector import MetricsValidator

validator = MetricsValidator()
is_valid, errors, warnings = validator.validate_metrics(metrics_data)

if is_valid:
    print("✅ Métriques valides!")
else:
    print(f"❌ {len(errors)} erreurs détectées")
```
