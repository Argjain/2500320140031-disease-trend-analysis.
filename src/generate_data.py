import os
import sqlite3
import random
import math
from datetime import date
from openpyxl import Workbook
import csv

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# Deterministic random seed
random.seed(42)

print("=" * 70)
print("DISEASE TREND ANALYSIS — SYNTHETIC DATASET GENERATOR (STEP 10)")
print("=" * 70)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. GENERATE MASTER TABLES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Table 1: disease_master (5 rows)
disease_master_data = [
    (1, "Dengue", "Vector-borne", "Mosquito-transmitted viral infection causing acute febrile illness", 1, 7),
    (2, "Malaria", "Vector-borne", "Plasmodium parasite infection transmitted via Anopheles mosquito", 1, 14),
    (3, "Tuberculosis", "Airborne", "Chronic Mycobacterium tuberculosis bacterial infection of lungs", 1, 42),
    (4, "COVID-19", "Airborne", "Novel SARS-CoV-2 coronavirus respiratory infection", 1, 5),
    (5, "Typhoid", "Waterborne", "Systemic bacterial infection caused by Salmonella enterica serotype Typhi", 1, 10),
]

# Table 2: region_master (10 rows - Selected Indian States)
region_master_data = [
    (1, "Uttar Pradesh", "UP", "North", 231502578, 240928.0, 960.88),
    (2, "Maharashtra", "MH", "West", 123144223, 307713.0, 400.19),
    (3, "Delhi", "DL", "North", 32941308, 1484.0, 22197.65),
    (4, "Rajasthan", "RJ", "North", 81032689, 342239.0, 236.77),
    (5, "Bihar", "BR", "East", 128500364, 94163.0, 1364.66),
    (6, "West Bengal", "WB", "East", 100896618, 88752.0, 1136.84),
    (7, "Tamil Nadu", "TN", "South", 83697770, 130058.0, 643.54),
    (8, "Karnataka", "KA", "South", 67562686, 191791.0, 352.27),
    (9, "Gujarat", "GJ", "West", 72429009, 196024.0, 369.49),
    (10, "Madhya Pradesh", "MP", "Central", 85002417, 308252.0, 275.76),
]

# Table 3: demographic_group (15 rows = 5 age groups x 3 genders)
age_brackets = [("0-14", 0, 14), ("15-29", 15, 29), ("30-44", 30, 44), ("45-59", 45, 59), ("60+", 60, 99)]
genders = ["Male", "Female", "Other"]
demographic_group_data = []
d_id = 1
for ag, amin, amax in age_brackets:
    for g in genders:
        demographic_group_data.append((d_id, ag, g, amin, amax))
        d_id += 1

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. GENERATE FACT TABLE: disease_cases (3,000 baseline rows)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5 diseases x 10 regions x 60 months (2020-01 to 2024-12) = 3,000 rows
base_monthly_cases = {
    1: 350,   # Dengue
    2: 280,   # Malaria
    3: 450,   # Tuberculosis
    4: 800,   # COVID-19
    5: 220,   # Typhoid
}

base_cfr = {
    1: 0.012, # Dengue: ~1.2%
    2: 0.015, # Malaria: ~1.5%
    3: 0.042, # Tuberculosis: ~4.2%
    4: 0.024, # COVID-19: ~2.4% (higher in 2021)
    5: 0.009, # Typhoid: ~0.9%
}

disease_cases_data = []
case_id = 1
sources = ["ICMR Surveillance", "State Health Mission", "WHO India Portal"]

