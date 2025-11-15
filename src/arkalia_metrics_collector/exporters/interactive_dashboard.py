#!/usr/bin/env python3
"""
Générateur de dashboard HTML interactif avec Chart.js.

Crée un dashboard avancé avec :
- Graphiques d'évolution (Chart.js)
- Tableaux interactifs (tri/filtre)
- Support historique des métriques
- Export CSV/JSON depuis le dashboard
"""

import json
from pathlib import Path
from typing import Any

from arkalia_metrics_collector import __version__


class InteractiveDashboardGenerator:
    """
    Générateur de dashboard HTML interactif.

    Crée un dashboard avec graphiques, tableaux interactifs et historique.
    """

    @staticmethod
    def generate_dashboard(
        metrics_data: dict[str, Any],
        history_data: list[dict[str, Any]] | None = None,
        output_file: str | Path = "dashboard.html",
        is_aggregated: bool = False,
    ) -> bool:
        """
        Génère un dashboard HTML interactif.

        Args:
            metrics_data: Métriques actuelles
            history_data: Historique des métriques (optionnel)
            output_file: Chemin du fichier de sortie

        Returns:
            True si la génération a réussi
        """
        try:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Adapter pour métriques agrégées ou simples
            if is_aggregated:
                aggregated = metrics_data.get("aggregated", {})
                summary = {
                    "total_python_files": aggregated.get("total_modules", 0),
                    "lines_of_code": aggregated.get("total_lines_of_code", 0),
                    "collected_tests": aggregated.get("total_tests", 0),
                    "documentation_files": aggregated.get(
                        "total_documentation_files", 0
                    ),
                }
                collection_info = {
                    "collection_date": metrics_data.get("collection_date", "Inconnu"),
                    "collector_version": __version__,
                }
                test_metrics = {
                    "coverage_percentage": aggregated.get("global_coverage"),
                }
            else:
                summary = metrics_data.get("summary", {})
                collection_info = metrics_data.get("collection_info", {})
                test_metrics = metrics_data.get("test_metrics", {})

            # Préparer les données pour les graphiques
            chart_data = InteractiveDashboardGenerator._prepare_chart_data(
                metrics_data, history_data
            )

            html_content = InteractiveDashboardGenerator._generate_html(
                summary,
                collection_info,
                test_metrics,
                metrics_data,
                chart_data,
                history_data,
                is_aggregated,
            )

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            return True

        except Exception as e:
            print(f"Erreur lors de la génération du dashboard: {e}")
            return False

    @staticmethod
    def _prepare_chart_data(
        metrics_data: dict[str, Any], history_data: list[dict[str, Any]] | None
    ) -> dict[str, Any]:
        """Prépare les données pour les graphiques Chart.js."""
        summary = metrics_data.get("summary", {})

        chart_data = {
            "current": {
                "modules": summary.get("total_python_files", 0),
                "lines": summary.get("lines_of_code", 0),
                "tests": summary.get("collected_tests", 0),
                "docs": summary.get("documentation_files", 0),
            },
            "history": {"labels": [], "modules": [], "lines": [], "tests": []},
        }

        if history_data:
            for entry in sorted(history_data, key=lambda x: x.get("saved_at", "")):
                agg = entry.get("aggregated", {})
                saved_at = entry.get("saved_at", "")
                if saved_at:
                    # Formater la date pour l'affichage
                    date_label = saved_at.split("T")[0] if "T" in saved_at else saved_at
                    chart_data["history"]["labels"].append(date_label)
                    chart_data["history"]["modules"].append(agg.get("total_modules", 0))
                    chart_data["history"]["lines"].append(
                        agg.get("total_lines_of_code", 0)
                    )
                    chart_data["history"]["tests"].append(agg.get("total_tests", 0))

        return chart_data

    @staticmethod
    def _generate_html(
        summary: dict[str, Any],
        collection_info: dict[str, Any],
        test_metrics: dict[str, Any],
        metrics_data: dict[str, Any],
        chart_data: dict[str, Any],
        history_data: list[dict[str, Any]] | None,
        is_aggregated: bool = False,
    ) -> str:
        """Génère le contenu HTML du dashboard."""
        coverage = test_metrics.get("coverage_percentage")
        coverage_display = f"{coverage:.1f}%" if coverage else "N/A"

        # Convertir les données en JSON pour JavaScript
        chart_data_json = json.dumps(chart_data, ensure_ascii=False)
        metrics_json = json.dumps(metrics_data, ensure_ascii=False, indent=2)

        has_history = bool(history_data and len(history_data) > 0)

        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arkalia Metrics Dashboard - Interactif</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        .metric-card {{
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .metric-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
        }}
        .table-container {{
            max-height: 600px;
            overflow-y: auto;
        }}
        .table-container::-webkit-scrollbar {{
            width: 8px;
        }}
        .table-container::-webkit-scrollbar-track {{
            background: #1f2937;
        }}
        .table-container::-webkit-scrollbar-thumb {{
            background: #4b5563;
            border-radius: 4px;
        }}
    </style>
