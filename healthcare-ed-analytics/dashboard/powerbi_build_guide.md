# Power BI Build Guide — ED Performance Dashboard

This guide reproduces the dashboard in Power BI Desktop from the same three
CSVs, so you can publish an interactive `.pbix` and screenshot **your own**
build. The matplotlib PNG in this folder is the reference layout to match.

> Do this once and the screenshot is genuinely your work — which is the point.

## 1. Load the data

1. **Home → Get data → Text/CSV**, load all three:
   `data/patients.csv`, `data/ed_presentations.csv`, `data/admissions.csv`.
2. In **Transform data (Power Query)** confirm types:
   - `arrival_datetime`, `departure_datetime`, `admit_datetime`,
     `discharge_datetime` → *Date/Time*
   - flags (`met_4hr_target`, `left_without_being_seen`, `admitted`,
     `readmitted_28d`) → *Whole number*
   - `ed_los_minutes`, `los_days` → *Decimal number*

## 2. Model relationships (Model view)

- `patients[patient_id]` **1 → \*** `ed_presentations[patient_id]`
- `patients[patient_id]` **1 → \*** `admissions[patient_id]`
- `ed_presentations[presentation_id]` **1 → \*** `admissions[presentation_id]`

Create a **Date table** and mark it as a date table:

```DAX
Date = CALENDAR(DATE(2024,7,1), DATE(2025,6,30))
```

Relate `Date[Date]` to `ed_presentations[arrival_datetime]` (date portion).

## 3. Core measures

Put these in a dedicated **_Measures** table. Full list with comments is in
[`dax_measures.md`](dax_measures.md). The four KPI-card measures:

```DAX
Presentations = COUNTROWS ( ed_presentations )

Pct Within 4hr =
DIVIDE ( SUM ( ed_presentations[met_4hr_target] ), [Presentations] )

LWBS Rate =
DIVIDE ( SUM ( ed_presentations[left_without_being_seen] ), [Presentations] )

Readmission Rate 28d =
DIVIDE ( SUM ( admissions[readmitted_28d] ), COUNTROWS ( admissions ) )
```

## 4. Build the visuals (match the reference layout)

| Reference panel | Power BI visual | Fields |
|:----------------|:----------------|:-------|
| 4 KPI cards | **Card** ×4 | the four measures above; format `Pct/LWBS/Readmission` as % |
| Monthly demand vs 4hr | **Line and clustered column** | Axis = `Date[Month]`; Column = `[Presentations]`; Line = `[Pct Within 4hr]` |
| % within 4hr by triage | **Clustered bar** | Axis = `triage_category`; Value = `[Pct Within 4hr]`; conditional colour < 0.81 = red |
| Arrivals by hour | **Area chart** | Axis = `Hour of Day`* ; Legend = `arrival_mode`; Value = `[Presentations]` |
| Readmission by diagnosis | **Clustered bar** | Axis = `admissions[diagnosis_group]`; Value = `[Readmission Rate 28d]` |
| Avg ED LOS by triage | **Line** | Axis = `triage_category`; Value = `[Avg ED LOS]`; add constant line at 240 |
| Presentations by catchment | **Clustered bar** | Axis = `patients[region]`; Value = `[Presentations]` |

\* Add an `Hour of Day` column: `Hour of Day = HOUR ( ed_presentations[arrival_datetime] )`

## 5. Polish

- **Slicers:** `Date[Month]`, `triage_category`, `patients[region]`.
- Conditional formatting on the triage bar: **Format → Data colors → fx →**
  rule `[Pct Within 4hr] < 0.81` → red, else green.
- Add a target line at **81%** (NEAT) and **240 min** (4hr) via the Analytics pane.
- Title the page "Emergency Department — Performance & Patient Flow" and add a
  footer noting the data is synthetic.

## 6. Publish & screenshot

**File → Export → Export to PDF**, or screenshot the canvas, and save it into
this folder as `ed_dashboard_powerbi.png`. Then reference it from the project
README next to (or instead of) the matplotlib version.
