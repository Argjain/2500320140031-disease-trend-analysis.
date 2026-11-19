# 09 ArgJain DiseaseTrendAnalysis ERDiagram

DISEASE TREND ANALYSIS

STEP 9 — Entity-Relationship (ER) Diagram Specification


## 1. Mermaid Entity-Relationship (ER) Definition

The formal entity-relationship schema is defined below using declarative Mermaid erDiagram syntax. This specification explicitly documents all five base relational entities, their attribute data types, primary keys (PK), foreign keys (FK), and cardinality constraints:

erDiagram
    disease_master {
        int disease_id PK
        string disease_name
        string disease_category
        string description
        int is_contagious
        int typical_incubation_days
    }
    region_master {
        int region_id PK
        string region_name
        string state_code
        string zone
        int population
        real area_sqkm
        real population_density
    }
    demographic_group {
        int demo_id PK
        string age_group
        string gender
        int age_min
        int age_max
    }
    disease_cases {
        int case_id PK
        int disease_id FK
        int region_id FK
        date report_date
        int report_year
        int report_month
        int cases_reported
        int deaths
        int recovered
        int active_cases
        int hospitalized
        int is_outbreak
        string data_source
        timestamp created_at
    }
    demographic_breakdown {
        int breakdown_id PK
        int case_id FK
        int demo_id FK
        int cases_in_group
        int deaths_in_group
        int recovered_in_group
    }

    disease_master ||--o{ disease_cases : "has"
    region_master ||--o{ disease_cases : "reports"
    disease_cases ||--o{ demographic_breakdown : "broken down by"
    demographic_group ||--o{ demographic_breakdown : "classifies"


## 2. Visual Architecture: Entity-Relationship Diagram

The schematic diagram below illustrates the structural topology of the database, detailing primary key associations, foreign key references, and one-to-many cardinality flows across master dimensions and transaction facts:

Figure 9.1: Entity-Relationship Diagram for Disease Trend Analysis (app.db)


## 3. Plain-English Relationship Semantics

Each relational join pathway enforces specific domain cardinality rules:


### Relationship 1: disease_master to disease_cases (1 : N)

One disease entity in disease_master has zero or many periodic case reports in disease_cases. Conversely, each individual case record reports epidemiological incidence for exactly one disease entity. Orphan case records with unmapped disease identifiers are forbidden by foreign key constraints.


### Relationship 2: region_master to disease_cases (1 : N)

One geographic state in region_master reports zero or many disease case records over time. Conversely, each individual case record belongs to exactly one sovereign state boundary. Case records without valid state associations cannot be inserted.


### Relationship 3: disease_cases to demographic_breakdown (1 : N)

One aggregate case record in disease_cases is partitioned into zero or many demographic sub-group rows in demographic_breakdown. Conversely, each demographic breakdown slice belongs to exactly one aggregate state-month case transaction. Deleting a parent case record cascades to purge its demographic sub-slices.


### Relationship 4: demographic_group to demographic_breakdown (1 : N)

One demographic cohort in demographic_group classifies zero or many clinical breakdown rows in demographic_breakdown. Conversely, each demographic sub-slice is categorized under exactly one standardized age-gender cohort.


### Relationship 5: v_disease_analysis Query View (Denormalized Join)

The materialized analytical view v_disease_analysis executes an inner join across disease_cases, disease_master, and region_master, synthesizing a 35-column denormalized projection enriched with real-time computed KPIs (CFR %, recovery rate %, and incidence per 100,000 residents).


## 4. Business Rules Enforced by Relational Constraints

The database engine actively guarantees data integrity through physical DDL constraints:


## 5. Schema Review: Design Challenges & Remediation

During architectural peer review, five potential design pitfalls were evaluated. The table below itemizes the trade-offs considered and the architectural fixes adopted:

09_ArgJain_DiseaseTrendAnalysis_ERDiagram.docx | v1.0 | ABES Engineering College | November 2026


---
### 📋 Embedded Data Tables


#### Table 1

| Project ID & Title | P-01 / Disease Trend Analysis |
| --- | --- |
| Domain | Healthcare Data Analytics |
| Student Architect | Arg Jain (Roll No. 2500320140031) |
| Academic Program | MCA 2nd Year (Data Analytics Specialization) |
| Institution | ABES Engineering College, Ghaziabad |
| Faculty Mentor | Ms. Kalpana Dwivedi |
| Document Version | v1.0 |
| Schema Model | Extended Star / Snowstorm Relational Model (3NF) |
| Diagram Assets | Mermaid DDL + Embedded High-Resolution PNG Graphic |
| Release Date | November 2026 |



#### Table 2

| # | Enforced Rule | Database Constraint Syntax | Operational Benefit |
| --- | --- | --- | --- |
| 1 | Referential Entity Integrity | disease_cases.disease_id REFERENCES disease_master(disease_id) | Guarantees every case record links to a recognized disease entity. Restricts deletion of active diseases. |
| 2 | Geographic Jurisdiction Integrity | disease_cases.region_id REFERENCES region_master(region_id) | Guarantees all case reporting maps to an established state. Restricts orphaned regional data. |
| 3 | Mortality Upper-Bound Constraint | CHECK (deaths >= 0 AND deaths <= cases_reported) | Physically forbids impossible clinical data where reported fatalities exceed total confirmed infections. |
| 4 | Recovery Upper-Bound Constraint | CHECK (recovered >= 0 AND recovered <= cases_reported) | Physically forbids illogical clinical data where documented recoveries exceed total confirmed infections. |
| 5 | Non-Negative Morbidity Rule | CHECK (cases_reported >= 0 AND active_cases >= 0) | Guarantees case counts cannot be negative under any reporting circumstance. |
| 6 | Unique Disease Naming Constraint | disease_master.disease_name UNIQUE | Eliminates redundant taxonomic duplication (e.g., prevents having two distinct rows for Dengue). |
| 7 | Demographic Cohort Uniqueness | UNIQUE (age_group, gender) | Ensures the 15-cell demographic segmentation matrix (5 age groups x 3 genders) is mathematically distinct. |



#### Table 3

| Item | Design Challenge Identified | Nature of Structural Issue | Severity | Adopted Engineering Remediation |
| --- | --- | --- | --- | --- |
| DP-01 | Derived Column Redundancy in Fact | active_cases is mathematically derived as (cases - deaths - recovered). Storing derived data risks synchronization drift. | Medium | Adopted CHECK constraint: active_cases = cases - deaths - recovered. Retained column in SQLite to avoid recurring arithmetic overhead during high-frequency dashboard queries. |
| DP-02 | Geospatial Density Calculation Overhead | population_density is derived from population / area_sqkm in region_master. | Low | Pre-calculated and stored at master initialization. State land area and decennial census figures are static, making dynamic recalculation unnecessary. |
| DP-03 | M:N Cardinality Resolution | Directly linking disease_cases to demographic_group would create an unwieldy composite relation. | High | Resolved by introducing demographic_breakdown as a dedicated sub-fact / bridge table with independent surrogate key breakdown_id. |
| DP-04 | Redundant Temporal Dimension Columns | Storing report_year and report_month alongside report_date introduces slight storage redundancy. | Low | Deliberate architectural denormalization. Integer year/month columns enable ultra-fast indexed GROUP BY operations without date parsing latency. |
| DP-05 | Absence of Mutability Audit Trail | Base tables lack updated_at timestamp columns to log data corrections. | Low | Created created_at DEFAULT CURRENT_TIMESTAMP. Application dataset is designed as an append-only historical epidemiological ledger. |

