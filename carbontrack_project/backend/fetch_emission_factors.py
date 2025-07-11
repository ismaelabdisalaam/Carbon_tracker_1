import requests
import sqlite3
import csv

# URL for emission factors CSV (BEIS UK Government dataset)
CSV_URL = "https://raw.githubusercontent.com/climatiq/climatiq/main/climatiq/cli/data/emissions_factors.csv"
DB_FILE = "factors.db"

def fetch_csv(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text.splitlines()

def init_db(conn):
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS emission_factors (
        category TEXT PRIMARY KEY,
        sub_category TEXT,
        unit TEXT,
        factor REAL
    )
    """)
    conn.commit()

def store_factors(conn, csv_lines):
    reader = csv.DictReader(csv_lines)
    cur = conn.cursor()
    for row in reader:
        category = row.get('category')
        sub_category = row.get('sub_category')
        unit = row.get('unit')
        try:
            factor = float(row.get('co2e'))
        except (TypeError, ValueError):
            continue
        cur.execute("""
            INSERT OR REPLACE INTO emission_factors(category, sub_category, unit, factor)
            VALUES (?, ?, ?, ?)
        """, (category, sub_category, unit, factor))
    conn.commit()

def main():
    print("Fetching emission factors CSV...")
    lines = fetch_csv(CSV_URL)
    conn = sqlite3.connect(DB_FILE)
    init_db(conn)
    print("Storing factors into database...")
    store_factors(conn, lines)
    conn.close()
    print(f"Stored factors into {DB_FILE}")

if __name__ == "__main__":
    main()
