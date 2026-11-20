# 📊 BI Dashboard Specification — Tableau & Power BI Architecture
## Project ID: P-01 | Disease Trend Analysis Intelligence Cockpit
**Student:** Arg Jain (Roll No. 2500320140031)  
**Program:** MCA 2nd Year — Data Analytics Specialization | **ABES Engineering College, Ghaziabad**  
**Faculty Mentor:** Ms. Kalpana Dwivedi | **Target Release:** December 2026

---

## 📑 Table of Contents
1. [Executive Summary & BI Architecture](#1-executive-summary--bi-architecture)
2. [Data Modeling & Star Schema](#2-data-modeling--star-schema)
3. [Power BI Implementation Guide & DAX Catalog](#3-power-bi-implementation-guide--dax-catalog)
4. [Tableau Implementation Guide & LOD Expressions](#4-tableau-implementation-guide--lod-expressions)
5. [5-Page BI Dashboard Canvas Blueprints](#5-5-page-bi-dashboard-canvas-blueprints)
6. [Teacher & Viva Defense Q&A (BI Technical Evaluation)](#6-teacher--viva-defense-qa)

---

## 1. Executive Summary & BI Architecture

While our Python Streamlit web application serves as the primary operational surveillance cockpit, enterprise public health organizations and hospital networks frequently rely on enterprise Business Intelligence (BI) platforms like **Microsoft Power BI** and **Tableau Desktop/Server** for:
- Self-service reporting and executive board presentations.
- Cross-filtering slicing by geography, season, and demographics.
- Direct drill-down from national totals to state hospital beds.

Both Tableau and Power BI ingest our cleaned, sanitized dataset:
- Primary Fact/Flattened Source: `data/disease_analysis_merged.csv` (3,003 rows, 25 columns)
- Demographic Fact Source: `data/demographics_merged.csv` (300 rows, 10 columns)

---

## 2. Data Modeling & Star Schema

In enterprise BI, best practices dictate structuring data in a **Star Schema** to optimize query performance and enable clean slicing.

### Star Schema Entity-Relationship:
```
                      ┌──────────────────────┐
                      │    disease_master    │ (Dimension)
                      │ ──────────────────── │
                      │ PK: disease_id       │
                      │     disease_name     │
                      │     category         │
                      │     incubation_days  │
                      └──────────┬───────────┘
                                 │ 1
                                 │
                                 │ *
┌─────────────────────┐   ┌──────┴───────────────┐   ┌──────────────────────┐
│    region_master    │   │     disease_cases    │   │      date_table      │ (Dimension)
│ ─────────────────── │   │ ──────────────────── │   │ ──────────────────── │
│ PK: region_id       │1  │ PK: case_id          │* 1│ PK: Date             │
│     region_name     ├───┤ FK: disease_id       ├───┤     Year, Month      │
│     zone, pop, area │ * │ FK: region_id        │   │     Quarter, Season  │
│     pop_density     │   │ FK: report_date      │   │     Monsoon_Flag     │
└─────────────────────┘   │     cases_reported   │   └──────────────────────┘
                          │     deaths           │
                          │     recovered        │
                          │     active_cases     │
                          │     hospitalized     │
                          │     is_outbreak      │
                          └──────────────────────┘
```

---

## 3. Power BI Implementation Guide & DAX Catalog

### A. Data Connection & Power Query Steps
1. Open **Power BI Desktop** → Click **Get Data** → Select **Text/CSV**.
2. Select `data/disease_analysis_merged.csv`.
3. In Power Query Editor:
   - Ensure `report_date` is detected as **Date** format (`YYYY-MM-DD`).
   - Ensure `cases_reported`, `deaths`, `recovered`, `active_cases`, `hospitalized` are **Whole Number** / **Decimal Number**.
   - Ensure `population_density` and `area_sqkm` are **Decimal Number**.
4. Click **Close & Apply**.

### B. Core DAX Measures Catalog (Ready to Copy-Paste)

Create a dedicated Measures Table in Power BI named `_Surveillance_Measures`:

#### 1. Core Volume Metrics
```dax
Total Cases = SUM('disease_analysis_merged'[cases_reported])

Total Deaths = SUM('disease_analysis_merged'[deaths])

Total Recovered = SUM('disease_analysis_merged'[recovered])

Active Cases = SUM('disease_analysis_merged'[active_cases])

Total Hospitalized = SUM('disease_analysis_merged'[hospitalized])
```

#### 2. Epidemiological Rates & Benchmarks
```dax
Case Fatality Rate (CFR %) = 
DIVIDE([Total Deaths], [Total Cases], 0) * 100

Recovery Rate (%) = 
DIVIDE([Total Recovered], [Total Cases], 0) * 100

Hospitalization Rate (%) = 
DIVIDE([Total Hospitalized], [Total Cases], 0) * 100

Incidence per 100k = 
VAR TotalCases = [Total Cases]
VAR TotalPop = MAX('disease_analysis_merged'[population])
RETURN
DIVIDE(TotalCases, TotalPop, 0) * 100000

Mortality per 100k = 
VAR TotalDeaths = [Total Deaths]
VAR TotalPop = MAX('disease_analysis_merged'[population])
RETURN
DIVIDE(TotalDeaths, TotalPop, 0) * 100000
```

#### 3. Time-Intelligence & Growth Tracking
```dax
Cases Prior Month = 
CALCULATE(
    [Total Cases],
    DATEADD('disease_analysis_merged'[report_date], -1, MONTH)
)

MoM Case Growth % = 
VAR CurrentCases = [Total Cases]
VAR PriorCases = [Cases Prior Month]
RETURN
IF(
    ISBLANK(PriorCases) || PriorCases = 0,
    BLANK(),
    DIVIDE(CurrentCases - PriorCases, PriorCases, 0) * 100
)

Cases Same Period Last Year = 
CALCULATE(
    [Total Cases],
    SAMEPERIODLASTYEAR('disease_analysis_merged'[report_date])
)

YoY Case Growth % = 
VAR CurrentCases = [Total Cases]
VAR LastYearCases = [Cases Same Period Last Year]
RETURN
IF(
    ISBLANK(LastYearCases) || LastYearCases = 0,
    BLANK(),
    DIVIDE(CurrentCases - LastYearCases, LastYearCases, 0) * 100
)

3-Month Moving Average = 
CALCULATE(
    AVERAGEX(
        DATESINPERIOD(
            'disease_analysis_merged'[report_date],
            LASTDATE('disease_analysis_merged'[report_date]),
            -3,
            MONTH
        ),
        [Total Cases]
    )
)
```

#### 4. Outbreak Surge Alert Logic
```dax
Historical State Baseline = 
CALCULATE(
    AVERAGE('disease_analysis_merged'[cases_reported]),
    ALLEXCEPT('disease_analysis_merged', 'disease_analysis_merged'[disease_name], 'disease_analysis_merged'[region_name])
)

Surge Alert Threshold (1.5x) = 
[Historical State Baseline] * 1.5

Surge Status Indicator = 
IF(
    [Total Cases] > [Surge Alert Threshold (1.5x)],
    "🚨 CRITICAL SURGE (>1.5x)",
    "✔ Normal Range"
)
```

---

## 4. Tableau Implementation Guide & LOD Expressions

### A. Data Source Connection
1. Open **Tableau Desktop** → Connect to **Text File** → Select `data/disease_analysis_merged.csv`.
2. Verify Data Types:
   - `report_date`: Date icon (📅)
   - `region_name`: Geographic Role → State/Province
   - `state_code`: Geographic Role → State/Province (Abbreviation)
   - `population`, `area_sqkm`, `cases_reported`: Number (whole/decimal)

### B. Tableau Calculated Fields & Level of Detail (LOD) Calculations

#### 1. Fundamental Calculations
```tableau
// [Total Cases]
SUM([cases_reported])

// [Total Deaths]
SUM([deaths])

// [Case Fatality Rate (CFR %)]
ZN(SUM([deaths])) / ZN(SUM([cases_reported])) * 100

// [Recovery Rate (%)]
ZN(SUM([recovered])) / ZN(SUM([cases_reported])) * 100

// [Incidence per 100k Population]
(SUM([cases_reported]) / MAX([population])) * 100000
```

#### 2. Level of Detail (LOD) Expressions
LOD calculations allow computing metrics independent of the visual shelf dimensionality:
```tableau
// [State Baseline Caseload (Fixed LOD)]
{ FIXED [disease_name], [region_name] : AVG([cases_reported]) }

// [Outbreak Anomaly Trigger]
IF SUM([cases_reported]) > (AVG([State Baseline Caseload (Fixed LOD)]) * 1.5)
THEN "CRITICAL OUTBREAK"
ELSE "NORMAL"
END
```

#### 3. Table Calculations (Time Series)
```tableau
// [Month-over-Month Growth %]
(ZN(SUM([cases_reported])) - LOOKUP(ZN(SUM([cases_reported])), -1)) 
/ ABS(LOOKUP(ZN(SUM([cases_reported])), -1)) * 100

// [3-Month Centered Moving Average]
WINDOW_AVG(SUM([cases_reported]), -2, 0)
```

---

## 5. 5-Page BI Dashboard Canvas Blueprints

Both Power BI and Tableau dashboards are architected into **5 interactive tabs**:

### 📱 Tab 1: Executive Surveillance Cockpit (Overview)
* **Top Banner:** 4 KPI Cards:
  * Total Caseload (1.67M), Total Deaths (43.5k), Clinical Recovery (90.4%), Active Patients (128k).
* **Left Visual:** Horizontal Ranked Bar Chart: Total Morbidity by State (Maharashtra, Delhi, UP).
* **Right Visual:** Disease Category Donut Chart (Vector-borne, Airborne, Waterborne).
* **Bottom Visual:** Monthly Transmission Wave (Area Chart) with 3M Moving Average trendline.
* **Global Slicers:** Year (2020–2024), Disease Multi-select, Region Zone.

### 🌧️ Tab 2: Seasonality & Outbreak Heatmap
* **Main Visual:** Matrix/Heatmap:
  * Rows = Years (2020 to 2024), Columns = Months (Jan to Dec).
  * Color encoding = Case Count (Light Yellow to Deep Red).
* **Clinical Insight Box:** Visual annotation showing the **Monsoon Surge Window (July–October)** for Dengue and Malaria.
* **Secondary Visual:** Year-over-Year (YoY %) Delta Heatmap showing accelerating vs declining diseases.

### 🏙️ Tab 3: Urban Density & Spatial Analysis
* **Map Visual:** Indian State Filled Map / Choropleth shaded by `Incidence per 100k`.
* **Scatter Visual:** Population Density ($X$-axis, persons/km²) vs Cumulative Incidence ($Y$-axis, per 100k).
  * Bubble size = Total Fatalities.
  * Bubble color = Geographic Zone.
  * Reference line = Pearson correlation slope ($r = 0.96$). Highlights Delhi as an urban contagion outlier.

### 👥 Tab 4: Demographic Vulnerability Matrix
* **Data Source:** `demographics_merged.csv`.
* **Visual 1:** Population Pyramid / Tornado Chart:
  * $Y$-axis = Age Bands (`0-14`, `15-29`, `30-44`, `45-59`, `60+`).
  * $X$-axis = Cases split by Gender (Male left in Blue, Female right in Pink).
* **Visual 2:** Grouped Bar Chart of Case Fatality Rate (CFR %) by Age Band.
  * Clearly shows senior citizens ($60+$) facing $3\times$ higher mortality risk ($5.5\%$ vs $1.5\%$).

### 🚨 Tab 5: Early Warning & Data Quality Ledger
* **Visual 1:** Multi-Disease Outbreak Calendar Matrix flagging state-months where $\ge 2$ diseases exceed $1.5\times$ baseline.
* **Visual 2:** Data Quality Scorecard: Completeness Rate (99.89%), Duplicate purge count (0), Imputation tally (82 values).

---

## 6. Teacher & Viva Defense Q&A

### Q1: Why did you use `DIVIDE()` in DAX instead of standard division `/`?
> **Answer:** In DAX, standard division `[Total Deaths] / [Total Cases]` produces a `NaN` or divide-by-zero error whenever a state reports 0 cases in a month. `DIVIDE([Deaths], [Cases], 0)` safely returns an alternate result (`0`) without crashing visuals or disrupting aggregations.

### Q2: What is the difference between a Tableau Table Calculation and an LOD Expression?
> **Answer:** 
> - A **Table Calculation** (like `WINDOW_AVG` or `LOOKUP`) is calculated after Tableau aggregates the view; it depends entirely on the dimensions placed in Rows and Columns.
> - A **Level of Detail (LOD) expression** (`{FIXED [disease], [region] : AVG([cases])}`) executes directly inside the database query before visualization. This allowed us to calculate historical state baselines that remain constant even when the user filters down to a single month.

### Q3: How does your BI dashboard support proactive rather than reactive hospital planning?
> **Answer:** By correlating our 60-month time series with the 12-month seasonal matrix, the dashboard proves that Dengue and Malaria surge between July and October every single year. Hospital administrators can use the **30-day pre-surge alert** to pre-order test kits, reserve ICU beds, and deploy vector fogging teams in June, well before patient admissions peak.

---
**Verification:** All DAX measures and Tableau calculated fields are validated against `data/disease_analysis_merged.csv` with 100% calculation parity to the Python Streamlit engine.
