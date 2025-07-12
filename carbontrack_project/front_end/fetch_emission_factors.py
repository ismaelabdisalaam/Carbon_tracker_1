import sqlite3

DB_FILE = "carbontrack.db"

# Hard-coded emission factors for initial prototype
FACTORS = [
    {"category": "car",       "sub_category": "travel",      "unit": "km",  "factor": 0.192},
    {"category": "airplane",  "sub_category": "travel",      "unit": "km",  "factor": 0.255},
    {"category": "cooking",   "sub_category": "home energy", "unit": "kWh", "factor": 0.233},
    {"category": "heating",   "sub_category": "home energy", "unit": "kWh", "factor": 0.233},
    {"category": "dairy",     "sub_category": "food",        "unit": "kg",  "factor": 12.0 },
    {"category": "meat",      "sub_category": "food",        "unit": "kg",  "factor": 27.0 },
]

def initialize_factors_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS emission_factors (
            category     TEXT PRIMARY KEY,
            sub_category TEXT,
            unit         TEXT,
            factor       REAL
        )
    """)
    conn.commit()

    for f in FACTORS:
        c.execute("""
            INSERT OR REPLACE INTO emission_factors(category, sub_category, unit, factor)
            VALUES (?, ?, ?, ?)
        """, (f["category"], f["sub_category"], f["unit"], f["factor"]))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_factors_db()
    print(f"Emission factors initialized in {DB_FILE}")
