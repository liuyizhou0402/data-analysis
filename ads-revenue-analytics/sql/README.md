# SQL

| File | Purpose |
|---|---|
| `01_schema.sql` | Star schema, foreign keys, CSV load, denormalised `v_performance` view |
| `02_analysis.sql` | 12 business questions |

## Running

```bash
python analysis/run_analysis.py     # builds the DB and runs everything
```

or directly:

```bash
duckdb ads.duckdb < sql/01_schema.sql
duckdb ads.duckdb < sql/02_analysis.sql
```

Run from the project root — the schema loads CSVs by relative path.

## Model

```
dim_sales_rep ──┐
                ├── dim_advertiser ──┐
                ┘                    ├── fact_daily_performance
                     dim_campaign ───┘
```

Fact grain: one row per campaign per delivering day.

`v_performance` joins all four and is the entry point for every analysis query,
so the joins and month truncation are written once rather than repeated twelve
times.

## Portability

Written for DuckDB. Three things need changing for Postgres:

| DuckDB | Postgres |
|---|---|
| `read_csv_auto('file.csv')` | `COPY tbl FROM 'file.csv' WITH (FORMAT csv, HEADER true)` |
| `QUALIFY` | wrap in a subquery, filter in outer `WHERE` |
| `MEDIAN(x) OVER (...)` | `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY x)` |

`DATE_DIFF`, `DATE_TRUNC`, `NTILE`, `LAG`, `RANK` and the window frame syntax
are all standard.
