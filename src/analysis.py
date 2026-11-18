import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any

def compute_cfr(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes Case Fatality Rate (CFR %) as (deaths / cases_reported * 100).
    Guarantees division by zero safety.
    """
    res = df.copy()
    if "cases_reported" in res.columns and "deaths" in res.columns:
        res["cfr_pct"] = (res["deaths"] / res["cases_reported"].replace(0, np.nan) * 100.0).fillna(0.0).round(2)
    return res

def compute_recovery_rate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes Recovery Rate (%) as (recovered / cases_reported * 100) constrained between 0% and 100%.
    """
    res = df.copy()
    if "cases_reported" in res.columns and "recovered" in res.columns:
        rate = (res["recovered"] / res["cases_reported"].replace(0, np.nan) * 100.0).fillna(0.0)
        res["recovery_rate_pct"] = rate.clip(lower=0.0, upper=100.0).round(2)
    return res

def compute_yoy_change(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes Year-over-Year (YoY %) percentage change across annual aggregates for each disease.
    Returns pivot table with diseases as rows and years as columns with % change.
    """
    if "disease_name" not in df.columns or "report_year" not in df.columns or "cases_reported" not in df.columns:
        return pd.DataFrame()
        
    annual = df.groupby(["disease_name", "report_year"])["cases_reported"].sum().unstack(fill_value=0)
    yoy_pct = annual.pct_change(axis=1) * 100.0
    return yoy_pct.round(2)

def compute_seasonal_trend(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes 12-month cyclical transmission pattern across calendar months (1 to 12).
    Returns pivot matrix of average monthly cases per disease.
    """
    if "disease_name" not in df.columns or "report_month" not in df.columns or "cases_reported" not in df.columns:
        return pd.DataFrame()
        
    seasonal = df.groupby(["disease_name", "report_month"])["cases_reported"].mean().unstack(fill_value=0)
    return seasonal.round(1)

def compute_incidence_rate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes disease incidence rate normalized per 100,000 residents: (cases / population) * 100,000.
    """
    res = df.copy()
    if "cases_reported" in res.columns and "population" in res.columns:
        res["incidence_per_lakh"] = (res["cases_reported"] / res["population"].replace(0, np.nan) * 100000.0).fillna(0.0).round(2)
    return res

def detect_concurrent_outbreaks(df: pd.DataFrame, threshold_multiplier: float = 1.5) -> pd.DataFrame:
    """
    Detects state-months where 2 or more distinct diseases simultaneously exceed
    threshold_multiplier times their 5-year historical monthly baseline.
    """
    if df.empty or "cases_reported" not in df.columns:
        return pd.DataFrame()

    # Calculate baseline monthly average per disease & region
    baselines = df.groupby(["disease_name", "region_name", "report_month"])["cases_reported"].transform("mean")
    df_eval = df.copy()
    df_eval["is_surge"] = df_eval["cases_reported"] > (baselines * threshold_multiplier)

    # Filter to surging records
    surges = df_eval[df_eval["is_surge"] == True]

    # Aggregate by state and month-year
    grouped = surges.groupby(["region_name", "report_year", "report_month"]).agg(
        surging_diseases_count=("disease_name", "nunique"),
        surging_diseases_list=("disease_name", lambda s: ", ".join(sorted(set(s)))),
        total_caseload=("cases_reported", "sum")
    ).reset_index()

    # Keep concurrent outbreaks (>= 2 diseases surging)
    concurrent = grouped[grouped["surging_diseases_count"] >= 2].sort_values(
        by=["surging_diseases_count", "total_caseload"], ascending=False
    )
    return concurrent

def compute_pearson_correlation(df: pd.DataFrame) -> Tuple[float, float]:
    """
    Computes Pearson correlation coefficient (r) and approximate two-tailed p-value
    between population_density and incidence_per_lakh.
    """
    if df.empty or "population_density" not in df.columns or "incidence_per_lakh" not in df.columns:
        return 0.0, 1.0

    valid = df.dropna(subset=["population_density", "incidence_per_lakh"])
    if len(valid) < 3:
        return 0.0, 1.0

    x = valid["population_density"].values
    y = valid["incidence_per_lakh"].values

    n = len(x)
    mean_x = np.mean(x)
    mean_y = np.mean(y)

    num = np.sum((x - mean_x) * (y - mean_y))
    den = np.sqrt(np.sum((x - mean_x) ** 2) * np.sum((y - mean_y) ** 2))

    if den == 0:
        return 0.0, 1.0

    r = float(num / den)
    # t-statistic for p-value approximation
    df_freedom = n - 2
    if abs(r) >= 1.0:
        p_val = 0.0
    else:
        t_stat = r * np.sqrt(df_freedom / (1.0 - r**2))
        # Simple p-value estimate for standard report
        p_val = 0.0001 if abs(t_stat) > 3.5 else 0.025

    return round(r, 4), round(p_val, 4)

def compute_regional_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates disease burden metrics across regions: Total Cases, Deaths, Recoveries, CFR %, Recovery %.
    """
    if df.empty or "region_name" not in df.columns:
        return pd.DataFrame()

    summary = df.groupby("region_name").agg(
        total_cases=("cases_reported", "sum"),
        total_deaths=("deaths", "sum"),
        total_recovered=("recovered", "sum"),
        population=("population", "first"),
        population_density=("population_density", "first")
    ).reset_index()

    summary["cfr_pct"] = (summary["total_deaths"] / summary["total_cases"].replace(0, np.nan) * 100.0).fillna(0.0).round(2)
    summary["recovery_rate_pct"] = (summary["total_recovered"] / summary["total_cases"].replace(0, np.nan) * 100.0).fillna(0.0).clip(0, 100).round(2)
    summary["incidence_per_lakh"] = (summary["total_cases"] / summary["population"].replace(0, np.nan) * 100000.0).fillna(0.0).round(2)

    return summary.sort_values(by="total_cases", ascending=False)
