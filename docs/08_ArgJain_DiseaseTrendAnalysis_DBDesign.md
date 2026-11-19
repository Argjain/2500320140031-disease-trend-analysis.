# 08 ArgJain DiseaseTrendAnalysis DBDesign

> Official Project Spreadsheet Artifact: `08_ArgJain_DiseaseTrendAnalysis_DBDesign.xlsx`


## 📊 Sheet: Overview (11 rows)

| DISEASE TREND ANALYSIS — RELATIONAL DATABASE ARCHITECTURE | Unnamed: 1 |
| --- | --- |
| — | — |
| Project ID & Title | P-01 / Disease Trend Analysis |
| Domain | Healthcare Data Analytics / Public Health Surveillance |
| Architect | Arg Jain (Roll No. 2500320140031), MCA 2nd Yr DA, ABES |
| Faculty Mentor | Ms. Kalpana Dwivedi |
| Database Engine | SQLite 3 (Serverless Relational Engine with Foreign Key Support) |
| Normalization Standard | Third Normal Form (3NF) for Base Tables + Denormalized Analytical View |
| Total Entity Tables | 5 Base Tables (3 Masters + 1 Main Fact + 1 Demographic Fact) |
| Analytical Views | 1 Materialized Query View (v_disease_analysis with ~35 columns) |
| Observation Scope | 5 Diseases, 10 States, 60 Months (2020-2024), 5 Age Groups, 3 Genders |
| Fact Table Volume | 3,003 Rows in disease_cases (including 3 audit test duplicates) |



## 📊 Sheet: Tables_Summary (6 rows)

| Table Name | Table Type | Granularity (Grain) | Primary Key | Foreign Keys | Columns Count | Est. Rows | Architectural Role |
| --- | --- | --- | --- | --- | --- | --- | --- |
| disease_master | Master / Dimension | One record per disease entity | disease_id | — | 6 | 5 | Reference taxonomy & contagion metadata |
| region_master | Master / Dimension | One record per Indian state | region_id | — | 7 | 10 | Geospatial attributes & census population/area |
| demographic_group | Master / Dimension | One record per age cohort x gender | demo_id | — | 5 | 15 | Demographic classification matrix |
| disease_cases | Transaction Fact | Disease x State x Calendar Month | case_id | disease_id, region_id | 14 | 3003 | Core incident cases, deaths, recoveries & active |
| demographic_breakdown | Sub-fact / Bridge | Case Record x Demographic Group | breakdown_id | case_id, demo_id | 6 | 300 | Granular demographic distribution of cases |
| v_disease_analysis | Analytical View | Denormalized joined analytical record | case_id (logical) | Inherited from fact | 35 | 3000 | Unified querying view with computed KPIs |



## 📊 Sheet: DD_disease_master (6 rows)

| Column Name | Data Type | Key Type | Nullable | Allowed Values / Range | Description | OQ / BR Supported |
| --- | --- | --- | --- | --- | --- | --- |
| disease_id | INTEGER | PRIMARY KEY | No | 1 to 5 | Unique surrogate identifier for each disease | All OQs / BR-10 |
| disease_name | TEXT | UNIQUE | No | Dengue, Malaria, Tuberculosis, COVID-19, Typhoid | Standard clinical disease name | OQ-01, 02, 03 / BR-01 |
| disease_category | TEXT | — | No | Vector-borne, Airborne, Waterborne | Epidemiological transmission vector | OQ-03, 10 / BR-06 |
| description | TEXT | — | Yes | Free text description | Clinical summary and pathogen pathology | Informational |
| is_contagious | INTEGER | — | No | 0 or 1 (CHECK) | Binary indicator for human-to-human transmission | BR-01, BR-05 |
| typical_incubation_days | INTEGER | — | No | 1 to 60 | Standard incubation period in days | BR-05, BR-06 |



## 📊 Sheet: DD_region_master (7 rows)

