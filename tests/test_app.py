try:
    import pytest
except ImportError:
    pytest = None
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def test_application_entry_points_exist(): # TC-T-16
    """TC-T-16: Verify app.py and all 6 multi-page files exist on filesystem."""
    app_py = BASE_DIR / "app.py"
    assert app_py.exists(), "app.py root file missing."
    pages_dir = BASE_DIR / "pages"
    assert pages_dir.exists(), "pages/ directory missing."
    
    expected_pages = [
        "01_Overview.py",
        "02_Trends.py",
        "03_Regional_Analysis.py",
        "04_Demographics.py",
        "05_EDA_Statistics.py",
        "06_Data_Quality.py",
        "07_Project_Documents.py"
    ]
    for p in expected_pages:
        p_path = pages_dir / p
        assert p_path.exists(), f"Page route {p} missing in pages/ directory."

def test_source_modules_exist(): # TC-T-17
    """TC-T-17: Verify all modular Python source files exist under src/."""
    src_dir = BASE_DIR / "src"
    expected_src = ["__init__.py", "data_loader.py", "cleaning.py", "analysis.py", "ui.py", "generate_data.py"]
    for s in expected_src:
        assert (src_dir / s).exists(), f"Source module {s} missing."

def test_static_configuration_files(): # TC-T-18
    """TC-T-18: Verify configuration, manifest and documentation files are present."""
    assert (BASE_DIR / "requirements.txt").exists(), "requirements.txt missing."
    assert (BASE_DIR / ".streamlit" / "config.toml").exists(), ".streamlit/config.toml missing."
    assert (BASE_DIR / "data" / "disease_cases.csv").exists(), "disease_cases.csv missing."