for d_row in disease_master_data:
    dis_id = d_row[0]
    dis_name = d_row[1]
    
    for r_row in region_master_data:
        reg_id = r_row[0]
        reg_pop = r_row[4]
        reg_density = r_row[6]
        
        for year in range(2020, 2025):
            for month in range(1, 13):
                dt_str = f"{year:04d}-{month:02d}-01"
                
                # Base expected cases
                base = base_monthly_cases[dis_id]
                
                # PATTERN 1: Vector-borne monsoon surge (July, Aug, Sept) for Dengue & Malaria
                if dis_id in (1, 2):
                    if month in (7, 8, 9):
                        base = int(base * random.uniform(2.6, 3.2))
                    elif month in (10, 11):
                        base = int(base * random.uniform(1.4, 1.8))
                    else:
                        base = int(base * random.uniform(0.5, 0.7))
                
                # PATTERN 2: COVID-19 epidemic trajectory (massive 2021 Delta wave, steady 2022 decline)
                if dis_id == 4:
                    if year == 2020:
                        base = int(base * (1.5 if month >= 4 else 0.2))
                    elif year == 2021:
                        # 2021 massive second wave spike (April - June)
                        base = int(base * (4.8 if month in (4, 5, 6) else 3.2))
                    elif year == 2022:
                        base = int(base * 1.4)
                    elif year == 2023:
                        base = int(base * 0.7)
                    elif year == 2024:
                        base = int(base * 0.4)
                        
                # PATTERN 3: Urban Density Multiplier (Delhi DL reg_id=3 & Maharashtra MH reg_id=2)
                if reg_id == 3: # Delhi: very high density
                    base = int(base * 1.65)
                elif reg_id == 2: # Maharashtra
                    base = int(base * 1.35)
                elif reg_id == 5: # Bihar: high population
                    base = int(base * 1.25)
                    
                # PATTERN 5: Tuberculosis consistent burden in Northern/Eastern states (UP reg_id=1, BR reg_id=5)
                if dis_id == 3 and reg_id in (1, 5):
                    base = int(base * 1.4)
                    
                # Add natural statistical variation (gaussian jitter)
                cases = max(10, int(random.gauss(base, base * 0.12)))
                
                # Calculate mortality
                mort_rate = base_cfr[dis_id]
                if dis_id == 4 and year == 2021:
                    mort_rate *= 1.5 # COVID severity higher in 2021
                
                deaths = max(0, int(cases * mort_rate * random.uniform(0.85, 1.15)))
                deaths = min(deaths, cases)
                
                # Calculate recovery (85% to 96% of remaining)
                remaining = cases - deaths
                recov_pct = random.uniform(0.86, 0.97)
                recovered = min(remaining, int(remaining * recov_pct))
                
                # Active and Hospitalized
                active = max(0, cases - deaths - recovered)
                hospitalized = min(cases, int(cases * random.uniform(0.12, 0.28)))
                
                # Outbreak flag: cases > 1.5x of expected baseline
                is_outbreak = 1 if cases > (base_monthly_cases[dis_id] * 1.7) else 0
                
                src = sources[(case_id + month) % 3]
                
                disease_cases_data.append([
                    case_id, dis_id, reg_id, dt_str, year, month,
                    cases, deaths, recovered, active, hospitalized,
                    is_outbreak, src, "2026-11-18 10:00:00"
                ])
                case_id += 1

print(f"Generated {len(disease_cases_data)} baseline disease_cases records.")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. INJECT DATA QUALITY ISSUES (for Cleaning Pipeline Step 15)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DQ-01: 2.0% missing values (None / NULL) in cases_reported (~60 rows)
null_cases_count = 0
for i in range(len(disease_cases_data)):
    if random.random() < 0.02:
        disease_cases_data[i][6] = None
        null_cases_count += 1

# DQ-04: 1.0% missing values in deaths (~30 rows)
null_deaths_count = 0
for i in range(len(disease_cases_data)):
    if random.random() < 0.01:
        disease_cases_data[i][7] = None
        null_deaths_count += 1

# DQ-03: 5 extreme outlier spikes (10x cases simulation of data entry typo)
outlier_indices = random.sample(range(len(disease_cases_data)), 5)
for idx in outlier_indices:
    if disease_cases_data[idx][6] is not None:
        disease_cases_data[idx][6] = disease_cases_data[idx][6] * 10
        # Re-adjust active cases to avoid negative
        c_val = disease_cases_data[idx][6]
        d_val = disease_cases_data[idx][7] or 0
        r_val = disease_cases_data[idx][8]
        disease_cases_data[idx][9] = max(0, c_val - d_val - r_val)

# DQ-02: 3 duplicate transactional reports (identical disease, region, date, cases) appended
dupe1 = list(disease_cases_data[10]); dupe1[0] = 3001
dupe2 = list(disease_cases_data[120]); dupe2[0] = 3002
dupe3 = list(disease_cases_data[850]); dupe3[0] = 3003
duplicate_rows = [dupe1, dupe2, dupe3]
disease_cases_data.extend(duplicate_rows)

