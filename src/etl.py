import argparse
from pathlib import Path
import sqlite3
import pandas as pd
from utils import ensure_dir, to_datetime

def load_to_sqlite(df: pd.DataFrame, table: str, conn: sqlite3.Connection):
    df.to_sql(table, conn, if_exists="append", index=False)

def main(args):
    input_claims = Path(args.input)
    input_benes = Path(args.beneficiaries)
    db_path = Path(args.db)
    out_dir = Path("data/clean")
    ensure_dir(out_dir)

    # Connect DB
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Create schema
    schema_sql = Path("sql/schema.sql").read_text(encoding="utf-8")
    cur.executescript(schema_sql)
    conn.commit()

    # Load beneficiaries
    benes = pd.read_csv(input_benes, dtype={'zip3': 'string', 'bene_id': 'string'})
    benes['dual_eligible'] = benes['dual_eligible'].astype(int)
    benes['chronic_count'] = benes['chronic_count'].astype(int)
    load_to_sqlite(benes, "beneficiaries", conn)

    # Load claims
    claims = pd.read_csv(input_claims, dtype={'bene_id':'string','claim_id':'string','drg_code':'string'})
    claims = to_datetime(claims, ["admission_date","discharge_date"])
    load_to_sqlite(claims, "claims", conn)

    # Rebuild inpatient_readmissions derived table
    cur.execute("DROP TABLE IF EXISTS inpatient_readmissions;")
    conn.commit()
    cur.executescript(Path("sql/schema.sql").read_text(encoding="utf-8"))
    conn.commit()

    # Export flattened dataset for BI
    q = (
        "SELECT c.*, b.sex, b.state, b.dual_eligible, b.chronic_count, "
        "ir.readmitted_30d "
        "FROM claims c "
        "LEFT JOIN beneficiaries b ON b.bene_id = c.bene_id "
        "LEFT JOIN inpatient_readmissions ir ON ir.index_claim_id = c.claim_id"
    )
    df = pd.read_sql_query(q, conn, parse_dates=["admission_date","discharge_date"])
    out_csv = out_dir / "claims_for_bi.csv"
    df.to_csv(out_csv, index=False)
    print(f"Exported: {out_csv} ({len(df)} rows)")

    conn.close()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="Path to claims CSV")
    p.add_argument("--beneficiaries", required=True, help="Path to beneficiaries CSV")
    p.add_argument("--db", default="data/claims.db", help="SQLite DB path")
    main(p.parse_args())
