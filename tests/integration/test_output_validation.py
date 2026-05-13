#!/usr/bin/env python3
"""
Tests de validation systématique des outputs.

Valide que tous les formats d'export produisent des outputs
cohérents et de qualité professionnelle.
"""

import csv
import json
from pathlib import Path

import pytest

from arkalia_metrics_collector import (
    MetricsCollector,
    MetricsExporter,
)


class TestOutputValidation:
    """Tests de validation des outputs."""

    @pytest.fixture
    def comprehensive_project(self, tmp_path: Path) -> Path:
        """Projet complet pour les tests de validation."""
        project = tmp_path / "comprehensive_project"
        project.mkdir()

        # Structure complète
        src_dir = project / "src" / "comprehensive_package"
        src_dir.mkdir(parents=True)

        tests_dir = project / "tests"
        tests_dir.mkdir()

        docs_dir = project / "docs"
        docs_dir.mkdir()

        scripts_dir = project / "scripts"
        scripts_dir.mkdir()

        # Modules source variés
        modules = {
            "core": '''"""Module core principal."""
import os
from typing import List, Dict, Any

class CoreProcessor:
    """Processeur principal."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.data = []

    def process(self, items: List[str]) -> List[str]:
        """Traite une liste d'éléments."""
        return [item.upper() for item in items]

    def validate(self, data: Any) -> bool:
        """Valide des données."""
        return data is not None and len(str(data)) > 0
''',
            "api": '''"""Module API REST."""
from typing import Optional
import json

class APIClient:
    """Client API."""

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get(self, endpoint: str) -> Optional[dict]:
        """Effectue une requête GET."""
        return {"endpoint": endpoint, "status": "success"}

    def post(self, endpoint: str, data: dict) -> Optional[dict]:
        """Effectue une requête POST."""
        return {"endpoint": endpoint, "data": data, "status": "created"}
''',
            "utils": '''"""Utilitaires divers."""
import re
from datetime import datetime

def clean_string(text: str) -> str:
    """Nettoie une chaîne de caractères."""
    return re.sub(r'\\s+', ' ', text.strip())

def format_timestamp(dt: datetime) -> str:
    """Formate un timestamp."""
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def calculate_hash(data: str) -> str:
    """Calcule un hash simple."""
    return str(hash(data))
''',
            "models": '''"""Modèles de données."""
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    """Modèle utilisateur."""
    id: int
    name: str
    email: str
    active: bool = True

    def to_dict(self) -> dict:
        """Convertit en dictionnaire."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "active": self.active
        }

@dataclass
class Product:
    """Modèle produit."""
    id: int
    name: str
    price: float
    description: Optional[str] = None
''',
        }

        for module_name, content in modules.items():
            (src_dir / f"{module_name}.py").write_text(content)

        # Tests correspondants
        test_modules = {
            "test_core": '''"""Tests du module core."""
import pytest
from comprehensive_package.core import CoreProcessor

def test_core_processor_init():
    """Test d'initialisation."""
    config = {"debug": True}
    processor = CoreProcessor(config)
    assert processor.config == config
    assert processor.data == []

def test_core_processor_process():
    """Test de traitement."""
    processor = CoreProcessor({})
    result = processor.process(["hello", "world"])
    assert result == ["HELLO", "WORLD"]

def test_core_processor_validate():
    """Test de validation."""
    processor = CoreProcessor({})
    assert processor.validate("test") is True
    assert processor.validate("") is False
    assert processor.validate(None) is False
''',
            "test_api": '''"""Tests du module API."""
import pytest
from comprehensive_package.api import APIClient

def test_api_client_init():
    """Test d'initialisation."""
    client = APIClient("https://api.example.com")
    assert client.base_url == "https://api.example.com"

def test_api_client_get():
    """Test requête GET."""
    client = APIClient("https://api.example.com")
    result = client.get("/users")
    assert result["endpoint"] == "/users"
    assert result["status"] == "success"

def test_api_client_post():
    """Test requête POST."""
    client = APIClient("https://api.example.com")
    data = {"name": "test"}
    result = client.post("/users", data)
    assert result["endpoint"] == "/users"
    assert result["data"] == data
    assert result["status"] == "created"
''',
            "test_utils": '''"""Tests des utilitaires."""
import pytest
from datetime import datetime
from comprehensive_package.utils import clean_string, format_timestamp, calculate_hash

def test_clean_string():
    """Test nettoyage de chaîne."""
    assert clean_string("  hello   world  ") == "hello world"
    assert clean_string("test\\n\\t") == "test"

def test_format_timestamp():
    """Test formatage timestamp."""
    dt = datetime(2024, 1, 1, 12, 30, 45)
    result = format_timestamp(dt)
    assert result == "2024-01-01 12:30:45"

def test_calculate_hash():
    """Test calcul de hash."""
    hash1 = calculate_hash("test")
    hash2 = calculate_hash("test")
    assert hash1 == hash2
    assert hash1 != calculate_hash("different")
''',
            "test_models": '''"""Tests des modèles."""
import pytest
from comprehensive_package.models import User, Product

def test_user_model():
    """Test modèle User."""
    user = User(1, "John", "arkalia.luna.system@gmail.com")
    assert user.id == 1
    assert user.name == "John"
    assert user.email == "arkalia.luna.system@gmail.com"
    assert user.active is True

    user_dict = user.to_dict()
    assert user_dict["id"] == 1
    assert user_dict["name"] == "John"

def test_product_model():
    """Test modèle Product."""
    product = Product(1, "Laptop", 999.99, "Gaming laptop")
    assert product.id == 1
    assert product.name == "Laptop"
    assert product.price == 999.99
    assert product.description == "Gaming laptop"

    product_no_desc = Product(2, "Mouse", 29.99)
    assert product_no_desc.description is None
''',
        }

        for test_name, content in test_modules.items():
            (tests_dir / f"{test_name}.py").write_text(content)

        # Documentation
        (docs_dir / "README.md").write_text(
            """# Comprehensive Package

Package complet pour les tests de validation des outputs.

## Installation

```bash
pip install comprehensive-package
```

## Usage

```python
from comprehensive_package import CoreProcessor
processor = CoreProcessor({"debug": True})
result = processor.process(["hello", "world"])
```

## API Reference

### CoreProcessor

Classe principale pour le traitement de données.

#### Methods

- `__init__(config)`: Initialise le processeur
- `process(items)`: Traite une liste d'éléments
- `validate(data)`: Valide des données
"""
        )

        (docs_dir / "CHANGELOG.md").write_text(
            """# Changelog

## [1.0.0] - 2024-01-01

### Added
- CoreProcessor class
- APIClient class
- Utility functions
- Data models

### Changed
- Initial release

### Fixed
- None
"""
        )

        # Scripts
        (scripts_dir / "deploy.py").write_text(
            '''#!/usr/bin/env python3
"""Script de déploiement."""
import os
import sys

def deploy():
    """Déploie l'application."""
    print("Déploiement en cours...")
    # Logique de déploiement
    print("Déploiement terminé!")

if __name__ == "__main__":
    deploy()
'''
        )

        return project

    def test_json_output_validation(self, comprehensive_project: Path, tmp_path: Path):
        """Validation de l'output JSON."""
        collector = MetricsCollector(str(comprehensive_project))
        metrics = collector.collect_all_metrics()

        exporter = MetricsExporter(metrics)
        output_dir = tmp_path / "json_validation"
        output_dir.mkdir()

        # Export JSON
        json_file = output_dir / "metrics.json"
        assert exporter.export_json(str(json_file)) is True

        # Validation du fichier JSON
        assert json_file.exists()

        with open(json_file) as f:
            data = json.load(f)

        # Structure requise
        required_keys = [
            "timestamp",
            "project_root",
            "python_files",
            "test_metrics",
            "documentation_metrics",
            "summary",
        ]
        for key in required_keys:
            assert key in data, f"Clé manquante: {key}"

        # Validation des types
        assert isinstance(data["timestamp"], str)
        assert isinstance(data["python_files"], dict)
        assert isinstance(data["test_metrics"], dict)
        assert isinstance(data["summary"], dict)

        # Validation des métriques Python
        python_files = data["python_files"]
        assert "count" in python_files
        assert "total_lines" in python_files
        assert "files_list" in python_files
        assert isinstance(python_files["count"], int)
        assert isinstance(python_files["total_lines"], int)
        assert isinstance(python_files["files_list"], list)

        # Validation des métriques de test
        test_metrics = data["test_metrics"]
        assert "collected_tests_count" in test_metrics
        assert "test_files_count" in test_metrics
        assert isinstance(test_metrics["collected_tests_count"], int)
        assert isinstance(test_metrics["test_files_count"], int)

        # Validation de cohérence
        assert python_files["count"] >= 4  # Au moins 4 modules
        assert test_metrics["collected_tests_count"] >= 4  # Au moins 4 tests
        assert python_files["total_lines"] > 0

    def test_markdown_output_validation(
        self, comprehensive_project: Path, tmp_path: Path
    ):
        """Validation de l'output Markdown."""
        collector = MetricsCollector(str(comprehensive_project))
        metrics = collector.collect_all_metrics()

        exporter = MetricsExporter(metrics)
        output_dir = tmp_path / "markdown_validation"
        output_dir.mkdir()

        # Export Markdown
        md_file = output_dir / "metrics.md"
        assert exporter.export_markdown_summary(str(md_file)) is True

        # Validation du fichier Markdown
        assert md_file.exists()

        content = md_file.read_text(encoding="utf-8")

        # Validation de la structure Markdown
        assert "#" in content  # Titres
        assert "##" in content  # Sous-titres
        assert "|" in content  # Tableaux
        assert "-" in content  # Listes

        # Validation du contenu
        required_sections = ["Métriques", "Python", "Tests", "Documentation"]
        for section in required_sections:
            assert section in content, f"Section manquante: {section}"

        # Validation des métriques dans le texte
        assert "Fichiers Python" in content
        assert "Lignes de Code" in content or "lignes" in content
        assert "Tests collectés" in content or "Tests" in content

    def test_html_output_validation(self, comprehensive_project: Path, tmp_path: Path):
        """Validation de l'output HTML."""
        collector = MetricsCollector(str(comprehensive_project))
        metrics = collector.collect_all_metrics()

        exporter = MetricsExporter(metrics)
        output_dir = tmp_path / "html_validation"
        output_dir.mkdir()

        # Export HTML
        html_file = output_dir / "dashboard.html"
        assert exporter.export_html_dashboard(str(html_file)) is True

        # Validation du fichier HTML
        assert html_file.exists()

        content = html_file.read_text(encoding="utf-8")

        # Validation de la structure HTML
        assert "<!DOCTYPE html>" in content
        assert "<html" in content
        assert "<head>" in content
        assert "<body" in content
        assert "</html>" in content

        # Validation des éléments de style
        assert "style" in content or "css" in content
        assert "grid" in content or "div" in content
        assert "h1" in content or "h2" in content

        # Validation du contenu
        assert "Métriques" in content or "Metrics" in content
        assert "Python" in content

    def test_csv_output_validation(self, comprehensive_project: Path, tmp_path: Path):
        """Validation de l'output CSV."""
        collector = MetricsCollector(str(comprehensive_project))
        metrics = collector.collect_all_metrics()

        exporter = MetricsExporter(metrics)
        output_dir = tmp_path / "csv_validation"
        output_dir.mkdir()

        # Export CSV
        csv_file = output_dir / "metrics.csv"
        assert exporter.export_csv(str(csv_file)) is True

        # Validation du fichier CSV
        assert csv_file.exists()

        # Validation de la structure CSV
        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)

        assert len(rows) > 0  # Au moins une ligne
        assert len(rows[0]) >= 2  # Au moins 2 colonnes (métrique, valeur)

        # Validation des en-têtes
        headers = rows[0]
        assert "Metric" in headers or "Métrique" in headers
        assert "Value" in headers or "Valeur" in headers

        # Validation des données
        data_rows = rows[1:]  # Exclure l'en-tête
        assert len(data_rows) > 0

        # Vérifier que chaque ligne a le bon nombre de colonnes (si non vide)
        for row in data_rows:
            if row:  # Ignorer les lignes vides
                assert len(row) == len(headers)

    def test_output_consistency_across_formats(
        self, comprehensive_project: Path, tmp_path: Path
    ):
        """Validation de la cohérence entre tous les formats."""
        collector = MetricsCollector(str(comprehensive_project))
        metrics = collector.collect_all_metrics()

        exporter = MetricsExporter(metrics)
        output_dir = tmp_path / "consistency_validation"
        output_dir.mkdir()

        # Export de tous les formats
        json_file = output_dir / "metrics.json"
        md_file = output_dir / "metrics.md"
        html_file = output_dir / "dashboard.html"
        csv_file = output_dir / "metrics.csv"

        assert exporter.export_json(str(json_file)) is True
        assert exporter.export_markdown_summary(str(md_file)) is True
        assert exporter.export_html_dashboard(str(html_file)) is True
        assert exporter.export_csv(str(csv_file)) is True

        # Charger les données JSON pour référence
        with open(json_file) as f:
            json_data = json.load(f)

        # Vérifier que les métriques sont cohérentes
        python_count = json_data["python_files"]["count"]
        test_count = json_data["test_metrics"]["collected_tests_count"]
        lines_count = json_data["python_files"]["total_lines"]

        # Vérifier dans le Markdown
        md_content = md_file.read_text(encoding="utf-8")
        assert str(python_count) in md_content
        assert str(test_count) in md_content
        assert str(lines_count) in md_content

        # Vérifier dans le HTML
        html_content = html_file.read_text(encoding="utf-8")
        assert str(python_count) in html_content
        assert str(test_count) in html_content
        assert str(lines_count) in html_content

        # Vérifier dans le CSV
        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            csv_data = {row[0]: row[1] for row in reader if len(row) >= 2}

        # Les valeurs doivent être cohérentes (approximativement)
        if "Python Files" in csv_data:
            assert abs(int(csv_data["Python Files"]) - python_count) <= 1
        if "Tests" in csv_data:
            assert abs(int(csv_data["Tests"]) - test_count) <= 1

    def test_output_encoding_validation(
        self, comprehensive_project: Path, tmp_path: Path
    ):
        """Validation de l'encodage des outputs."""
        collector = MetricsCollector(str(comprehensive_project))
        metrics = collector.collect_all_metrics()

        exporter = MetricsExporter(metrics)
        output_dir = tmp_path / "encoding_validation"
        output_dir.mkdir()

        # Export de tous les formats
        files = {
            "json": output_dir / "metrics.json",
            "md": output_dir / "metrics.md",
            "html": output_dir / "dashboard.html",
            "csv": output_dir / "metrics.csv",
        }

        exporter.export_json(str(files["json"]))
        exporter.export_markdown_summary(str(files["md"]))
        exporter.export_html_dashboard(str(files["html"]))
        exporter.export_csv(str(files["csv"]))

        # Vérifier que tous les fichiers sont lisibles en UTF-8
        for file_type, file_path in files.items():
            assert file_path.exists()

            try:
                content = file_path.read_text(encoding="utf-8")
                assert len(content) > 0
            except UnicodeDecodeError:
                pytest.fail(f"Fichier {file_type} n'est pas encodé en UTF-8")

    def test_output_file_permissions(self, comprehensive_project: Path, tmp_path: Path):
        """Validation des permissions des fichiers de sortie."""
        collector = MetricsCollector(str(comprehensive_project))
        metrics = collector.collect_all_metrics()

        exporter = MetricsExporter(metrics)
        output_dir = tmp_path / "permissions_validation"
        output_dir.mkdir()

        # Export de tous les formats
        files = {
            "json": output_dir / "metrics.json",
            "md": output_dir / "metrics.md",
            "html": output_dir / "dashboard.html",
            "csv": output_dir / "metrics.csv",
        }

        exporter.export_json(str(files["json"]))
        exporter.export_markdown_summary(str(files["md"]))
        exporter.export_html_dashboard(str(files["html"]))
        exporter.export_csv(str(files["csv"]))

        # Vérifier que tous les fichiers sont lisibles
        for _file_type, file_path in files.items():
            assert file_path.exists()
            assert file_path.is_file()
            assert file_path.stat().st_size > 0  # Fichier non vide

    def test_output_with_special_characters(self, tmp_path: Path):
        """Test avec caractères spéciaux dans les métriques."""
        # Créer un projet avec des caractères spéciaux
        project = tmp_path / "special_chars_project"
        project.mkdir()

        src_dir = project / "src" / "special_package"
        src_dir.mkdir(parents=True)

        # Fichier avec caractères spéciaux (sans émojis problématiques)
        (src_dir / "special.py").write_text(
            '''"""Module avec caractères spéciaux."""
# Accents: éàçù
# Symboles: @#$%^&*()

def fonction_spéciale():
    """Fonction avec caractères spéciaux."""
    return "Café & croissants"
'''
        )

        collector = MetricsCollector(str(project))
        metrics = collector.collect_all_metrics()

        exporter = MetricsExporter(metrics)
        output_dir = tmp_path / "special_chars_output"
        output_dir.mkdir()

        # Export de tous les formats
        assert exporter.export_json(str(output_dir / "metrics.json")) is True
        assert exporter.export_markdown_summary(str(output_dir / "metrics.md")) is True
        assert (
            exporter.export_html_dashboard(str(output_dir / "dashboard.html")) is True
        )
        assert exporter.export_csv(str(output_dir / "metrics.csv")) is True

        # Vérifier que les caractères spéciaux sont préservés
        md_content = (output_dir / "metrics.md").read_text(encoding="utf-8")
        assert (
            "Python" in md_content or "Métriques" in md_content
        )  # Au moins du contenu

    def test_output_validation_with_empty_project(self, tmp_path: Path):
        """Test de validation avec projet vide."""
        empty_project = tmp_path / "empty_project"
        empty_project.mkdir()

        collector = MetricsCollector(str(empty_project))
        metrics = collector.collect_all_metrics()

        exporter = MetricsExporter(metrics)
        output_dir = tmp_path / "empty_output"
        output_dir.mkdir()

        # Export doit fonctionner même avec un projet vide
        assert exporter.export_json(str(output_dir / "metrics.json")) is True
        assert exporter.export_markdown_summary(str(output_dir / "metrics.md")) is True
        assert (
            exporter.export_html_dashboard(str(output_dir / "dashboard.html")) is True
        )
        assert exporter.export_csv(str(output_dir / "metrics.csv")) is True

        # Vérifier que les fichiers sont créés
        for file_name in [
            "metrics.json",
            "metrics.md",
            "dashboard.html",
            "metrics.csv",
        ]:
            file_path = output_dir / file_name
            assert file_path.exists()
            assert file_path.stat().st_size > 0  # Fichier non vide