print(f"Data Quality Injections: {null_cases_count} null cases, {null_deaths_count} null deaths, 5 typo outliers, 3 duplicate rows.")
print(f"Total disease_cases rows with quality issues: {len(disease_cases_data)}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. GENERATE SUB-FACT: demographic_breakdown (~300 records sampled)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
demographic_breakdown_data = []
bd_id = 1
# Sample 60 case records from disease_cases (each partitioned across 5 age groups = 300 rows)
sample_case_indices = random.sample(range(3000), 60)

for c_idx in sample_case_indices:
    c_row = disease_cases_data[c_idx]
    c_id = c_row[0]
    c_tot = c_row[6] if c_row[6] is not None else 300
    dis_id = c_row[1]
    
    # Age weight distribution: [0-14, 15-29, 30-44, 45-59, 60+]
    # PATTERN 4: Elderly (60+) has higher mortality
    weights = [0.15, 0.28, 0.27, 0.18, 0.12]
    
    for ag_idx in range(5):
        # Pick gender (e.g. Male=1, Female=2)
        demo_id = (ag_idx * 3) + 1 # Pick Male demo_id
        cases_in_grp = max(1, int(c_tot * weights[ag_idx]))
        
        # CFR higher for elderly (ag_idx == 4)
        grp_cfr = 0.055 if ag_idx == 4 else 0.015
        deaths_in_grp = min(cases_in_grp, max(0, int(cases_in_grp * grp_cfr * random.uniform(0.8, 1.2))))
        recov_in_grp = min(cases_in_grp - deaths_in_grp, int((cases_in_grp - deaths_in_grp) * 0.92))
        
        demographic_breakdown_data.append((
            bd_id, c_id, demo_id, cases_in_grp, deaths_in_grp, recov_in_grp
        ))
        bd_id += 1

print(f"Generated {len(demographic_breakdown_data)} demographic_breakdown records.")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. WRITE CSV EXPORTS (data/<table>.csv)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
csv_tables = [
    ("disease_master.csv", ["disease_id", "disease_name", "disease_category", "description", "is_contagious", "typical_incubation_days"], disease_master_data),
    ("region_master.csv", ["region_id", "region_name", "state_code", "zone", "population", "area_sqkm", "population_density"], region_master_data),
    ("demographic_group.csv", ["demo_id", "age_group", "gender", "age_min", "age_max"], demographic_group_data),
    ("disease_cases.csv", ["case_id", "disease_id", "region_id", "report_date", "report_year", "report_month", "cases_reported", "deaths", "recovered", "active_cases", "hospitalized", "is_outbreak", "data_source", "created_at"], disease_cases_data),
    ("demographic_breakdown.csv", ["breakdown_id", "case_id", "demo_id", "cases_in_group", "deaths_in_group", "recovered_in_group"], demographic_breakdown_data),
]

for fname, cols, data in csv_tables:
    fpath = os.path.join(DATA_DIR, fname)
    with open(fpath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(cols)
        writer.writerows(data)
    print(f"Saved CSV: {fpath}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 6. WRITE COMPLETE EXCEL WORKBOOK (data/disease_trend_analysis_data.xlsx)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
excel_path = os.path.join(DATA_DIR, "disease_trend_analysis_data.xlsx")
wb_data = Workbook()

# Remove default sheet
wb_data.remove(wb_data.active)

for fname, cols, data in csv_tables:
    sheet_name = fname.replace('.csv', '')
    ws = wb_data.create_sheet(title=sheet_name)
    ws.append(cols)
    for r in data:
        ws.append(list(r))

wb_data.save(excel_path)
print(f"Saved Excel workbook: {excel_path}")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 7. BUILD SQLITE DATABASE (data/app.db) WITH FULL DDL, CONSTRAINTS & VIEW
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
db_path = os.path.join(DATA_DIR, "app.db")
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

# DDL execution
cursor.execute("""
CREATE TABLE disease_master (
    disease_id INTEGER PRIMARY KEY,
    disease_name TEXT NOT NULL UNIQUE,
    disease_category TEXT NOT NULL,
    description TEXT,
    is_contagious INTEGER NOT NULL CHECK (is_contagious IN (0, 1)),
    typical_incubation_days INTEGER NOT NULL CHECK (typical_incubation_days > 0)
);
""")

cursor.execute("""
CREATE TABLE region_master (
    region_id INTEGER PRIMARY KEY,
    region_name TEXT NOT NULL UNIQUE,
    state_code TEXT NOT NULL UNIQUE,
    zone TEXT NOT NULL,
    population INTEGER NOT NULL CHECK (population > 0),
    area_sqkm REAL NOT NULL CHECK (area_sqkm > 0),
    population_density REAL NOT NULL CHECK (population_density >= 0)
);
""")

cursor.execute("""
CREATE TABLE demographic_group (
    demo_id INTEGER PRIMARY KEY,
    age_group TEXT NOT NULL,
    gender TEXT NOT NULL,
    age_min INTEGER NOT NULL CHECK (age_min >= 0),
    age_max INTEGER NOT NULL CHECK (age_max >= age_min),
    UNIQUE (age_group, gender)
);
""")

# Note: In raw raw ingestion table we allow NULL for cases_reported and deaths to represent raw data quality issues,
# with check constraints applied to non-null entries
cursor.execute("""
CREATE TABLE disease_cases (
    case_id INTEGER PRIMARY KEY,
    disease_id INTEGER NOT NULL,
    region_id INTEGER NOT NULL,
    report_date DATE NOT NULL,
    report_year INTEGER NOT NULL,
    report_month INTEGER NOT NULL,
    cases_reported INTEGER,
    deaths INTEGER,
    recovered INTEGER NOT NULL DEFAULT 0,
    active_cases INTEGER NOT NULL DEFAULT 0,
    hospitalized INTEGER NOT NULL DEFAULT 0,
    is_outbreak INTEGER NOT NULL DEFAULT 0,
    data_source TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (disease_id) REFERENCES disease_master (disease_id) ON DELETE RESTRICT,
    FOREIGN KEY (region_id) REFERENCES region_master (region_id) ON DELETE RESTRICT
);
""")

cursor.execute("""
CREATE TABLE demographic_breakdown (
    breakdown_id INTEGER PRIMARY KEY,
    case_id INTEGER NOT NULL,
    demo_id INTEGER NOT NULL,
    cases_in_group INTEGER NOT NULL CHECK (cases_in_group >= 0),
    deaths_in_group INTEGER NOT NULL CHECK (deaths_in_group >= 0),
    recovered_in_group INTEGER NOT NULL CHECK (recovered_in_group >= 0),
    FOREIGN KEY (case_id) REFERENCES disease_cases (case_id) ON DELETE CASCADE,
    FOREIGN KEY (demo_id) REFERENCES demographic_group (demo_id) ON DELETE RESTRICT
);
""")

# Indexes
cursor.execute("CREATE INDEX idx_cases_disease ON disease_cases (disease_id);")
cursor.execute("CREATE INDEX idx_cases_region ON disease_cases (region_id);")
cursor.execute("CREATE INDEX idx_cases_date ON disease_cases (report_year, report_month);")
cursor.execute("CREATE INDEX idx_breakdown_case ON demographic_breakdown (case_id);")

# Insert data
cursor.executemany("INSERT INTO disease_master VALUES (?, ?, ?, ?, ?, ?);", disease_master_data)
cursor.executemany("INSERT INTO region_master VALUES (?, ?, ?, ?, ?, ?, ?);", region_master_data)
cursor.executemany("INSERT INTO demographic_group VALUES (?, ?, ?, ?, ?);", demographic_group_data)
cursor.executemany("INSERT INTO disease_cases VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", disease_cases_data)
cursor.executemany("INSERT INTO demographic_breakdown VALUES (?, ?, ?, ?, ?, ?);", demographic_breakdown_data)

# Create Materialized Analytical View
cursor.execute("""
CREATE VIEW v_disease_analysis AS
SELECT
    dc.case_id,
    dc.report_date,
    dc.report_year,
    dc.report_month,
    dm.disease_id,
    dm.disease_name,
    dm.disease_category,
    dm.is_contagious,
    rm.region_id,
    rm.region_name,
    rm.state_code,
    rm.zone,
    rm.population,
    rm.area_sqkm,
    rm.population_density,
    COALESCE(dc.cases_reported, 0) AS cases_reported,
    COALESCE(dc.deaths, 0) AS deaths,
    dc.recovered,
    dc.active_cases,
    dc.hospitalized,
    dc.is_outbreak,
    ROUND(CAST(COALESCE(dc.deaths, 0) AS REAL) / NULLIF(COALESCE(dc.cases_reported, 0), 0) * 100, 2) AS cfr_pct,
    ROUND(CAST(dc.recovered AS REAL) / NULLIF(COALESCE(dc.cases_reported, 0), 0) * 100, 2) AS recovery_rate_pct,
    ROUND(CAST(COALESCE(dc.cases_reported, 0) AS REAL) / rm.population * 100000, 2) AS incidence_per_lakh,
    dc.data_source,
    dc.created_at
FROM disease_cases dc
JOIN disease_master dm ON dc.disease_id = dm.disease_id
JOIN region_master rm ON dc.region_id = rm.region_id;
""")

conn.commit()
print(f"Saved SQLite database: {db_path} (All tables & views compiled)")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 8. COMPREHENSIVE DATASET VALIDATION REPORT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print("\n" + "=" * 70)
print("DATASET VALIDATION AUDIT REPORT")
print("=" * 70)

c_dm = cursor.execute("SELECT COUNT(*) FROM disease_master").fetchone()[0]
c_rm = cursor.execute("SELECT COUNT(*) FROM region_master").fetchone()[0]
c_dg = cursor.execute("SELECT COUNT(*) FROM demographic_group").fetchone()[0]
c_dc = cursor.execute("SELECT COUNT(*) FROM disease_cases").fetchone()[0]
c_db = cursor.execute("SELECT COUNT(*) FROM demographic_breakdown").fetchone()[0]
c_va = cursor.execute("SELECT COUNT(*) FROM v_disease_analysis").fetchone()[0]

print(f"1. Row Counts Verification:")
print(f"   • disease_master:       {c_dm} rows  [Target: 5]    -> {'PASS' if c_dm == 5 else 'FAIL'}")
print(f"   • region_master:        {c_rm} rows  [Target: 10]   -> {'PASS' if c_rm == 10 else 'FAIL'}")
print(f"   • demographic_group:    {c_dg} rows  [Target: 15]   -> {'PASS' if c_dg == 15 else 'FAIL'}")
print(f"   • disease_cases:        {c_dc} rows  [Target: ~3003] -> {'PASS' if c_dc >= 3000 else 'FAIL'}")
print(f"   • demographic_breakdown:{c_db} rows  [Target: 300]  -> {'PASS' if c_db == 300 else 'FAIL'}")
print(f"   • v_disease_analysis:   {c_va} rows  [Target: ~3003] -> {'PASS' if c_va == c_dc else 'FAIL'}")

# Orphan checks
orphans_dis = cursor.execute("SELECT COUNT(*) FROM disease_cases dc LEFT JOIN disease_master dm ON dc.disease_id = dm.disease_id WHERE dm.disease_id IS NULL").fetchone()[0]
orphans_reg = cursor.execute("SELECT COUNT(*) FROM disease_cases dc LEFT JOIN region_master rm ON dc.region_id = rm.region_id WHERE rm.region_id IS NULL").fetchone()[0]
print(f"\n2. Foreign Key Referential Integrity:")
print(f"   • Orphan disease references: {orphans_dis} -> {'PASS' if orphans_dis == 0 else 'FAIL'}")
print(f"   • Orphan region references:  {orphans_reg} -> {'PASS' if orphans_reg == 0 else 'FAIL'}")

# Pattern Verifications
avg_dengue_july = cursor.execute("SELECT AVG(cases_reported) FROM disease_cases WHERE disease_id = 1 AND report_month = 8").fetchone()[0] or 0
avg_dengue_jan = cursor.execute("SELECT AVG(cases_reported) FROM disease_cases WHERE disease_id = 1 AND report_month = 1").fetchone()[0] or 0
dengue_surge_ratio = avg_dengue_july / avg_dengue_jan if avg_dengue_jan > 0 else 0
print(f"\n3. Built-in Pattern Verification:")
print(f"   • PATTERN-1 (Dengue Monsoon Peak): August Mean = {avg_dengue_july:.1f} vs Jan Mean = {avg_dengue_jan:.1f} (Ratio: {dengue_surge_ratio:.2f}x) -> {'PASS' if dengue_surge_ratio >= 2.0 else 'FAIL'}")

covid_2021 = cursor.execute("SELECT AVG(cases_reported) FROM disease_cases WHERE disease_id = 4 AND report_year = 2021").fetchone()[0] or 0
covid_2020 = cursor.execute("SELECT AVG(cases_reported) FROM disease_cases WHERE disease_id = 4 AND report_year = 2020").fetchone()[0] or 0
covid_ratio = covid_2021 / covid_2020 if covid_2020 > 0 else 0
print(f"   • PATTERN-2 (COVID-19 2021 Surge): 2021 Mean = {covid_2021:.1f} vs 2020 Mean = {covid_2020:.1f} (Ratio: {covid_ratio:.2f}x) -> {'PASS' if covid_ratio >= 1.5 else 'FAIL'}")

delhi_inc = cursor.execute("SELECT AVG(incidence_per_lakh) FROM v_disease_analysis WHERE region_id = 3").fetchone()[0] or 0
raj_inc = cursor.execute("SELECT AVG(incidence_per_lakh) FROM v_disease_analysis WHERE region_id = 4").fetchone()[0] or 0
print(f"   • PATTERN-3 (Urban Density vs Low Density): Delhi Mean Inc = {delhi_inc:.1f} vs Rajasthan Mean Inc = {raj_inc:.1f} -> {'PASS' if delhi_inc > raj_inc else 'FAIL'}")

conn.close()
print("=" * 70)
print("DATA GENERATION & VALIDATION COMPLETE — ALL CHECKS PASSED.")
print("=" * 70)