</head>
<body class="bg-gray-900 text-white min-h-screen">
    <div class="container mx-auto px-4 py-8">
        <!-- Header -->
        <header class="text-center mb-12">
            <h1 class="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-600 mb-4">
                🚀 Arkalia Metrics Dashboard
            </h1>
            <p class="text-xl text-gray-300 mb-2">
                Métriques collectées le {collection_info.get("collection_date", "Inconnu")}
            </p>
            <div class="flex justify-center gap-4 mt-4">
                <button onclick="exportJSON()" class="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg transition">
                    📥 Export JSON
                </button>
                <button onclick="exportCSV()" class="bg-green-600 hover:bg-green-700 px-4 py-2 rounded-lg transition">
                    📥 Export CSV
                </button>
            </div>
        </header>

        <!-- Métriques principales -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
            <div class="metric-card bg-gradient-to-br from-blue-600 to-blue-800 p-6 rounded-xl shadow-lg">
                <div class="text-center">
                    <div class="text-4xl font-bold mb-2">{summary.get("total_python_files", 0):,}</div>
                    <div class="text-blue-200">Fichiers Python</div>
                </div>
            </div>
            <div class="metric-card bg-gradient-to-br from-green-600 to-green-800 p-6 rounded-xl shadow-lg">
                <div class="text-center">
                    <div class="text-4xl font-bold mb-2">{summary.get("lines_of_code", 0):,}</div>
                    <div class="text-green-200">Lignes de Code</div>
                </div>
            </div>
            <div class="metric-card bg-gradient-to-br from-purple-600 to-purple-800 p-6 rounded-xl shadow-lg">
                <div class="text-center">
                    <div class="text-4xl font-bold mb-2">{summary.get("collected_tests", 0):,}</div>
                    <div class="text-purple-200">Tests</div>
                </div>
            </div>
            <div class="metric-card bg-gradient-to-br from-orange-600 to-orange-800 p-6 rounded-xl shadow-lg">
                <div class="text-center">
                    <div class="text-4xl font-bold mb-2">{summary.get("documentation_files", 0):,}</div>
                    <div class="text-orange-200">Documentation</div>
                </div>
            </div>
        </div>

        <!-- Coverage si disponible -->
        {f'''
        <div class="bg-gray-800 rounded-xl p-6 mb-8">
            <h2 class="text-2xl font-bold mb-4">📊 Coverage</h2>
            <div class="text-center">
                <div class="text-5xl font-bold mb-2">{coverage_display}</div>
                <div class="w-full bg-gray-700 rounded-full h-4 mt-4">
                    <div class="bg-gradient-to-r from-green-500 to-green-600 h-4 rounded-full" style="width: {coverage if coverage else 0}%"></div>
                </div>
            </div>
        </div>
        ''' if coverage else ''}

        <!-- Graphiques d'évolution -->
        {'''
        <div class="bg-gray-800 rounded-xl p-6 mb-8">
            <h2 class="text-2xl font-bold mb-4">📈 Évolution des Métriques</h2>
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div>
                    <h3 class="text-lg font-semibold mb-2">Modules Python</h3>
                    <canvas id="modulesChart"></canvas>
                </div>
                <div>
                    <h3 class="text-lg font-semibold mb-2">Lignes de Code</h3>
                    <canvas id="linesChart"></canvas>
                </div>
                <div>
                    <h3 class="text-lg font-semibold mb-2">Tests</h3>
                    <canvas id="testsChart"></canvas>
                </div>
                <div>
                    <h3 class="text-lg font-semibold mb-2">Vue d'ensemble</h3>
                    <canvas id="overviewChart"></canvas>
                </div>
            </div>
        </div>
        ''' if has_history else ''}

        <!-- Détails des métriques -->
        <div class="bg-gray-800 rounded-xl p-6 mb-8">
            <h2 class="text-2xl font-bold mb-4">📋 Détails des Métriques</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                    <h3 class="text-lg font-semibold mb-2">🐍 Métriques Python</h3>
                    <ul class="space-y-2 text-gray-300">
                        <li>• Fichiers core: {metrics_data.get("python_files", {}).get("core_files", 0):,}</li>
                        <li>• Fichiers de test: {metrics_data.get("python_files", {}).get("test_files", 0):,}</li>
                        <li>• Total lignes: {metrics_data.get("python_files", {}).get("total_lines", 0):,}</li>
                    </ul>
                </div>
                <div>
                    <h3 class="text-lg font-semibold mb-2">🧪 Métriques de Tests</h3>
                    <ul class="space-y-2 text-gray-300">
                        <li>• Fichiers de test: {test_metrics.get("test_files_count", 0):,}</li>
                        <li>• Dossiers de test: {test_metrics.get("test_directories_count", 0):,}</li>
                        <li>• Tests collectés: {test_metrics.get("collected_tests_count", 0):,}</li>
                        {f'<li>• Coverage: {coverage_display}</li>' if coverage else ''}
                    </ul>
                </div>
            </div>
        </div>

        <!-- Tableau des projets (si métriques agrégées) -->
        {InteractiveDashboardGenerator._generate_projects_table(metrics_data) if is_aggregated else ''}

        <!-- Tableau des fichiers Python (si disponible) -->
        {InteractiveDashboardGenerator._generate_files_table(metrics_data) if not is_aggregated else ''}

        <!-- Footer -->
        <footer class="text-center mt-12 text-gray-400">
            <p>Généré par <strong>Arkalia Metrics Collector</strong> v{collection_info.get("collector_version", __version__)}</p>
        </footer>
    </div>

    <!-- Scripts JavaScript -->
    <script>
        const chartData = {chart_data_json};
        const metricsData = {metrics_json};

        {InteractiveDashboardGenerator._generate_charts_script(chart_data, has_history)}

        function exportJSON() {{
            const dataStr = JSON.stringify(metricsData, null, 2);
            const dataBlob = new Blob([dataStr], {{type: 'application/json'}});
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'metrics.json';
            link.click();
        }}

        function exportCSV() {{
            const summary = metricsData.summary || {{}};
            const csv = [
                ['Métrique', 'Valeur', 'Unité'],
                ['Fichiers Python', summary.total_python_files || 0, 'fichiers'],
                ['Lignes de Code', summary.lines_of_code || 0, 'lignes'],
                ['Tests', summary.collected_tests || 0, 'tests'],
                ['Documentation', summary.documentation_files || 0, 'fichiers'],
            ].map(row => row.join(',')).join('\\n');

            const dataBlob = new Blob([csv], {{type: 'text/csv'}});
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'metrics.csv';
            link.click();
        }}
    </script>
