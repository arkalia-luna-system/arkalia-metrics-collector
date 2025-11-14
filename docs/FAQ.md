# ❓ FAQ - Questions Fréquentes

## 🚀 Installation & Usage

### Q: Comment installer Arkalia Metrics Collector ?

**A:** Deux options :

```bash
# Option 1: Depuis le repository (recommandé actuellement)
git clone https://github.com/arkalia-luna-system/arkalia-metrics-collector.git
cd arkalia-metrics-collector
pip install -e .

# Option 2: Via PyPI (bientôt disponible)
pip install arkalia-metrics-collector
```

### Q: Quelle version de Python est requise ?

**A:** Python 3.8+ est requis. Testé sur Python 3.8, 3.9, 3.10, 3.11 et 3.12.

### Q: Ça fonctionne sur Windows/macOS/Linux ?

**A:** ✅ Oui ! Testé automatiquement sur les 3 plateformes via GitHub Actions.

## 🧪 Tests et Validation

### Q: Combien de tests y a-t-il ?

**A:** **120 tests** au total :
- **50+ tests unitaires** : Fonctionnalités individuelles
- **16+ tests d'intégration** : Projets externes et validation
- **15+ tests de performance** : Vitesse et mémoire
- **32+ tests CLI** : Interface en ligne de commande

### Q: Les tests couvrent-ils tous les cas d'usage ?

**A:** ✅ Oui ! Les tests couvrent :
- Projets de différentes tailles (petit, moyen, grand)
- Tous les formats d'export (JSON, Markdown, HTML, CSV)
- Validation des métriques et cohérence
- Gestion d'erreurs et cas limites
- Performance et utilisation mémoire
- Interface CLI complète

### Q: Comment exécuter les tests ?

**A:** Plusieurs options :

```bash
# Tous les tests
pytest tests/ -v

# Par catégorie
pytest tests/unit/ -v                    # Tests unitaires
pytest tests/integration/ -v             # Tests d'intégration
pytest tests/performance/ -v             # Tests de performance

# Avec couverture
pytest tests/ --cov=src/ --cov-report=html
```

### Q: Les tests valident-ils les projets externes ?

**A:** ✅ Oui ! Les tests d'intégration incluent :
- Tests sur projets simulés de différentes tailles
- Validation des métriques collectées
- Tests d'export sur projets externes
- Mesures de performance
- Gestion d'erreurs avec projets invalides

## 📊 Formats et Compatibilité

### Q: Quels formats d'export sont supportés ?

**A:** 4 formats disponibles :
- **JSON** : Données complètes pour intégration
- **Markdown** : Pour README et documentation
- **HTML** : Dashboard interactif
- **CSV** : Pour analyse dans Excel/Google Sheets

### Q: Est-ce compatible avec mon type de projet Python ?

**A:** ✅ Compatible avec :
- Projets Django/Flask
- Packages Python (setuptools, poetry, flit)
- Scripts simples
- Projets de data science (Jupyter notebooks exclus par défaut)
- Applications CLI
- APIs et microservices

### Q: Ça marche avec Poetry/Pipenv ?

**A:** ✅ Oui ! Le collecteur analyse la structure, pas le gestionnaire de dépendances.

## 🔧 Configuration

### Q: Comment exclure des dossiers spécifiques ?

**A:** Créez un fichier `arkalia-metrics.yaml` :

```yaml
exclusions:
  - "**/mon_dossier_prive/**"
  - "**/data/**"
  - "**/models/**"
```

### Q: Puis-je collecter seulement certaines métriques ?

**A:** Pas encore directement, mais c'est prévu ! Actuellement toutes les métriques sont collectées.

### Q: Comment configurer pour un projet monorepo ?

**A:** Lancez le collecteur sur chaque sous-projet :

```bash
arkalia-metrics collect ./frontend --output metrics/frontend
arkalia-metrics collect ./backend --output metrics/backend
arkalia-metrics collect ./shared --output metrics/shared
```

## 🛡️ Sécurité & Confidentialité

### Q: Mes données sont-elles sécurisées ?

