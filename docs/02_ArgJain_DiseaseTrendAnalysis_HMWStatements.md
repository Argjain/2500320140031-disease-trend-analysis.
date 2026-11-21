# 02 ArgJain DiseaseTrendAnalysis HMWStatements

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DISEASE TREND ANALYSIS

STEP 2 – How Might We (HMW) Statements

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Section 1 – Stakeholder Pain Points

The following pain points were elicited through stakeholder interviews and domain analysis. Each stakeholder's operational frustrations directly drive the HMW framing in Section 2.

Section 2 – How Might We (HMW) Statements

Ten HMW statements were synthesised from stakeholder pain points and linked to the ten Organisational Questions (OQ-01 … OQ-10). The top five are marked PRIORITY and form the core scope of the system.

Legend:  Rows shaded in yellow (#FEF9E7) = PRIORITY HMW (core system scope).  Rows in blue-tint (#EBF5FB) or white = secondary HMW (stretch goals).

Section 3 – Priority HMW Justifications

The five PRIORITY HMWs were selected because they address the highest-severity pain points of the highest-priority stakeholders (SH-01 H, SH-02 H, SH-03 H) and together cover the broadest slice of the OQs.

Section 4 – OQ Coverage Check

Every Organisational Question (OQ-01 … OQ-10) must be traceable to at least one HMW statement. The table below verifies full coverage.

✔ Coverage Confirmed: All 10 Organisational Questions (OQ-01 … OQ-10) are addressed by at least one HMW statement. No gap identified.


---
### 📋 Embedded Data Tables


#### Table 1

| Project ID | P100 |
| --- | --- |
| Student | Arg Jain |
| Roll Number | 2500320140031 |
| Course | MCA 2nd Year – Data Analytics |
| Institute | ABES Engineering College |
| Mentor | Mr. Dinesh |
| Date | November 2026 |



#### Table 2

| SH ID | Stakeholder | Pain Point 1 | Pain Point 2 | Pain Point 3 |
| --- | --- | --- | --- | --- |
| SH-01 | Public Health Officer | No single dashboard shows real-time district/state disease spikes | Outbreak alerts arrive days late; pattern recognition is manual | Co-occurring outbreaks are invisible until strain on clinics is severe |
| SH-02 | Hospital Administrator | Bed and staff planning is reactive – surge data arrives post-crisis | Recovery vs fatality benchmarks are not visible across peer hospitals | Seasonal admission spikes cause resource shortages every year |
| SH-03 | Policy Maker / Ministry | CFR data is scattered across state PDFs; cross-regional comparison impossible | No year-over-year summary to redirect budgets to rising-disease states | Funding decisions rely on anecdotal reports rather than trend evidence |
| SH-04 | Epidemiologist / Researcher | No drill-down by age group or gender to pinpoint vulnerable demographics | Population-density vs incidence correlation requires manual GIS work | Seasonal pattern analysis across 5 diseases needs custom scripting each cycle |



#### Table 3

| HMW ID | How Might We…? | Stakeholder(s) | Pain Point Addressed | Linked OQ(s) | Priority |
| --- | --- | --- | --- | --- | --- |
| HMW-01 | How might we help public health officers instantly spot which disease is spiking in a specific region this month vs last year? | SH-01 | No unified real-time trend view | OQ-01, OQ-09 | ✔ PRIORITY |
| HMW-02 | How might we show hospital administrators which states will face a patient surge next season so they can pre-allocate beds? | SH-02 | Reactive not proactive planning | OQ-02, OQ-03 | ✔ PRIORITY |
| HMW-03 | How might we help policy makers compare case fatality rates across regions in a single glance to justify targeted budget allocations? | SH-03 | Data scattered across reports | OQ-05, OQ-02 | ✔ PRIORITY |
| HMW-04 | How might we enable epidemiologists to filter disease data by age group and gender to identify the most vulnerable demographic segments? | SH-04 | No demographic drill-down | OQ-04 | ✔ PRIORITY |
| HMW-05 | How might we surface co-occurring disease outbreaks in the same region-time window to alert response teams before crises escalate? | SH-01, SH-04 | Outbreaks treated in isolation | OQ-08 | ✔ PRIORITY |
| HMW-06 | How might we visualise seasonal disease peaks across all diseases on one chart so analysts can prepare resources months in advance? | SH-01, SH-04 | Seasonal patterns buried | OQ-10, OQ-03 | — |
| HMW-07 | How might we display recovery rates alongside fatality rates per region so administrators can benchmark their hospitals against peer states? | SH-02 | Recovery data not compared | OQ-07, OQ-05 | — |
| HMW-08 | How might we show the correlation between population density and disease incidence on a scatter chart so researchers can prioritise dense urban zones? | SH-04 | No spatial-incidence link | OQ-06 | — |
| HMW-09 | How might we provide a year-over-year trend table that highlights which diseases are growing vs declining so ministers can redirect funds quickly? | SH-03 | No YoY summary | OQ-09, OQ-01 | — |
| HMW-10 | How might we give analysts a clean downloadable dataset with a data quality summary so they can demonstrate rigorous EDA methodology? | SH-05 | No exportable clean data view | OQ-01..OQ-10 | — |



#### Table 4

| HMW ID | Priority Justification |
| --- | --- |
| HMW-01 | Real-time regional spike detection is the #1 public-health-officer need; without it, outbreak response is delayed and lives are at risk (OQ-01, OQ-09). |
| HMW-02 | Proactive seasonal surge prediction directly prevents hospital resource crises; highest operational impact for SH-02 administrators (OQ-02, OQ-03). |
| HMW-03 | CFR comparison across regions in one view empowers evidence-based policy funding decisions—currently impossible without this dashboard (OQ-05, OQ-02). |
| HMW-04 | Demographic filtering (age/gender) is fundamental to epidemiological investigation; missing this makes the system non-viable for SH-04 researchers (OQ-04). |
| HMW-05 | Concurrent outbreak detection prevents compounding crises; no existing tool provides this multi-disease, single-region-window view (OQ-08). |



#### Table 5

| OQ ID | Organisational Question (summary) | Covered by HMW(s) |
| --- | --- | --- |
| OQ-01 | Which diseases have shown highest case increase over 5 years? | HMW-01, HMW-09, HMW-10 |
| OQ-02 | Which regions are most affected by each disease? | HMW-02, HMW-03 |
| OQ-03 | What is the monthly/seasonal trend of disease outbreaks? | HMW-02, HMW-06 |
| OQ-04 | Which age group/gender are most vulnerable? | HMW-04 |
| OQ-05 | What is the case fatality rate per disease per region? | HMW-03, HMW-07 |
| OQ-06 | How does incidence correlate with population density? | HMW-08 |
| OQ-07 | Which diseases have highest recovery rates, and where? | HMW-07 |
| OQ-08 | Are there concurrent outbreaks in any region? | HMW-05 |
| OQ-09 | What is year-over-year change in cases per disease? | HMW-01, HMW-09 |
| OQ-10 | Which months see peak disease reporting by disease type? | HMW-06 |

