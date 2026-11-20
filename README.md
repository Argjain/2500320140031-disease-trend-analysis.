# 🏥 Disease Trend Analysis Intelligence Cockpit

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=Argjain/2500320140031-disease-trend-analysis.&branch=main&main_file_path=app.py)

**Project ID:** P-01 | **Domain:** Healthcare Data Analytics / Public Health Surveillance  
**Author:** Arg Jain (Roll No. 2500320140031) | MCA 2nd Year Data Analytics, ABES Engineering College  
**Faculty Mentor:** Ms. Kalpana Dwivedi | **Target Release:** December 2026  
**Application Deployment:** [Streamlit Community Cloud](https://share.streamlit.io/deploy?repository=Argjain/2500320140031-disease-trend-analysis.&branch=main&main_file_path=app.py)  

---

## 📌 Project Overview
Disease Trend Analysis is an interactive healthcare analytics web application designed for public health surveillance across India. The platform monitors 5 major infectious diseases (**Dengue, Malaria, Tuberculosis, COVID-19, and Typhoid**) across 10 representative Indian states over a 5-year observation baseline (January 2020 to December 2024, 60 calendar months).

The application answers 10 core Operational Questions (OQ-01 through OQ-10) by providing:
1. **Executive Overview Dashboard**: Multi-dimensional case aggregates, fatalities, clinical recoveries, and state-level case burden rankings.
2. **Longitudinal Trends & Seasonality**: 60-month continuous time series, multi-year overlapping YoY wave comparisons, and 12-month cyclic transmission heatmaps.
3. **Regional Burden & Efficacy**: Cross-state Case Fatality Rate (CFR %) matrices and clinical recovery efficacy benchmarking.
4. **Demographic Drilldown**: Morbidity and mortality disaggregated across 5 age brackets (0–14, 15–29, 30–44, 45–59, 60+) and 3 gender identities.
5. **Advanced EDA & Surveillance**: Urban crowding regression scatter plots (Pearson $r$) and automated multi-disease concurrent outbreak surge alerts.
6. **Data Governance & Export**: Transparent data cleaning accounting ledgers and one-click filtered CSV dataset downloads.

---

## 🏗️ Technical Architecture & Stack
- **Programming Language:** Python 3.12
- **Relational Data Storage:** SQLite 3 (`data/app.db`) with 5 base 3NF tables + 1 denormalized materialized view (`v_disease_analysis`)
- **Data Engineering:** pandas 2.2, NumPy 1.26
- **Mathematical & Statistical Analytics:** SciPy 1.13, statsmodels 0.14
- **Interactive Visualizations:** Plotly Express 5.22
- **User Interface Framework:** Streamlit 1.35 (Multi-page architecture) + Tailwind CSS (injected via iframe components)
- **Quality Assurance & Testing:** pytest 8.2 + Streamlit AppTest framework
- **Cloud Infrastructure:** Streamlit Community Cloud (Public HTTPS deployment)

---

## 🚀 Local Installation & Execution Guide

### 1. Clone the Repository
```bash
git clone https://github.com/Argjain/2500320140031-disease-trend-analysis..git
cd 2500320140031-disease-trend-analysis
```

### 2. Configure Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Generate Synthetic Data Repository
```bash
python src/generate_data.py
```
*Compiles `data/app.db`, generates CSV flat files, and builds `data/disease_trend_analysis_data.xlsx` with deterministic seed 42.*

### 5. Execute Automated Verification Suite
```bash
python -m pytest tests/ -v
```

### 6. Launch Interactive Streamlit Application
```bash
streamlit run app.py
```
*Access the local web dashboard at `http://localhost:8501` in your browser.*

---

## 📁 Repository Structure
```
2500320140031-disease-trend-analysis/
├── app.py                      # Main entry point & shared session state
├── requirements.txt            # Pinned dependencies
├── BUILD_PLAN.md               # Machine-actionable build roadmap
├── README.md                   # Installation & deployment instructions
├── .gitignore                  # Git exclusions
├── .streamlit/
│   └── config.toml             # Theme & UI palette settings
├── src/
│   ├── __init__.py
│   ├── data_loader.py          # Cached SQLite querying & loading
│   ├── cleaning.py             # Deduplication, imputation, outlier bounds
│   ├── analysis.py             # Epidemiological calculation functions
│   ├── ui.py                   # Tailwind CSS iframe component library
│   └── generate_data.py        # Seed-42 deterministic synthetic data generator
├── pages/
│   ├── 01_Overview.py          # KPI dashboard & regional case ranking
│   ├── 02_Trends.py            # 60-month time-series & seasonal heatmaps
│   ├── 03_Regional_Analysis.py # State CFR & recovery rate benchmarking
│   ├── 04_Demographics.py       # Stacked age group & gender charts
│   ├── 05_EDA_Statistics.py    # Density correlation & outbreak anomaly detection
│   └── 06_Data_Quality.py      # Cleaning audit ledger & CSV export
├── data/
│   ├── app.db                  # SQLite database (5 tables + view)
│   ├── disease_cases.csv
│   ├── region_master.csv
│   ├── disease_master.csv
│   ├── demographic_group.csv
│   ├── demographic_breakdown.csv
│   └── disease_trend_analysis_data.xlsx
├── tests/
│   ├── __init__.py
│   ├── test_data.py            # Schema, row counts, FK constraint tests
│   ├── test_analysis.py        # Mathematical assertions on pure formulas
│   └── test_app.py             # Route existence & static file smoke tests
└── docs/                       # Formal step deliverables (01 to 18)
```

---

## 🧪 Automated Testing & Quality Assurance
The test suite enforces 100% mathematical, relational, and configuration integrity:
- **`tests/test_data.py`**: Relational table existence, row counts, zero-orphan foreign keys, and logical bounds (`deaths <= cases`, `recovered <= cases`).
- **`tests/test_analysis.py`**: Known-vector unit assertions on Case Fatality Rate (CFR), Recovery Rate, YoY percentage delta, incidence per 100,000, and Pearson correlation.
- **`tests/test_app.py`**: Verification of route files, source modules, and static configuration manifests.

---

## 📄 Formal Academic Documentation Deliverables
All 18 professional step deliverables conforming to the ABES MCA project template are archived in `docs/`:
- `01_ArgJain_DiseaseTrendAnalysis_ProjectUnderstanding.docx`
- `02_ArgJain_DiseaseTrendAnalysis_HMWStatements.docx`
- `03_ArgJain_DiseaseTrendAnalysis_NeedsAnalysis.docx`
- `04_ArgJain_DiseaseTrendAnalysis_RTM.xlsx` *(Complete Bidirectional Traceability)*
- `05_ArgJain_DiseaseTrendAnalysis_BRD.docx`
- `07_ArgJain_DiseaseTrendAnalysis_TRD.docx`
- `08_ArgJain_DiseaseTrendAnalysis_DBDesign.xlsx`
- `09_ArgJain_DiseaseTrendAnalysis_ERDiagram.docx` *(with embedded High-Res ER Diagram PNG)*
- `11_ArgJain_DiseaseTrendAnalysis_UserStories.docx`
- `12_ArgJain_DiseaseTrendAnalysis_UIFramework.docx`
- `13_ArgJain_DiseaseTrendAnalysis_TestCases.docx`
- `14_ArgJain_DiseaseTrendAnalysis_BuildPlan.docx`
- `16_ArgJain_DiseaseTrendAnalysis_DeploymentGuide.docx`
- `17_ArgJain_DiseaseTrendAnalysis_ProjectDocument.docx`
- `18_ArgJain_DiseaseTrendAnalysis_Presentation.docx`