**A:** ✅ **Aucun code source n'est collecté !** Seulement les métadonnées :
- Nombre de fichiers/lignes
- Résultats de tests (pas le contenu)
- Structure des dossiers
- Voir [SECURITY.md](SECURITY.md) pour plus de détails

### Q: Que faire si j'ai des fichiers sensibles ?

**A:** Ils sont automatiquement exclus (`.env`, `.git`, etc.) ou ajoutez-les dans la configuration :

```yaml
exclusions:
  - "**/secrets/**"
  - "**/private/**"
```

## 🐛 Résolution de Problèmes

### Q: "Aucun fichier Python détecté" mais j'en ai !

**A:** Vérifiez :
1. Vous êtes dans le bon dossier
2. Les fichiers ne sont pas dans `.venv/` ou `__pycache__/`
3. Utilisez `--verbose` pour voir ce qui est exclu

### Q: Les tests ne sont pas détectés

**A:** Vérifiez que vos tests :
- Sont dans un dossier `tests/`
- Ont des noms comme `test_*.py` ou `*_test.py`
- Sont détectables par pytest

### Q: Erreur "Permission denied"

**A:** Sur certains projets, lancez avec les bonnes permissions :

```bash
# Linux/macOS
sudo arkalia-metrics collect .

# Ou changez les permissions
chmod -R 755 mon_projet/
```

### Q: Le collecteur est lent sur mon gros projet

**A:** Optimisations disponibles :
- Excluez les gros dossiers (data, models, logs)
- Utilisez un SSD pour de meilleures performances
- Version future : collecte parallèle

## 🎯 Cas d'Usage

### Q: Comment utiliser dans un pipeline CI/CD ?

**A:** Ajoutez dans votre workflow :

```yaml
- name: Collect metrics
  run: |
    pip install arkalia-metrics-collector
    arkalia-metrics collect . --format json --output metrics/
    
- name: Upload metrics
  uses: actions/upload-artifact@v3
  with:
    name: project-metrics
    path: metrics/
```

### Q: Comment comparer les métriques dans le temps ?

**A:** Sauvegardez les fichiers JSON avec timestamps :

```bash
arkalia-metrics collect . --output "metrics/$(date +%Y-%m-%d)"
```

### Q: Comment intégrer dans un dashboard existant ?

**A:** Utilisez l'export JSON :

```python
import json
with open('metrics/metrics.json') as f:
    metrics = json.load(f)
    
# Intégrez dans votre dashboard
python_files = metrics['summary']['total_python_files']
```

## 🔮 Fonctionnalités Futures

### Q: Support d'autres langages prévu ?

**A:** 🎯 Oui ! Roadmap :
- JavaScript/TypeScript (v1.1)
- Go (v1.2)
- Rust (v1.3)

### Q: API REST prévue ?

**A:** 🎯 En développement pour v1.1 :
- Endpoint `/metrics`
- Webhook pour CI/CD
- Dashboard temps réel

### Q: Support des notebooks Jupyter ?

**A:** 🎯 Prévu pour v1.2 avec métriques spécialisées.

## 💬 Support

### Q: Où obtenir de l'aide ?

**A:** Plusieurs options :
1. **Issues GitHub** : [github.com/arkalia-luna-system/arkalia-metrics-collector/issues](https://github.com/arkalia-luna-system/arkalia-metrics-collector/issues)
2. **Discussions** : Pour questions générales
3. **Email** : `arkalia.luna.system@gmail.com`

### Q: Comment signaler un bug ?

**A:** Créez une issue avec :
- Version Python et OS
- Commande exacte utilisée
- Message d'erreur complet
- Structure de votre projet (si possible)

### Q: Comment proposer une nouvelle fonctionnalité ?

**A:** 
1. Vérifiez qu'elle n'existe pas déjà
2. Créez une issue avec le tag "enhancement"
3. Décrivez le cas d'usage et l'impact attendu

---

**Cette FAQ répond-elle à votre question ? Sinon, n'hésitez pas à [créer une issue](https://github.com/arkalia-luna-system/arkalia-metrics-collector/issues) ! 🚀**
