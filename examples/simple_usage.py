#!/usr/bin/env python3
"""
Exemple d'utilisation simple d'Arkalia Metrics Collector
========================================================

Ce script montre comment utiliser le collecteur de métriques de manière programmatique.
"""

from pathlib import Path
from arkalia_metrics_collector import MetricsCollector, MetricsExporter, MetricsValidator


def main():
    """Exemple d'utilisation basique du collecteur."""
    
    # 1. Initialiser le collecteur pour le projet courant
    print("🔍 Initialisation du collecteur...")
    collector = MetricsCollector(".")
    
    # 2. Collecter toutes les métriques
    print("📊 Collecte des métriques...")
    metrics = collector.collect_all_metrics()
    
    # 3. Afficher un résumé
    summary = metrics.get("summary", {})
    print(f"\n📈 Résumé des métriques :")
    print(f"   🐍 Fichiers Python: {summary.get('total_python_files', 0):,}")
    print(f"   📝 Lignes de code: {summary.get('lines_of_code', 0):,}")
    print(f"   🧪 Tests: {summary.get('collected_tests', 0):,}")
    print(f"   📚 Documentation: {summary.get('documentation_files', 0):,}")
    
    # 4. Valider les métriques (optionnel)
    print("\n✅ Validation des métriques...")
    validator = MetricsValidator()
    is_valid, errors, warnings = validator.validate_metrics(metrics)
    
    if is_valid:
        print("✅ Métriques valides !")
    else:
        print(f"❌ {len(errors)} erreurs trouvées")
        for error in errors:
            print(f"   • {error}")
    
    if warnings:
        print(f"⚠️  {len(warnings)} avertissements")
        for warning in warnings:
            print(f"   • {warning}")
    
    # 5. Exporter les résultats
    print("\n💾 Export des métriques...")
    exporter = MetricsExporter(metrics)
    
    # Export en différents formats
    outputs = Path("output_metrics")
    outputs.mkdir(exist_ok=True)
    
    results = {
        "JSON": exporter.export_json(str(outputs / "metrics.json")),
        "Markdown": exporter.export_markdown_summary(str(outputs / "metrics.md")),
        "HTML": exporter.export_html_dashboard(str(outputs / "dashboard.html")),
        "CSV": exporter.export_csv(str(outputs / "metrics.csv")),
    }
    
    # Afficher les résultats
    for format_name, success in results.items():
        status = "✅" if success else "❌"
        print(f"   {status} {format_name}: {'Succès' if success else 'Échec'}")
    
    print(f"\n🎉 Métriques exportées dans : {outputs.absolute()}")
    print(f"📊 Ouvrez {outputs / 'dashboard.html'} dans votre navigateur !")


if __name__ == "__main__":
    main()
