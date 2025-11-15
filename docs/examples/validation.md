# ✅ Validation des Métriques

Guide pour valider la qualité et la cohérence de vos métriques collectées.

## 🔍 Validation Basique

```python
from arkalia_metrics_collector import MetricsValidator

validator = MetricsValidator()
is_valid, errors, warnings = validator.validate_metrics(metrics_data)

if is_valid:
    print("✅ Métriques valides!")
else:
    print(f"❌ {len(errors)} erreurs détectées")
    for error in errors:
        print(f"  - {error}")
```

## 📊 Rapport Détaillé

Obtenez un rapport complet avec score de validation :

```python
report = validator.get_validation_report()
print(f"Score: {report['validation_summary']['score']}/100")
```