| Column Name | Data Type | Key Type | Nullable | Allowed Values / Range | Description | OQ / BR Supported |
| --- | --- | --- | --- | --- | --- | --- |
| region_id | INTEGER | PRIMARY KEY | No | 1 to 10 | Surrogate key for state boundary | All OQs / BR-10 |
| region_name | TEXT | UNIQUE | No | Uttar Pradesh, Maharashtra, Delhi, Rajasthan, Bihar, West Bengal, Tamil Nadu, Karnataka, Gujarat, Madhya Pradesh | Official Indian state/UT name | OQ-02, 05 / BR-02 |
| state_code | TEXT | UNIQUE | No | UP, MH, DL, RJ, BR, WB, TN, KA, GJ, MP | Two-letter ISO state code | OQ-02 / BR-02 |
| zone | TEXT | — | No | North, South, East, West, Central | Geographic administrative zone of India | OQ-02 / BR-02 |
| population | INTEGER | — | No | > 0 (1M to 250M) | Census population count | OQ-06 / BR-08 |
| area_sqkm | REAL | — | No | > 0 (1,000 to 350,000) | Geographic surface area in square kilometers | OQ-06 / BR-08 |
| population_density | REAL | — | No | population / area_sqkm | Derived population density (persons per sq. km) | OQ-06 / BR-08 |



## 📊 Sheet: DD_demographic_group (5 rows)

| Column Name | Data Type | Key Type | Nullable | Allowed Values / Range | Description | OQ / BR Supported |
| --- | --- | --- | --- | --- | --- | --- |
| demo_id | INTEGER | PRIMARY KEY | No | 1 to 15 | Unique demographic cohort identifier | OQ-04 / BR-04 |
| age_group | TEXT | — | No | 0-14, 15-29, 30-44, 45-59, 60+ | Standard 15-year age cohort bracket | OQ-04 / BR-04 |
| gender | TEXT | — | No | Male, Female, Other | Biological and social gender identity | OQ-04 / BR-04 |
| age_min | INTEGER | — | No | 0 to 60 | Lower age bound (inclusive) | OQ-04 / BR-04 |
| age_max | INTEGER | — | No | 14 to 99 | Upper age bound (inclusive) | OQ-04 / BR-04 |



## 📊 Sheet: DD_disease_cases (14 rows)

| Column Name | Data Type | Key Type | Nullable | Allowed Values / Range | Description | OQ / BR Supported |
| --- | --- | --- | --- | --- | --- | --- |
| case_id | INTEGER | PRIMARY KEY | No | 1 to 3003 | Unique surrogate transactional transaction key | All OQs / BR-10 |
| disease_id | INTEGER | FOREIGN KEY | No | References disease_master(disease_id) | FK link to disease entity | All OQs / BR-01 |
| region_id | INTEGER | FOREIGN KEY | No | References region_master(region_id) | FK link to geographic state | All OQs / BR-02 |
| report_date | DATE | — | No | 2020-01-01 to 2024-12-01 | First day of the reporting month (ISO 8601) | OQ-01, 03, 09 / BR-01 |
| report_year | INTEGER | — | No | 2020, 2021, 2022, 2023, 2024 | Calendar observation year for fast filtering | OQ-01, 09 / BR-01, 09 |
| report_month | INTEGER | — | No | 1 to 12 | Calendar month (1=Jan .. 12=Dec) | OQ-03, 10 / BR-06 |
| cases_reported | INTEGER | — | No (Cleaned) | >= 0 (CHECK) | Total clinical confirmed incident cases in state-month | OQ-01, 02 / BR-01 |
| deaths | INTEGER | — | No (Cleaned) | 0 <= deaths <= cases_reported (CHECK) | Reported disease-specific mortalities | OQ-05 / BR-03 |
| recovered | INTEGER | — | No | 0 <= recovered <= cases_reported (CHECK) | Documented clinical discharges / recoveries | OQ-07 / BR-07 |
| active_cases | INTEGER | — | No | cases - deaths - recovered (>= 0) | Net ongoing active caseload at month end | BR-01, BR-02 |
| hospitalized | INTEGER | — | No | 0 <= hospitalized <= cases_reported | Caseload requiring in-patient bed admission | BR-02 |
| is_outbreak | INTEGER | — | No | 0 or 1 | Outbreak anomaly flag (cases > 1.5x historical mean) | OQ-08 / BR-05 |
| data_source | TEXT | — | No | ICMR Synthetic, State Health Dept, WHO India | Originating reporting institutional body | Audit / BR-10 |
| created_at | TIMESTAMP | — | No | ISO timestamp | Database load and audit creation timestamp | Audit / BR-10 |



## 📊 Sheet: DD_demographic_breakdown (6 rows)

