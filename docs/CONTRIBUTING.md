# 🤝 Guide de Contribution

Merci de votre intérêt pour **Arkalia Metrics Collector** ! Toutes les contributions sont les bienvenues.

## 🎯 Types de Contributions Recherchées

### 🐛 **Issues Faciles pour Débuter**
- Amélioration de la documentation
- Ajout d'exemples d'utilisation
- Tests sur nouveaux types de projets
- Traductions (anglais, espagnol, etc.)

### 🚀 **Features Recherchées**
- Support de nouveaux formats d'export (XML, YAML)
- Métriques de qualité avancées (complexité cyclomatique)
- Intégration avec d'autres outils (SonarQube, CodeClimate)
- Support d'autres langages (JavaScript, TypeScript)

### 🧪 **Tests et Validation**
- Tests sur différents OS (Windows, macOS, Linux)
- Tests avec des projets de grande taille (>10k fichiers)
- Benchmarks de performance
- Tests d'intégration avec CI/CD
- Tests sur projets externes réels
- Validation des outputs en production

## 🛠️ Comment Contribuer

### 1. **Setup de Développement**

```bash
# Cloner le projet
git clone https://github.com/arkalia-luna-system/arkalia-metrics-collector.git
cd arkalia-metrics-collector

# Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# ou .venv\Scripts\activate  # Windows

# Installer en mode développement
pip install -e ".[dev]"
```

### 2. **Processus de Développement**

```bash
# Créer une branche pour votre feature
git checkout -b feature/ma-super-feature

# Développer votre feature
# ... vos modifications ...

# Vérifier la qualité du code
black .                    # Formatage
ruff check .              # Linting
mypy src/                 # Vérification des types
bandit -r src/            # Sécurité

# Lancer les tests
pytest tests/ -v --cov=arkalia_metrics_collector

# Tests spécifiques
pytest tests/unit/ -v                    # Tests unitaires
pytest tests/integration/ -v             # Tests d'intégration
pytest tests/performance/ -v             # Tests de performance

# Committer vos changements
git add .
git commit -m "✨ Ajout de ma super feature"

# Pousser et créer une Pull Request
git push origin feature/ma-super-feature
```

### 3. **Standards de Code**

- **Formatage** : Black (line-length=88)
- **Linting** : Ruff
- **Types** : MyPy avec annotations
- **Sécurité** : Bandit pour les scans
- **Tests** : pytest avec couverture >80% (113 tests actuels)
- **Documentation** : Docstrings Google style

### 4. **Structure des Commits**

Utilisez des préfixes clairs :

```
✨ feat: nouvelle fonctionnalité
🐛 fix: correction de bug
📚 docs: amélioration documentation
🎨 style: formatage, style
🔧 refactor: refactoring sans changement fonctionnel
🧪 test: ajout/modification de tests
⚡ perf: amélioration de performance
🔒 security: correction de sécurité
```

## 📋 Checklist Pull Request

- [ ] Code formaté avec Black
- [ ] Linting Ruff sans erreur
- [ ] Types vérifiés avec MyPy
- [ ] Tests ajoutés/mis à jour
- [ ] Couverture de tests maintenue
- [ ] Documentation mise à jour
- [ ] Changelog ajouté (si applicable)
- [ ] Tests passent sur CI

## 🎯 Issues "Help Wanted"

### 🟢 **Niveau Débutant**
- Améliorer les messages d'erreur CLI
- Ajouter des exemples dans `/examples/`
- Traduire la documentation
- Tester sur différents projets Python

### 🟡 **Niveau Intermédiaire**
- Optimiser les performances de collecte
- Ajouter support pour Poetry/Pipenv
- Créer templates de configuration
- Intégrer avec pre-commit hooks

### 🔴 **Niveau Avancé**
- Support multi-langages (JS, Go, Rust)
- API REST pour métriques en temps réel
- Plugin système pour extensibilité
- Intégration base de données

## 🎪 Guidelines de Review

### Ce qu'on recherche :
- ✅ Code propre et lisible
- ✅ Tests appropriés
- ✅ Documentation claire
- ✅ Performance acceptable
- ✅ Compatibilité multi-OS

### Ce qu'on évite :
- ❌ Fonctionnalités trop spécifiques
- ❌ Dépendances lourdes non justifiées
- ❌ Code non testé
- ❌ Breaking changes non documentés
- ❌ Collecte de données sensibles

## 🏆 Reconnaissance

Les contributeurs sont mentionnés dans :
- `CONTRIBUTORS.md`
- Release notes
- README (contributeurs majeurs)
- Page de remerciements du site

## 💬 Communication

- **Issues** : Questions, bugs, features
- **Discussions** : Idées, feedback, aide
- **Discord** : [Arkalia Community](https://discord.gg/arkalia) (optionnel)
- **Email** : `arkalia.luna.system@gmail.com`

## 📄 Licence

En contribuant, vous acceptez que votre code soit sous licence MIT.

---

**Merci de rendre Arkalia Metrics Collector encore meilleur ! 🚀**

## 🎯 Idées de Contributions Rapides

Vous voulez contribuer mais ne savez pas par où commencer ? Voici des idées simples :

1. **Testez sur votre projet** et signalez les problèmes
2. **Ajoutez un exemple** dans `/examples/`
3. **Améliorez la documentation** existante
4. **Créez un template** de configuration
5. **Partagez votre expérience** dans les discussions
