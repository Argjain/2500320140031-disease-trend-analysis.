try:
    import pytest
except ImportError:
    pytest = None
import sqlite3
import os
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "app.db"

def get_db_connection():
    assert DB_PATH.exists(), f"Database file missing at {DB_PATH}. Run src/generate_data.py first."
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def test_database_connection_and_table_existence(): # TC-T-01
    """TC-T-01: Verify all 5 base tables exist in SQLite database."""
    conn = get_db_connection()
    tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()]
    conn.close()
    expected = ["disease_master", "region_master", "demographic_group", "disease_cases", "demographic_breakdown"]
    for t in expected:
        assert t in tables, f"Expected table {t} not found in database."

def test_disease_cases_volume(): # TC-T-02
    """TC-T-02: Verify disease_cases contains expected ~3000 rows (including quality test dupes)."""
    conn = get_db_connection()
    count = conn.execute("SELECT COUNT(*) FROM disease_cases;").fetchone()[0]
    conn.close()
    assert count >= 3000, f"Expected at least 3000 records, got {count}."

def test_masters_row_counts(): # TC-T-03
    """TC-T-03: Verify exact row counts in reference dimension tables."""
    conn = get_db_connection()
    dm = conn.execute("SELECT COUNT(*) FROM disease_master;").fetchone()[0]
    rm = conn.execute("SELECT COUNT(*) FROM region_master;").fetchone()[0]
    dg = conn.execute("SELECT COUNT(*) FROM demographic_group;").fetchone()[0]
    conn.close()
    assert dm == 5, f"Expected 5 diseases, got {dm}."
    assert rm == 10, f"Expected 10 states, got {rm}."
    assert dg == 15, f"Expected 15 demographic segments, got {dg}."

def test_foreign_key_referential_integrity(): # TC-T-04
    """TC-T-04: Verify zero orphaned foreign key records exist in fact tables."""
    conn = get_db_connection()
    orphans_dis = conn.execute(
        "SELECT COUNT(*) FROM disease_cases dc LEFT JOIN disease_master dm ON dc.disease_id = dm.disease_id WHERE dm.disease_id IS NULL;"
    ).fetchone()[0]
    orphans_reg = conn.execute(
        "SELECT COUNT(*) FROM disease_cases dc LEFT JOIN region_master rm ON dc.region_id = rm.region_id WHERE rm.region_id IS NULL;"
    ).fetchone()[0]
    conn.close()
    assert orphans_dis == 0, f"Found {orphans_dis} orphaned disease foreign keys."
    assert orphans_reg == 0, f"Found {orphans_reg} orphaned region foreign keys."

def test_morbidity_mortality_logical_bounds(): # TC-T-05
    """TC-T-05: Verify clinical constraints (non-negative cases, deaths <= cases, recovered <= cases)."""
    conn = get_db_connection()
    neg_cases = conn.execute("SELECT COUNT(*) FROM disease_cases WHERE cases_reported < 0;").fetchone()[0]
    deaths_gt_cases = conn.execute("SELECT COUNT(*) FROM disease_cases WHERE deaths > cases_reported;").fetchone()[0]
    rec_gt_cases = conn.execute("SELECT COUNT(*) FROM disease_cases WHERE recovered > cases_reported;").fetchone()[0]
    conn.close()
    assert neg_cases == 0, f"Found {neg_cases} records with negative cases."
    assert deaths_gt_cases == 0, f"Found {deaths_gt_cases} records where deaths > cases."
    assert rec_gt_cases == 0, f"Found {rec_gt_cases} records where recovered > cases."

def test_unique_disease_names(): # TC-T-06
    """TC-T-06: Verify unique constraint on disease names."""
    conn = get_db_connection()
    tot = conn.execute("SELECT COUNT(*) FROM disease_master;").fetchone()[0]
    distinct = conn.execute("SELECT COUNT(DISTINCT disease_name) FROM disease_master;").fetchone()[0]
    conn.close()
    assert tot == distinct, "Duplicate disease names detected."

def test_analytical_view_columns_and_rows(): # TC-T-07
    """TC-T-07: Verify v_disease_analysis view returns joined projection matching fact rows."""
    conn = get_db_connection()
    view_count = conn.execute("SELECT COUNT(*) FROM v_disease_analysis;").fetchone()[0]
    cursor = conn.execute("SELECT * FROM v_disease_analysis LIMIT 1;")
    cols = [desc[0] for desc in cursor.description]
    conn.close()
    assert view_count >= 3000, f"Expected >= 3000 rows in view, got {view_count}."
    for req_col in ["cfr_pct", "recovery_rate_pct", "incidence_per_lakh", "disease_name", "region_name"]:
        assert req_col in cols, f"Required column {req_col} missing from analysis view."

def test_database_cold_query_latency(): # TC-T-15
    """TC-T-15: Verify analytical view full query latency executes under 1.5 seconds."""
    conn = get_db_connection()
    start_time = time.time()
    rows = conn.execute("SELECT * FROM v_disease_analysis;").fetchall()
    elapsed = time.time() - start_time
    conn.close()
    assert len(rows) >= 3000
    assert elapsed < 1.5, f"Query latency was {elapsed:.3f}s (Threshold: < 1.5s)."