| Column Name | Data Type | Key Type | Nullable | Allowed Values / Range | Description | OQ / BR Supported |
| --- | --- | --- | --- | --- | --- | --- |
| breakdown_id | INTEGER | PRIMARY KEY | No | 1 to 300+ | Surrogate identifier for demographic slice | OQ-04 / BR-04 |
| case_id | INTEGER | FOREIGN KEY | No | References disease_cases(case_id) | Foreign key link to specific state-month case batch | OQ-04 / BR-04 |
| demo_id | INTEGER | FOREIGN KEY | No | References demographic_group(demo_id) | Foreign key link to demographic cohort | OQ-04 / BR-04 |
| cases_in_group | INTEGER | — | No | >= 0 | Number of incident cases belonging to this demographic cohort | OQ-04 / BR-04 |
| deaths_in_group | INTEGER | — | No | 0 <= deaths <= cases_in_group | Number of fatalities within this cohort | OQ-04 / BR-04 |
| recovered_in_group | INTEGER | — | No | 0 <= recov <= cases_in_group | Number of patient recoveries within this cohort | OQ-04 / BR-04 |



## 📊 Sheet: Relationships (4 rows)

| Relationship ID | Parent Table | Child Table | Foreign Key / Join Column | Cardinality | Referential Rule | Operational Purpose |
| --- | --- | --- | --- | --- | --- | --- |
| REL-01 | disease_master | disease_cases | disease_id | One-to-Many (1:N) | ON DELETE RESTRICT | Every disease case record must reference a valid disease entity. |
| REL-02 | region_master | disease_cases | region_id | One-to-Many (1:N) | ON DELETE RESTRICT | Every disease case record must belong to a known state jurisdiction. |
| REL-03 | disease_cases | demographic_breakdown | case_id | One-to-Many (1:N) | ON DELETE CASCADE | Case records are partitioned into detailed demographic sub-slices. |
| REL-04 | demographic_group | demographic_breakdown | demo_id | One-to-Many (1:N) | ON DELETE RESTRICT | Every demographic breakdown row references a valid age-gender cohort. |



## 📊 Sheet: KPIs_Measures (9 rows)

| Measure / KPI Name | Mathematical Formula | Units | Aggregation Grain | Governing OQ | Governing BR |
| --- | --- | --- | --- | --- | --- |
| Total Incident Cases | SUM(cases_reported) | Count (Cases) | Dynamic per Filter Slice | OQ-01, 02 | BR-01, BR-02 |
| Total Fatalities | SUM(deaths) | Count (Deaths) | Dynamic per Filter Slice | OQ-05 | BR-03 |
| Total Recoveries | SUM(recovered) | Count (Patients) | Dynamic per Filter Slice | OQ-07 | BR-07 |
| Case Fatality Rate (CFR %) | (SUM(deaths) / SUM(cases_reported)) * 100 | Percentage (0.00%) | Per Disease / State / Period | OQ-05 | BR-03 |
| Clinical Recovery Rate (%) | (SUM(recovered) / SUM(cases_reported)) * 100 | Percentage (0.00%) | Per Disease / State / Period | OQ-07 | BR-07 |
| Incidence per Lakh | (SUM(cases) / population) * 100,000 | Rate per 100,000 | State Annual / Monthly | OQ-06 | BR-08 |
| Year-over-Year Delta (YoY %) | ((Cases_t - Cases_t-1) / Cases_t-1) * 100 | Percentage (+/- 0.0%) | Annual per Disease | OQ-09 | BR-09 |
| Seasonal Transmission Index | AVG(cases_month) / AVG(cases_annual) | Normalized Ratio | Calendar Month (1-12) | OQ-03, 10 | BR-06 |
| Concurrent Outbreak Flag | COUNT(Diseases where Cases > 1.5 * Mean) >= 2 | Binary (1 / 0) | State-Month Level | OQ-08 | BR-05 |



## 📊 Sheet: SQLite_DDL (24 rows)

