#!/usr/bin/env python3
"""
Exemple d'utilisation avancée avec configuration personnalisée
=============================================================

Ce script montre comment utiliser le collecteur avec des configurations avancées.
"""

import yaml
from pathlib import Path
from arkalia_metrics_collector import MetricsCollector, MetricsExporter


def create_custom_config():
    """Crée une configuration personnalisée."""
    config = {
        "project": {
            "name": "Mon Projet Awesome",
            "type": "web_application",
            "description": "Application web Django avec API REST"
        },
        "exclusions": [
            "**/migrations/**",
            "**/static/vendor/**", 
            "**/media/**",
            "**/locale/**",
            "**/venv/**",
            "**/.venv/**",
            "**/node_modules/**",
            "**/__pycache__/**",
            "**/.pytest_cache/**",
            "**/htmlcov/**",
            "**/coverage/**"
        ],
        "metrics": {
            "include_tests": True,
            "include_documentation": True,
            "deep_analysis": False
        }
    }
    
    config_path = Path("custom_metrics_config.yaml")
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    
    print(f"📋 Configuration créée : {config_path}")
    return config_path


def analyze_multiple_projects():
    """Analyse plusieurs projets et compare les métriques."""
    projects = [
        {"name": "frontend", "path": "./frontend"},
        {"name": "backend", "path": "./backend"}, 
        {"name": "shared", "path": "./shared"},
        {"name": "docs", "path": "./docs"}
    ]
    
    all_metrics = {}
    
    for project in projects:
        print(f"\n🔍 Analyse de {project['name']}...")
        
        # Vérifier si le projet existe
        project_path = Path(project["path"])
        if not project_path.exists():
            print(f"⚠️  Projet {project['name']} non trouvé à {project_path}")
            continue
        
        # Collecter les métriques
        collector = MetricsCollector(project["path"])
        metrics = collector.collect_all_metrics()
        all_metrics[project["name"]] = metrics
        
        # Afficher résumé
        summary = metrics.get("summary", {})
        print(f"   🐍 Python: {summary.get('total_python_files', 0)} fichiers")
        print(f"   📝 Code: {summary.get('lines_of_code', 0):,} lignes")
        print(f"   🧪 Tests: {summary.get('collected_tests', 0)} tests")
    
    return all_metrics


def generate_comparison_report(all_metrics):
    """Génère un rapport de comparaison entre projets."""
    print("\n📊 Génération du rapport de comparaison...")
    
    # Calculer les totaux
    total_files = sum(
        m.get("summary", {}).get("total_python_files", 0) 
        for m in all_metrics.values()
    )
    total_lines = sum(
        m.get("summary", {}).get("lines_of_code", 0)
        for m in all_metrics.values()
    )
    total_tests = sum(
        m.get("summary", {}).get("collected_tests", 0)
        for m in all_metrics.values()
    )
    
    # Créer le rapport
    report = f"""# 📊 Rapport de Comparaison Multi-Projets

## 🎯 Vue d'ensemble

- **Total fichiers Python**: {total_files:,}
- **Total lignes de code**: {total_lines:,}
- **Total tests**: {total_tests:,}

## 📈 Détails par projet

"""
    
    for project_name, metrics in all_metrics.items():
        summary = metrics.get("summary", {})
        files = summary.get("total_python_files", 0)
        lines = summary.get("lines_of_code", 0)
        tests = summary.get("collected_tests", 0)
        docs = summary.get("documentation_files", 0)
        
        # Calculer les pourcentages
        files_pct = (files / total_files * 100) if total_files > 0 else 0
        lines_pct = (lines / total_lines * 100) if total_lines > 0 else 0
        tests_pct = (tests / total_tests * 100) if total_tests > 0 else 0
        
        report += f"""### 🎯 {project_name.title()}

| Métrique | Valeur | % du total |
|----------|--------|------------|
| Fichiers Python | {files:,} | {files_pct:.1f}% |
| Lignes de code | {lines:,} | {lines_pct:.1f}% |
| Tests | {tests:,} | {tests_pct:.1f}% |
| Documentation | {docs:,} | - |

"""
    
    # Sauvegarder le rapport
    report_path = Path("comparison_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"📄 Rapport sauvegardé : {report_path}")
    return report_path


def main():
    """Exemple d'utilisation avancée."""
    print("🚀 Arkalia Metrics Collector - Utilisation Avancée")
    print("=" * 50)
    
    # 1. Créer une configuration personnalisée
    config_path = create_custom_config()
    
    # 2. Analyser le projet courant avec config personnalisée
    print("\n🔍 Analyse avec configuration personnalisée...")
    collector = MetricsCollector(".")
    metrics = collector.collect_all_metrics()
    
    # 3. Export avec noms personnalisés
    exporter = MetricsExporter(metrics)
    timestamp = metrics.get("timestamp", "").replace(":", "-").split(".")[0]
    
    output_dir = Path(f"advanced_metrics_{timestamp}")
    output_dir.mkdir(exist_ok=True)
    
    # Export personnalisé
    exports = {
        "Rapport principal": exporter.export_json(str(output_dir / "full_metrics.json")),
        "Résumé exécutif": exporter.export_markdown_summary(str(output_dir / "executive_summary.md")),
        "Dashboard interactif": exporter.export_html_dashboard(str(output_dir / "interactive_dashboard.html")),
        "Données pour Excel": exporter.export_csv(str(output_dir / "data_for_excel.csv"))
    }
    
    print(f"\n💾 Exports dans {output_dir}:")
    for name, success in exports.items():
        status = "✅" if success else "❌"
        print(f"   {status} {name}")
    
    # 4. Analyser plusieurs projets (optionnel)
    try:
        all_metrics = analyze_multiple_projects()
        if all_metrics:
            generate_comparison_report(all_metrics)
    except Exception as e:
        print(f"⚠️  Analyse multi-projets ignorée : {e}")
    
    # 5. Nettoyage
    if config_path.exists():
        config_path.unlink()
        print(f"\n🧹 Configuration temporaire supprimée")
    
    print(f"\n🎉 Analyse avancée terminée !")
    print(f"📊 Résultats dans : {output_dir.absolute()}")


if __name__ == "__main__":
    main()
