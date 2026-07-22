# DAX Measures — ED Performance Dashboard

Copy these into a `_Measures` table in Power BI Desktop. Grouped by theme.

## Volume & demand

```DAX
Presentations = COUNTROWS ( ed_presentations )

Admissions = COUNTROWS ( admissions )

Admission Rate =
DIVIDE ( SUM ( ed_presentations[admitted] ), [Presentations] )

Presentations MoM % =
VAR Curr = [Presentations]
VAR Prev = CALCULATE ( [Presentations], DATEADD ( 'Date'[Date], -1, MONTH ) )
RETURN DIVIDE ( Curr - Prev, Prev )
```

## Access & timeliness (NEAT / 4-hour target)

```DAX
Pct Within 4hr =
DIVIDE ( SUM ( ed_presentations[met_4hr_target] ), [Presentations] )

Avg ED LOS =
AVERAGE ( ed_presentations[ed_los_minutes] )

-- internal sub-target for the urgent cohort only
Pct Within 4hr (T1-T2) =
CALCULATE ( [Pct Within 4hr], ed_presentations[triage_category] <= 2 )

Breaches 4hr =
CALCULATE ( [Presentations], ed_presentations[met_4hr_target] = 0 )
```

## Quality & safety

```DAX
LWBS Rate =
DIVIDE ( SUM ( ed_presentations[left_without_being_seen] ), [Presentations] )

Readmission Rate 28d =
DIVIDE ( SUM ( admissions[readmitted_28d] ), [Admissions] )

Avg Inpatient LOS (days) =
AVERAGE ( admissions[los_days] )
```

## Cohort / utilisation

```DAX
-- distinct patients presenting in the current filter context
Distinct Patients =
DISTINCTCOUNT ( ed_presentations[patient_id] )

-- average visits per patient
Visits per Patient =
DIVIDE ( [Presentations], [Distinct Patients] )
```

## Conditional-formatting helper

Use on the triage bar chart data colours (rule: value is red when below target):

```DAX
Below NEAT Target =
IF ( [Pct Within 4hr] < 0.81, 1, 0 )
```
