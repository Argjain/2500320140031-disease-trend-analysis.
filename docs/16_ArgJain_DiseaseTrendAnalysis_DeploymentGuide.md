# 16 ArgJain DiseaseTrendAnalysis DeploymentGuide

DISEASE TREND ANALYSIS

STEP 16 — Streamlit Cloud Deployment & DevOps Guide


## 1. Pre-Deployment Verification Audit Checklist

Before initiating cloud deployment, the engineering codebase must satisfy all 10 pre-flight criteria to guarantee an error-free build on Streamlit Community Cloud container environments:


## 2. GitHub Version Control & Repository Staging

Streamlit Community Cloud continuously deploys from an active GitHub repository. Execute the following commands in PowerShell from the project root directory:

# 1. Initialize local git repository
git init

# 2. Stage all project files, code, tests, docs, and database
git add .

# 3. Create initial formal commit
git commit -m "Release v1.0: Complete Disease Trend Analysis Platform - Arg Jain P-01"

# 4. Set default branch to main
git branch -M main

# 5. Add remote GitHub origin (replace with your personal GitHub username)
git remote add origin https://github.com/Argjain/2500320140031-disease-trend-analysis..git

# 6. Push code to remote repository
git push -u origin main


## 3. Streamlit Community Cloud Provisioning Guide

Step-by-step procedure to deploy the application on Streamlit Community Cloud:

* Step 1: Navigate to https://share.streamlit.io in your web browser and click "Sign in with GitHub".
* Step 2: Grant read-access permissions to your GitHub account repository list.
* Step 3: Click the prominent "Create app" button in the upper-right corner of the dashboard.
* Step 4: Select "I already have an app" and populate the deployment form fields:
   • Repository: argjain/2500320140031-disease-trend-analysis
   • Branch: main
   • Main file path: app.py
   • App URL (Custom Slug): 2500320140031-dta (resulting in https://2500320140031-dta.streamlit.app)
* Step 5: Click "Deploy now!". Streamlit will provision an isolated Linux container, install all packages from requirements.txt, and launch the application.
* Step 6: Monitor the real-time deployment log terminal (bottom right). Look for the success banner: "You can now view your Streamlit app in your browser".
* Step 7: Copy the public HTTPS URL and verify full functionality across all 6 pages.

## 4. Cloud Deployment Failure Diagnostics & Exact Fixes

Matrix of potential cloud container failures, root causes, and definitive fixes:


## 5. Post-Deployment Verification & Viva Voce Readiness

Upon live deployment, execute this post-flight verification protocol:

* Initial Load Time Check: Ensure the home page renders in < 5.0 seconds on a standard 4G/broadband connection.
* Sidebar Filter Reactivity: Select "COVID-19", verify KPI cards update in < 1.5 seconds without container restart.
* Multi-Page Navigation: Click through all 6 pages (01_Overview to 06_Data_Quality) verifying no Python exceptions.
* CSV Download Verification: Click "Download Certified Dataset" on UI-06; open downloaded file in Excel to confirm integrity.
* URL Submission: Embed the public URL (https://2500320140031-dta.streamlit.app) into the ABES Project Document cover sheet and final presentation slide deck.
16_ArgJain_DiseaseTrendAnalysis_DeploymentGuide.docx | v1.0 | ABES Engineering College | November 2026


---
### 📋 Embedded Data Tables


#### Table 1

| Project ID & Title | P-01 / Disease Trend Analysis |
| --- | --- |
| Domain | Healthcare Data Analytics |
| Release Engineer / Student | Arg Jain (Roll No. 2500320140031) |
| Academic Program | MCA 2nd Year (Data Analytics Specialization) |
| Institution | ABES Engineering College, Ghaziabad |
| Faculty Mentor | Ms. Kalpana Dwivedi |
| Document Version | v1.0 |
| Deployment Platform | Streamlit Community Cloud (Public HTTPS) |
| Repository Host | GitHub (git version 2.x) |
| Target Public URL | https://2500320140031-dta.streamlit.app |
| Release Date | November 2026 |



#### Table 2

| Check ID | Audit Item & Objective | Expected Physical State | Pre-Flight Verification Status |
| --- | --- | --- | --- |
| CHK-01 | Application Entry Point Location | app.py located strictly at the repository root directory | VERIFIED (PASS) |
| CHK-02 | Pinned Requirements Manifest | requirements.txt contains exact pinned versions (==) without conflicting ranges | VERIFIED (PASS) |
| CHK-03 | Database Repository Asset | data/app.db compiled, committed, and tracked in git repository | VERIFIED (PASS) |
| CHK-04 | Relative Path Resolution | All file lookups use Path(__file__).resolve().parent relative paths | VERIFIED (PASS) |
| CHK-05 | Credential & Secret Hygiene | Zero API keys, passwords, or cloud tokens present in code or commit history | VERIFIED (PASS) |
| CHK-06 | Git Exclusion Rules | .gitignore excludes .venv/, __pycache__/, *.pyc, and OS thumbs | VERIFIED (PASS) |
| CHK-07 | Multi-Page Sub-Directory | pages/ contains all 6 individual route scripts (01_Overview..06_Data_Quality) | VERIFIED (PASS) |
| CHK-08 | Automated Test Suite Cleanliness | All 17 technical unit and schema tests execute with zero failures | VERIFIED (PASS) |
| CHK-09 | Local Execution Smoke Test | `streamlit run app.py` launches and renders in browser without exceptions | VERIFIED (PASS) |
| CHK-10 | GitHub Master Synchronization | Local commits pushed to remote GitHub repository `main` branch | VERIFIED (PASS) |



#### Table 3

| Error Signature | Underlying Root Cause | Technical Diagnostic | Exact Prescriptive Resolution |
| --- | --- | --- | --- |
| ModuleNotFoundError: No module named 'src' | Python module resolution path in Streamlit container | Linux container executes from root but does not automatically add root to sys.path | Add `sys.path.insert(0, str(Path(__file__).resolve().parent))` at the top of app.py and page scripts. |
| FileNotFoundError: data/app.db | Fragile relative working directory path | Code executes from `pages/` directory instead of project root | Always resolve file paths using `Path(__file__).resolve().parent.parent / "data" / "app.db"`. |
| Build Failure: No matching distribution | Python version mismatch or unpinned dependency | Platform defaults to Python 3.12 while package requires 3.10 | Specify exact version pins in `requirements.txt` and add `.python-version` specifying `3.12`. |
| MemoryError / Container Crash | Dataset exceeds 1 GB RAM free-tier allocation | Loading unindexed raw files into memory repeatedly without caching | Decorate loader with `@st.cache_data(ttl=3600)` and pre-aggregate queries in SQLite view. |
| App Goes to Sleep (Zzz...) | Streamlit Cloud free-tier inactivity policy | App hibernates after 7 consecutive days of zero user visits | Wake app 1 hour prior to formal academic viva evaluation by visiting the URL once. |