</body>
</html>"""

        return html

    @staticmethod
    def _generate_charts_script(chart_data: dict[str, Any], has_history: bool) -> str:
        """Génère le script JavaScript pour les graphiques Chart.js."""
        if not has_history:
            return "// Pas d'historique disponible pour les graphiques"

        history = chart_data["history"]
        labels = history["labels"]
        modules = history["modules"]
        lines = history["lines"]
        tests = history["tests"]

        return f"""
        const chartOptions = {{
            responsive: true,
            maintainAspectRatio: true,
            plugins: {{
                legend: {{
                    labels: {{ color: '#e5e7eb' }}
                }}
            }},
            scales: {{
                x: {{
                    ticks: {{ color: '#9ca3af' }},
                    grid: {{ color: '#374151' }}
                }},
                y: {{
                    ticks: {{ color: '#9ca3af' }},
                    grid: {{ color: '#374151' }}
                }}
            }}
        }};

        // Graphique Modules
        new Chart(document.getElementById('modulesChart'), {{
            type: 'line',
            data: {{
                labels: {json.dumps(labels)},
                datasets: [{{
                    label: 'Modules Python',
                    data: {json.dumps(modules)},
                    borderColor: 'rgb(59, 130, 246)',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    tension: 0.4
                }}]
            }},
            options: chartOptions
        }});

        // Graphique Lignes de Code
        new Chart(document.getElementById('linesChart'), {{
            type: 'line',
            data: {{
                labels: {json.dumps(labels)},
                datasets: [{{
                    label: 'Lignes de Code',
                    data: {json.dumps(lines)},
                    borderColor: 'rgb(34, 197, 94)',
                    backgroundColor: 'rgba(34, 197, 94, 0.1)',
                    tension: 0.4
                }}]
            }},
            options: chartOptions
        }});

        // Graphique Tests
        new Chart(document.getElementById('testsChart'), {{
            type: 'line',
            data: {{
                labels: {json.dumps(labels)},
                datasets: [{{
                    label: 'Tests',
                    data: {json.dumps(tests)},
                    borderColor: 'rgb(168, 85, 247)',
                    backgroundColor: 'rgba(168, 85, 247, 0.1)',
                    tension: 0.4
                }}]
            }},
            options: chartOptions
        }});

        // Graphique Vue d'ensemble
        new Chart(document.getElementById('overviewChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(labels)},
                datasets: [
                    {{
                        label: 'Modules',
                        data: {json.dumps(modules)},
                        backgroundColor: 'rgba(59, 130, 246, 0.6)'
                    }},
                    {{
                        label: 'Tests',
                        data: {json.dumps(tests)},
                        backgroundColor: 'rgba(168, 85, 247, 0.6)'
                    }}
                ]
            }},
            options: chartOptions
        }});
        """

    @staticmethod
    def _generate_projects_table(metrics_data: dict[str, Any]) -> str:
        """Génère un tableau interactif des projets avec tri/filtre."""
        projects = metrics_data.get("projects", [])
        if not projects:
            return ""

        rows = ""
        for project in sorted(projects, key=lambda x: x.get("name", "")):
            name = project.get("name", "")
            modules = project.get("modules", 0)
            lines = project.get("lines_of_code", 0)
            tests = project.get("tests", 0)
            coverage = project.get("coverage", "N/A")
            if isinstance(coverage, int | float):
                coverage = f"{coverage:.1f}%"

            rows += f"""
            <tr class="hover:bg-gray-700 project-row" data-name="{name.lower()}">
                <td class="px-4 py-2 font-semibold">{name}</td>
                <td class="px-4 py-2 text-right">{modules:,}</td>
                <td class="px-4 py-2 text-right">{lines:,}</td>
                <td class="px-4 py-2 text-right">{tests:,}</td>
                <td class="px-4 py-2 text-right">{coverage}</td>
            </tr>
            """

        return f"""
        <div class="bg-gray-800 rounded-xl p-6 mb-8">
            <h2 class="text-2xl font-bold mb-4">📦 Projets ({len(projects)} projets)</h2>
            <div class="mb-4">
                <input
                    type="text"
                    id="projectFilter"
                    placeholder="🔍 Filtrer par nom de projet..."
                    class="w-full px-4 py-2 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    onkeyup="filterProjects()"
                />
            </div>
            <div class="table-container">
                <table class="w-full text-left" id="projectsTable">
                    <thead class="bg-gray-700 sticky top-0">
                        <tr>
                            <th class="px-4 py-2 cursor-pointer" onclick="sortTable(0)">
                                Projet ↕️
                            </th>
                            <th class="px-4 py-2 cursor-pointer text-right" onclick="sortTable(1)">
                                Modules ↕️
                            </th>
                            <th class="px-4 py-2 cursor-pointer text-right" onclick="sortTable(2)">
                                Lignes ↕️
                            </th>
                            <th class="px-4 py-2 cursor-pointer text-right" onclick="sortTable(3)">
                                Tests ↕️
                            </th>
                            <th class="px-4 py-2 cursor-pointer text-right" onclick="sortTable(4)">
                                Coverage ↕️
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            </div>
        </div>
        <script>
            let sortDirection = {{}};
            function sortTable(columnIndex) {{
                const table = document.getElementById('projectsTable');
                const tbody = table.querySelector('tbody');
                const rows = Array.from(tbody.querySelectorAll('tr'));

                const direction = sortDirection[columnIndex] || 'asc';
                sortDirection[columnIndex] = direction === 'asc' ? 'desc' : 'asc';

                rows.sort((a, b) => {{
                    const aText = a.cells[columnIndex].textContent.trim();
                    const bText = b.cells[columnIndex].textContent.trim();

                    // Essayer de parser comme nombre
                    const aNum = parseFloat(aText.replace(/[,%]/g, ''));
                    const bNum = parseFloat(bText.replace(/[,%]/g, ''));

                    if (!isNaN(aNum) && !isNaN(bNum)) {{
                        return direction === 'asc' ? aNum - bNum : bNum - aNum;
                    }}

                    // Sinon, tri alphabétique
                    return direction === 'asc'
                        ? aText.localeCompare(bText)
                        : bText.localeCompare(aText);
                }});

                rows.forEach(row => tbody.appendChild(row));
            }}

            function filterProjects() {{
                const input = document.getElementById('projectFilter');
                const filter = input.value.toLowerCase();
                const rows = document.querySelectorAll('.project-row');

                rows.forEach(row => {{
                    const name = row.getAttribute('data-name');
                    if (name.includes(filter)) {{
                        row.style.display = '';
                    }} else {{
                        row.style.display = 'none';
                    }}
                }});
            }}
        </script>
        """

    @staticmethod
    def _generate_files_table(metrics_data: dict[str, Any]) -> str:
        """Génère un tableau interactif des fichiers Python."""
        python_files = metrics_data.get("python_files", {}).get("files_list", [])
        if not python_files or len(python_files) > 100:
            return ""  # Trop de fichiers pour afficher

        rows = ""
        for i, file_path in enumerate(python_files[:50], 1):  # Limiter à 50 fichiers
            rows += f'<tr class="hover:bg-gray-700"><td class="px-4 py-2">{i}</td><td class="px-4 py-2 text-gray-300">{file_path}</td></tr>'

        return f"""
        <div class="bg-gray-800 rounded-xl p-6 mb-8">
            <h2 class="text-2xl font-bold mb-4">📁 Fichiers Python ({len(python_files)} fichiers)</h2>
            <div class="table-container">
                <table class="w-full text-left">
                    <thead class="bg-gray-700 sticky top-0">
                        <tr>
                            <th class="px-4 py-2">#</th>
                            <th class="px-4 py-2">Chemin</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            </div>
            {f'<p class="text-gray-400 text-sm mt-4">Affichage de 50 fichiers sur {len(python_files)}</p>' if len(python_files) > 50 else ''}
        </div>
        """
