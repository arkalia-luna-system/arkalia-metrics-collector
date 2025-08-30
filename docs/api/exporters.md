# 📤 Exporters

## MetricsExporter

Classe pour l'export des métriques dans différents formats.

### Constructeur

```python
MetricsExporter(metrics_data: dict[str, Any])
```

**Paramètres :**
- `metrics_data` : Données des métriques à exporter

### Méthodes d'export

#### export_json(output_path: str) -> bool

Exporte les métriques au format JSON.

**Paramètres :**
- `output_path` : Chemin du fichier de sortie

**Retour :** `bool` - True si l'export a réussi

**Exemple :**
```python
exporter = MetricsExporter(metrics_data)
success = exporter.export_json("metrics.json")
```

#### export_markdown_summary(output_path: str) -> bool

Exporte un résumé des métriques au format Markdown.

**Paramètres :**
- `output_path` : Chemin du fichier de sortie

**Retour :** `bool` - True si l'export a réussi

**Format généré :**
```markdown
## 📊 Métriques du Projet

- **Fichiers Python** : 25 fichiers
- **Lignes de code** : 1,500 lignes
- **Tests** : 45 tests
- **Documentation** : 3 fichiers
```

#### export_html_dashboard(output_path: str) -> bool

Exporte un dashboard HTML interactif.

**Paramètres :**
- `output_path` : Chemin du fichier de sortie

**Retour :** `bool` - True si l'export a réussi

**Caractéristiques :**
- Design moderne avec Tailwind CSS
- Interface responsive
- Métriques visuelles
- Navigation intuitive

#### export_csv(output_path: str) -> bool

Exporte les métriques au format CSV.

**Paramètres :**
- `output_path` : Chemin du fichier de sortie

**Retour :** `bool` - True si l'export a réussi

**Format généré :**
```csv
Métrique,Valeur,Unité

Fichiers Python,25,fichiers
Lignes de Code,1500,lignes
Tests,45,tests
Documentation,3,fichiers

Date de collecte,2024-01-01T00:00:00,
Version collecteur,1.0.0,
```

#### export_all_formats(output_dir: str = "metrics") -> dict[str, bool]

Exporte dans tous les formats disponibles.

**Paramètres :**
- `output_dir` : Dossier de sortie (défaut: "metrics")

**Retour :** `dict[str, bool]` - Résultat pour chaque format

**Exemple :**
```python
results = exporter.export_all_formats("output/")
# Retourne : {"json": True, "markdown": True, "html": True, "csv": True}
```

### Gestion des erreurs

L'exporteur gère automatiquement :
- Création des dossiers de sortie
- Erreurs d'écriture de fichiers
- Données manquantes ou invalides

**Exemple de gestion d'erreur :**
```python
try:
    success = exporter.export_json("metrics.json")
    if success:
        print("✅ Export réussi")
    else:
        print("❌ Export échoué")
except Exception as e:
    print(f"Erreur lors de l'export : {e}")
```

### Personnalisation des exports

#### Template Markdown personnalisé

```python
# Créer un template personnalisé
custom_template = """
# Métriques de {project_name}

## Résumé
- Fichiers Python : {python_files}
- Lignes de code : {lines_of_code}
- Tests : {tests}
- Documentation : {documentation}

## Détails
{details}
"""

# Utiliser le template (extension future)
# exporter.export_custom_markdown("custom.md", template=custom_template)
```

#### Format CSV personnalisé

```python
# Ajouter des colonnes personnalisées
custom_columns = [
    "Métrique",
    "Valeur",
    "Unité",
    "Pourcentage",
    "Tendance"
]

# Utiliser les colonnes personnalisées (extension future)
# exporter.export_custom_csv("custom.csv", columns=custom_columns)
```

### Formats de sortie

#### JSON
- **Avantages** : Structuré, facile à parser
- **Utilisation** : API, intégration, analyse programmatique

#### Markdown
- **Avantages** : Lisible, compatible GitHub, documentation
- **Utilisation** : README, documentation, rapports

#### HTML
- **Avantages** : Interactif, visuel, navigation
- **Utilisation** : Dashboards, présentations, web

#### CSV
- **Avantages** : Compatible Excel, analyse de données
- **Utilisation** : Rapports, analyse, import dans d'autres outils

### Intégration avec d'autres outils

#### GitHub Actions
```yaml
- name: Export Metrics
  run: |
    arkalia-metrics collect . --format all --output metrics/
    # Les métriques sont maintenant disponibles dans metrics/
```

#### CI/CD
```bash
# Collecter et exporter
arkalia-metrics collect . --format json --output artifacts/

# Utiliser dans le pipeline
python -c "
import json
with open('artifacts/metrics.json') as f:
    metrics = json.load(f)
    print(f'Tests: {metrics[\"summary\"][\"collected_tests\"]}')
"
```

#### Monitoring
```python
# Collecter des métriques périodiquement
import schedule
import time

def export_metrics():
    collector = MetricsCollector("./mon-projet")
    metrics = collector.collect_all_metrics()
    
    exporter = MetricsExporter(metrics)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    exporter.export_json(f"metrics_{timestamp}.json")

# Planifier l'export toutes les heures
schedule.every().hour.do(export_metrics)

while True:
    schedule.run_pending()
    time.sleep(60)
```
