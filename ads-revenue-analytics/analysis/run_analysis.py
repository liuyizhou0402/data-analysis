"""
Build the DuckDB database, run every analysis query, print the results, and
export each one as a Tableau-ready CSV.

    python analysis/run_analysis.py

Outputs:
    ads.duckdb                     the loaded database (gitignored)
    dashboard/extracts/*.csv       one file per query, for Tableau to connect to
"""

from __future__ import annotations

import re
from pathlib import Path

import duckdb
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SQL_DIR = ROOT / "sql"
EXTRACT_DIR = ROOT / "dashboard" / "extracts"
DB_PATH = ROOT / "ads.duckdb"

# Query block -> output filename. Order matches sql/02_analysis.sql.
QUERY_NAMES = [
    "q01_executive_summary",
    "q02_revenue_trend",
    "q03_revenue_diagnosis",
    "q04_cohort_retention",
    "q05_tier_performance",
    "q06_advertiser_deciles",
    "q07_rep_scorecard",
    "q08_new_hire_ramp",
    "q09_book_size_retention",
    "q10_funnel_by_objective",
    "q11_growth_opportunities",
    "q12_churn_watchlist",
]


def split_statements(sql_text: str) -> list[str]:
    """Split a script into executable statements, ignoring semicolons in comments.

    A naive split on ";" breaks this file: the comment blocks contain
    semicolons in prose. Comment lines are stripped before splitting, and the
    original text is not modified for execution.
    """
    lines = []
    for line in sql_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("--"):
            continue
        lines.append(line)
    cleaned = "\n".join(lines)
    return [s.strip() for s in cleaned.split(";") if s.strip()]


def build_database(con: duckdb.DuckDBPyConnection) -> None:
    print("Building schema and loading CSVs ...")
    schema_sql = (SQL_DIR / "01_schema.sql").read_text()
    for stmt in split_statements(schema_sql):
        con.execute(stmt)

    counts = con.execute("""
        SELECT 'sales_reps' AS t, COUNT(*) AS n FROM dim_sales_rep
        UNION ALL SELECT 'advertisers', COUNT(*) FROM dim_advertiser
        UNION ALL SELECT 'campaigns',   COUNT(*) FROM dim_campaign
        UNION ALL SELECT 'daily_facts', COUNT(*) FROM fact_daily_performance
    """).fetchdf()
    for _, row in counts.iterrows():
        print(f"  {row['t']:<14} {row['n']:>9,}")


def run_analyses(con: duckdb.DuckDBPyConnection) -> dict[str, pd.DataFrame]:
    analysis_sql = (SQL_DIR / "02_analysis.sql").read_text()
    statements = split_statements(analysis_sql)

    if len(statements) != len(QUERY_NAMES):
        raise RuntimeError(
            f"Found {len(statements)} SQL statements but {len(QUERY_NAMES)} "
            f"names are configured. If a query was added to 02_analysis.sql, "
            f"add its name to QUERY_NAMES so the extract filenames stay aligned."
        )

    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
    results: dict[str, pd.DataFrame] = {}

    for name, stmt in zip(QUERY_NAMES, statements):
        df = con.execute(stmt).fetchdf()
        results[name] = df
        df.to_csv(EXTRACT_DIR / f"{name}.csv", index=False)

        title = name.split("_", 1)[1].replace("_", " ").title()
        print(f"\n{'=' * 78}\n{name[:3].upper()}  {title}   ({len(df)} rows)\n{'=' * 78}")
        with pd.option_context("display.width", 200,
                               "display.max_columns", 40,
                               "display.max_rows", 14):
            print(df.to_string(index=False))

    return results


def main() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()

    # Queries reference data/*.csv by relative path, so run from the project root.
    import os
    os.chdir(ROOT)

    con = duckdb.connect(str(DB_PATH))
    build_database(con)
    run_analyses(con)
    con.close()

    print(f"\n{'=' * 78}")
    print(f"Extracts written to {EXTRACT_DIR.relative_to(ROOT)}/ "
          f"({len(QUERY_NAMES)} files) — these are what Tableau connects to.")


if __name__ == "__main__":
    main()
