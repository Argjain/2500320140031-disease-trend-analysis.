import os
import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "app.db"

# Graceful st decorator fallback for test environments without Streamlit server
try:
    import streamlit as st
    cache_decorator = st.cache_data(ttl=3600, show_spinner="Loading epidemiological data...")
except Exception:
    def cache_decorator(func):
        return func

@cache_decorator
def load_data() -> pd.DataFrame:
    """
    Connects to the SQLite repository at data/app.db and queries the denormalized
    materialized view v_disease_analysis. Returns a high-performance pandas DataFrame.
    """
    if not DB_PATH.exists():
        # Fallback to CSV if DB not compiled yet
        csv_path = BASE_DIR / "data" / "disease_cases.csv"
        if csv_path.exists():
            return pd.read_csv(csv_path)
        raise FileNotFoundError(f"Database file not found at {DB_PATH}. Run src/generate_data.py first.")

    conn = sqlite3.connect(str(DB_PATH))
    query = """
    SELECT
        case_id,
        report_date,
        report_year,
        report_month,
        disease_id,
        disease_name,
        disease_category,
        is_contagious,
        region_id,
        region_name,
        state_code,
        zone,
        population,
        area_sqkm,
        population_density,
        cases_reported,
        deaths,
        recovered,
        active_cases,
        hospitalized,
        is_outbreak,
        cfr_pct,
        recovery_rate_pct,
        incidence_per_lakh,
        data_source,
        created_at
    FROM v_disease_analysis;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Convert date string to datetime
    df["report_date"] = pd.to_datetime(df["report_date"])
    return df

@cache_decorator
def load_demographic_breakdown() -> pd.DataFrame:
    """Loads granular demographic sub-fact records linked to demographic master."""
    if not DB_PATH.exists():
        return pd.DataFrame()

    conn = sqlite3.connect(str(DB_PATH))
    query = """
    SELECT
        db.breakdown_id,
        db.case_id,
        db.demo_id,
        dg.age_group,
        dg.gender,
        db.cases_in_group,
        db.deaths_in_group,
        db.recovered_in_group
    FROM demographic_breakdown db
    JOIN demographic_group dg ON db.demo_id = dg.demo_id;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
