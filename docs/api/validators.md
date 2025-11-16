# ✅ API Reference - Validators

Documentation complète des validateurs de métriques d'**Arkalia Metrics Collector**.

## 🎯 Vue d'ensemble

Les validateurs permettent de vérifier la qualité, la cohérence et la validité des métriques collectées.

## 📦 MetricsValidator

Classe principale pour la validation des métriques collectées.

### Constructeur

```python
MetricsValidator()
```

**Aucun paramètre requis** - Configuration par défaut

### Attributs

- `validation_errors` : Liste des erreurs de validation
- `validation_warnings` : Liste des avertissements de validation

### Méthodes principales

#### validate_metrics(metrics_data: dict[str, Any]) -> tuple[bool, list[str], list[str]]

Valide les métriques collectées.

**Paramètres :**
- `metrics_data` : Données des métriques à valider

**Retour :** `tuple[bool, list[str], list[str]]` - (is_valid, errors, warnings)

**Exemple :**
```python
validator = MetricsValidator()
is_valid, errors, warnings = validator.validate_metrics(metrics_data)

if is_valid:
    print("✅ Métriques valides!")
else:
    print(f"❌ {len(errors)} erreurs détectées")
```

#### get_validation_report() -> dict[str, Any]

Génère un rapport de validation détaillé.

**Retour :** `dict` avec :
- `errors` : Liste des erreurs
- `warnings` : Liste des avertissements
- `validation_summary` : Résumé avec score et statut

**Exemple :**
```python
report = validator.get_validation_report()
print(f"Score: {report['validation_summary']['score']}/100")
print(f"Statut: {report['validation_summary']['status']}")
```

### Règles de validation

#### Structure des métriques

**Clés requises :**
- `timestamp` : Horodatage de la collecte
- `project_root` : Chemin racine du projet
- `collection_info` : Informations sur la collecte
- `python_files` : Métriques des fichiers Python
- `test_metrics` : Métriques des tests
- `documentation_metrics` : Métriques de la documentation
- `summary` : Résumé des métriques

**Informations de collection requises :**
- `collector_version` : Version du collecteur
- `python_version` : Version Python utilisée
- `collection_date` : Date de collecte

#### Cohérence des données

**Validation Python :**
- `core_files + test_files == count` (cohérence du comptage)
- `total_lines > 0` si `count > 0` (lignes de code présentes)

**Validation des tests :**
- `test_files_count == python_test_files` (cohérence du comptage)
- `collected_tests_count >= 0` (nombre de tests non négatif)

**Validation de la documentation :**
- `documentation_files >= 0` (nombre de fichiers non négatif)

**Validation du résumé :**
- `total_python_files` cohérent avec `python_files.count`
- `lines_of_code` cohérent avec `python_files.total_lines`
- `collected_tests` cohérent avec `test_metrics.collected_tests_count`

### Messages d'erreur et d'avertissement

#### Erreurs (validation_errors)

**Structure :**
- `"Clé manquante: {key}"` : Clé requise manquante
- `"Nombre de fichiers Python manquant"` : Métrique Python manquante
- `"Incohérence dans le comptage des fichiers: {core} + {test} != {count}"` : Comptage incohérent
- `"Incohérence dans le comptage des tests: {count} != {python_count}"` : Tests incohérents
- `"Nombre de tests négatif: {count}"` : Valeur négative
- `"Nombre de fichiers de documentation négatif: {count}"` : Valeur négative
- `"Incohérence dans le résumé: {expected} != {actual}"` : Résumé incohérent

#### Avertissements (validation_warnings)

**Structure :**
- `"Info de collection manquante: {key}"` : Information optionnelle manquante
- `"Fichiers Python détectés mais 0 lignes de code"` : Problème potentiel
- `"Aucun fichier Python détecté"` : Projet vide
- `"Aucun fichier de documentation détecté"` : Documentation manquante

### Score de validation

Le score est calculé automatiquement :
- **Base** : 100 points
- **Erreur** : -10 points par erreur
- **Avertissement** : -2 points par avertissement
- **Minimum** : 0 points

**Statuts :**
- `"✅ VALID"` : Score = 100, aucune erreur
- `"❌ INVALID"` : Score < 100, erreurs détectées

### Exemples d'utilisation

#### Validation basique

```python
from arkalia_metrics_collector import MetricsValidator

validator = MetricsValidator()
is_valid, errors, warnings = validator.validate_metrics(metrics_data)

print(f"Valid: {is_valid}")
print(f"Erreurs: {len(errors)}")
print(f"Avertissements: {len(warnings)}")
```

#### Validation avec rapport

```python
validator = MetricsValidator()
validator.validate_metrics(metrics_data)
report = validator.get_validation_report()

print("=== RAPPORT DE VALIDATION ===")
print(f"Score: {report['validation_summary']['score']}/100")
print(f"Statut: {report['validation_summary']['status']}")

if report['errors']:
    print("\n❌ ERREURS:")
    for error in report['errors']:
        print(f"  - {error}")

if report['warnings']:
    print("\n⚠️ AVERTISSEMENTS:")
    for warning in report['warnings']:
        print(f"  - {warning}")
```

#### Validation dans un pipeline

```python
def validate_project_metrics(project_path: str) -> bool:
    """Valide les métriques d'un projet."""
    try:
        # Collecter les métriques
        collector = MetricsCollector(project_path)
        metrics = collector.collect_all_metrics()
        
        # Valider
        validator = MetricsValidator()
        is_valid, errors, warnings = validator.validate_metrics(metrics)
        
        # Afficher le rapport
        if not is_valid:
            print(f"❌ Projet {project_path} invalide:")
            for error in errors:
                print(f"  - {error}")
        
        return is_valid
        
    except Exception as e:
        print(f"❌ Erreur lors de la validation: {e}")
        return False

# Utilisation
projects = ["./projet1", "./projet2", "./projet3"]
for project in projects:
    if validate_project_metrics(project):
        print(f"✅ {project} validé")
    else:
        print(f"❌ {project} invalide")
```

### Intégration avec d'autres composants

#### Collecteur + Validateur

```python
# Collecter et valider en une fois
collector = MetricsCollector("./mon-projet")
validator = MetricsValidator()

# Collecter
metrics = collector.collect_all_metrics()

# Valider immédiatement
is_valid, errors, warnings = validator.validate_metrics(metrics)

if is_valid:
    print("✅ Métriques collectées et validées!")
else:
    print("❌ Métriques collectées mais invalides")
```

#### Exporteur + Validateur

```python
# Valider avant l'export
validator = MetricsValidator()
is_valid, errors, warnings = validator.validate_metrics(metrics_data)

if is_valid:
    # Exporter seulement si valide
    exporter = MetricsExporter(metrics_data)
    exporter.export_all_formats("output/")
    print("✅ Export réussi!")
else:
    print("❌ Export annulé - métriques invalides")
```

### Personnalisation future

**Règles personnalisées :**
- Seuils de qualité configurables
- Règles métier spécifiques
- Validation conditionnelle

**Extensions :**
- Validation de schémas JSON
- Règles de qualité de code
- Métriques de performance
