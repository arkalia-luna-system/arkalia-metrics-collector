# 🔍 Collectors

## MetricsCollector

Classe principale pour la collecte de métriques sur les projets Python.

### Constructeur

```python
MetricsCollector(project_root: Union[str, Path])
```

**Paramètres :**
- `project_root` : Chemin vers le projet à analyser (string ou Path)

### Attributs

- `project_root` : Chemin racine du projet
- `exclude_patterns` : Patterns d'exclusion (set)
- `metrics_data` : Données collectées (dict)

### Méthodes principales

#### collect_all_metrics()

Collecte toutes les métriques du projet.

**Retour :** `dict` - Dictionnaire complet des métriques

**Exemple :**
```python
collector = MetricsCollector("./mon-projet")
metrics = collector.collect_all_metrics()
```

#### collect_python_metrics()

Collecte les métriques sur les fichiers Python.

**Retour :** `dict` avec :
- `count` : Nombre total de fichiers Python
- `core_files` : Nombre de fichiers de code
- `test_files` : Nombre de fichiers de test
- `total_lines` : Nombre total de lignes
- `files_list` : Liste des fichiers Python

#### collect_test_metrics()

Collecte les métriques sur les tests.

**Retour :** `dict` avec :
- `collected_tests_count` : Nombre de tests détectés
- `test_files_count` : Nombre de fichiers de test
- `test_files` : Liste des fichiers de test

#### collect_documentation_metrics()

Collecte les métriques sur la documentation.

**Retour :** `dict` avec :
- `documentation_files` : Nombre de fichiers de documentation
- `documentation_list` : Liste des fichiers de documentation

### Méthodes utilitaires

#### _is_excluded(path: Path) -> bool

Vérifie si un chemin doit être exclu de l'analyse.

**Paramètres :**
- `path` : Chemin à vérifier

**Retour :** `bool` - True si le chemin doit être exclu

#### _is_test_file(path: Path) -> bool

Détermine si un fichier est un fichier de test.

**Paramètres :**
- `path` : Chemin du fichier

**Retour :** `bool` - True si c'est un fichier de test

### Configuration des exclusions

Par défaut, les patterns suivants sont exclus :
- `__pycache__` : Cache Python
- `.venv`, `venv` : Environnements virtuels
- `.git` : Dossier Git
- `.pytest_cache` : Cache pytest
- `._*` : Fichiers système macOS

**Ajouter des exclusions :**
```python
collector = MetricsCollector("./mon-projet")
collector.exclude_patterns.add("*.tmp")
collector.exclude_patterns.add("backup/")
```

### Gestion des erreurs

Le collecteur gère automatiquement :
- Fichiers non lisibles (encodage, permissions)
- Chemins invalides
- Erreurs de lecture de fichiers

**Exemple de gestion d'erreur :**
```python
try:
    metrics = collector.collect_all_metrics()
except Exception as e:
    print(f"Erreur lors de la collecte : {e}")
```

### Performance

- **Optimisé** pour les gros projets
- **Exclusion intelligente** des dossiers système
- **Détection automatique** des fichiers de test
- **Comptage efficace** des lignes de code
