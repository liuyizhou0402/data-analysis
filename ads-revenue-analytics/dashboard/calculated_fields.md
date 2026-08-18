# Tableau calculated fields

Every calculation the workbook needs, with the reasoning behind it. Most of the
metric logic already lives in SQL (`sql/02_analysis.sql`) — these are the
presentation-layer calculations that have to be in Tableau because they depend
on what the user has selected or filtered.

---

## Formatting and colour

### `Change Direction`
Used to colour the revenue-diagnosis bars.

```
IF [Change Usd] < 0 THEN "Decline" ELSE "Growth" END
```

### `Revenue (formatted)`
Tableau's default number formatting is unreadable at this scale.

```
IF ABS([Revenue Usd]) >= 1000000
THEN STR(ROUND([Revenue Usd] / 1000000, 1)) + "M"
ELSE STR(ROUND([Revenue Usd] / 1000, 0)) + "K"
END
```

### `MoM Label`
Signed percentage with an arrow, for KPI tiles.

```
IF ISNULL([Revenue Mom Pct]) THEN "—"
ELSEIF [Revenue Mom Pct] > 0 THEN "▲ " + STR(ROUND([Revenue Mom Pct], 1)) + "%"
ELSE "▼ " + STR(ROUND(ABS([Revenue Mom Pct]), 1)) + "%"
END
```

The `ISNULL` branch matters: the first month of any series has no prior month,
and without it Tableau renders the tile as "▼ %" with a blank number.

---

## Table calculations

### `Revenue MoM %` (if computing in Tableau rather than reading the SQL column)

```
(SUM([Revenue Usd]) - LOOKUP(SUM([Revenue Usd]), -1))
/ LOOKUP(SUM([Revenue Usd]), -1)
```

Set **Compute Using → Month**. If this is left on the default (Table Across)
it will silently compute across whatever dimension happens to be on Columns,
which usually produces a plausible-looking but wrong number — the most common
way a Tableau table calculation goes wrong without erroring.

### `Revenue 3-Month Moving Average`

```
WINDOW_AVG(SUM([Revenue Usd]), -2, 0)
```

The `-2, 0` window is trailing (this month and the two before). `WINDOW_AVG`
with no offsets averages the *entire* partition, which is a different and
usually unintended statistic.

### `Running % of Revenue` (Pareto curve)

```
RUNNING_SUM(SUM([Revenue Usd])) / TOTAL(SUM([Revenue Usd]))
```

Sort the decile axis descending first, or the curve is meaningless.

---

## Level-of-detail expressions

### `Revenue per Active Advertiser`
An LOD is needed because the advertiser count must not be affected by whichever
dimensions are on the view.

```
SUM([Revenue Usd]) / ATTR([Active Advertisers])
```

For the raw-fact version of this dashboard (connecting Tableau directly to
`data/daily_performance.csv` rather than the extracts) the equivalent is:

```
{ FIXED [Month] : COUNTD([Advertiser Id]) }
```

### `Top 20% Advertiser Flag`

```
IF [Cumulative Pct Of Revenue] <= 80 THEN "Top accounts (80% of revenue)"
ELSE "Long tail"
END
```

---

## Parameters

### `Target ROAS`
A parameter (Float, default `3.0`, range 1.0–6.0) lets a reviewer move the
threshold and watch the opportunity matrix re-classify. Pair it with:

```
IF [Roas] >= [Target ROAS] THEN "Above target" ELSE "Below target" END
```

Interactivity like this is worth adding before publishing — it demonstrates
parameter handling, which a static chart does not.

### `Decline Threshold %`
Integer parameter, default `-15`, range −50 to 0. Drives the diagnosis flag:

```
IF [Change Pct] <= [Decline Threshold %] THEN "Investigate"
ELSEIF [Change Pct] < 0 THEN "Soft"
ELSE "Growing"
END
```

---

## A note on where calculations live

The metric definitions — CTR, CVR, CPA, ROAS, retention, contribution to
change — are all computed in SQL, not here. That is deliberate:

- **One definition, one place.** If ROAS is defined in six Tableau sheets it
  will eventually be defined six slightly different ways.
- **Testable.** SQL output can be diffed and checked; a calculation buried in a
  workbook cannot.
- **Portable.** The same SQL runs if the dashboard is later rebuilt in Power BI
  or Looker.

Tableau's job here is to render and filter, not to define what a metric means.
