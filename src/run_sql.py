import argparse, sqlite3
from pathlib import Path

def main(args):
    conn = sqlite3.connect(args.db)
    sql = Path(args.file).read_text(encoding="utf-8")
    cur = conn.cursor()
    for stmt in [s.strip() for s in sql.split(';') if s.strip()]:
        print("\n--", stmt.replace("\n"," ")[:120], "...")
        try:
            cur.execute(stmt)
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description] if cur.description else []
            if cols:
                print("\t".join(cols))
                for r in rows[:50]:
                    print("\t".join([str(x) for x in r]))
                if len(rows) > 50:
                    print(f"... ({len(rows)} rows, showing first 50)")
        except Exception as e:
            print("Error:", e)
    conn.close()

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--db", default="data/claims.db")
    p.add_argument("--file", default="sql/queries.sql")
    main(p.parse_args())