| EXECUTABLE SQLITE DDL STATEMENTS |
| --- |
| — |
| -- PRAGMA Settings |
| PRAGMA foreign_keys = ON; |
| — |
| -- TABLE: disease_master |
| CREATE TABLE IF NOT EXISTS disease_master (     disease_id INTEGER PRIMARY KEY,     disease_name TEXT NOT NULL UNIQUE,     disease_category TEXT NOT NULL,     description TEXT,     is_contagious INTEGER NOT NULL CHECK (is_contagious IN (0, 1)),     typical_incubation_days INTEGER NOT NULL CHECK (typical_incubation_days > 0) ); |
| — |
| -- TABLE: region_master |
| CREATE TABLE IF NOT EXISTS region_master (     region_id INTEGER PRIMARY KEY,     region_name TEXT NOT NULL UNIQUE,     state_code TEXT NOT NULL UNIQUE,     zone TEXT NOT NULL,     population INTEGER NOT NULL CHECK (population > 0),     area_sqkm REAL NOT NULL CHECK (area_sqkm > 0),     population_density REAL NOT NULL CHECK (population_density >= 0) ); |
| — |
| -- TABLE: demographic_group |
| CREATE TABLE IF NOT EXISTS demographic_group (     demo_id INTEGER PRIMARY KEY,     age_group TEXT NOT NULL,     gender TEXT NOT NULL,     age_min INTEGER NOT NULL CHECK (age_min >= 0),     age_max INTEGER NOT NULL CHECK (age_max >= age_min),     UNIQUE (age_group, gender) ); |
| — |
| -- TABLE: disease_cases |
| CREATE TABLE IF NOT EXISTS disease_cases (     case_id INTEGER PRIMARY KEY,     disease_id INTEGER NOT NULL,     region_id INTEGER NOT NULL,     report_date DATE NOT NULL,     report_year INTEGER NOT NULL CHECK (report_year BETWEEN 2020 AND 2026),     report_month INTEGER NOT NULL CHECK (report_month BETWEEN 1 AND 12),     cases_reported INTEGER NOT NULL CHECK (cases_reported >= 0),     deaths INTEGER NOT NULL CHECK (deaths >= 0 AND deaths <= cases_reported),     recovered INTEGER NOT NULL CHECK (recovered >= 0 AND recovered <= cases_reported),     active_cases INTEGER NOT NULL CHECK (active_cases >= 0),     hospitalized INTEGER NOT NULL CHECK (hospitalized >= 0 AND hospitalized <= cases_reported),     is_outbreak INTEGER NOT NULL CHECK (is_outbreak IN (0, 1)),     data_source TEXT NOT NULL,     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,     FOREIGN KEY (disease_id) REFERENCES disease_master (disease_id) ON DELETE RESTRICT,     FOREIGN KEY (region_id) REFERENCES region_master (region_id) ON DELETE RESTRICT ); |
| — |
| -- TABLE: demographic_breakdown |
| CREATE TABLE IF NOT EXISTS demographic_breakdown (     breakdown_id INTEGER PRIMARY KEY,     case_id INTEGER NOT NULL,     demo_id INTEGER NOT NULL,     cases_in_group INTEGER NOT NULL CHECK (cases_in_group >= 0),     deaths_in_group INTEGER NOT NULL CHECK (deaths_in_group >= 0 AND deaths_in_group <= cases_in_group),     recovered_in_group INTEGER NOT NULL CHECK (recovered_in_group >= 0 AND recovered_in_group <= cases_in_group),     FOREIGN KEY (case_id) REFERENCES disease_cases (case_id) ON DELETE CASCADE,     FOREIGN KEY (demo_id) REFERENCES demographic_group (demo_id) ON DELETE RESTRICT ); |
| — |
| -- INDEXES FOR QUERY ACCELERATION |
| CREATE INDEX IF NOT EXISTS idx_cases_disease ON disease_cases (disease_id); CREATE INDEX IF NOT EXISTS idx_cases_region ON disease_cases (region_id); CREATE INDEX IF NOT EXISTS idx_cases_date ON disease_cases (report_year, report_month); CREATE INDEX IF NOT EXISTS idx_breakdown_case ON demographic_breakdown (case_id); CREATE INDEX IF NOT EXISTS idx_breakdown_demo ON demographic_breakdown (demo_id); |
| — |
| -- VIEW: v_disease_analysis |
| CREATE VIEW IF NOT EXISTS v_disease_analysis AS SELECT     dc.case_id,     dc.report_date,     dc.report_year,     dc.report_month,     dm.disease_id,     dm.disease_name,     dm.disease_category,     dm.is_contagious,     rm.region_id,     rm.region_name,     rm.state_code,     rm.zone,     rm.population,     rm.area_sqkm,     rm.population_density,     dc.cases_reported,     dc.deaths,     dc.recovered,     dc.active_cases,     dc.hospitalized,     dc.is_outbreak,     ROUND(CAST(dc.deaths AS REAL) / NULLIF(dc.cases_reported, 0) * 100, 2) AS cfr_pct,     ROUND(CAST(dc.recovered AS REAL) / NULLIF(dc.cases_reported, 0) * 100, 2) AS recovery_rate_pct,     ROUND(CAST(dc.cases_reported AS REAL) / rm.population * 100000, 2) AS incidence_per_lakh,     dc.data_source,     dc.created_at FROM disease_cases dc JOIN disease_master dm ON dc.disease_id = dm.disease_id JOIN region_master rm ON dc.region_id = rm.region_id; |

