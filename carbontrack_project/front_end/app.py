import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

import fetch_emission_factors  # backend initializer

DB_FILE = "carbontrack.db"

# Initialize emission factors and logs table
fetch_emission_factors.initialize_factors_db()
def init_logs_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            timestamp TEXT,
            name      TEXT,
            age       INTEGER,
            country   TEXT,
            category  TEXT,
            amount    REAL,
            emissions REAL
        )
    """)
    conn.commit()
    conn.close()
init_logs_db()

# Load factors once
@st.cache_data
def load_factors():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql("SELECT category, unit, factor FROM emission_factors", conn)
    conn.close()
    return df.set_index("category")
factors_df = load_factors()

# Helper to log a user entry
def log_entry(name, age, country, category, amount, emissions):
    conn = sqlite3.connect(DB_FILE)
    conn.execute("""
        INSERT INTO logs(timestamp, name, age, country, category, amount, emissions)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.utcnow().isoformat(),
        name, age, country, category, amount, emissions
    ))
    conn.commit()
    conn.close()

st.set_page_config(page_title="CarbonTrack", layout="wide")
st.title("CarbonTrack: Personalized Carbon Footprint Estimator")

with st.form("carbon_form"):
    # put the three fields on one line
    col1, col2, col3 = st.columns(3)
    name    = col1.text_input("Name")
    age     = col2.number_input("Age", min_value=0, step=1)
    country = col3.text_input("Country")

    # echo back their details
    if name:
        st.write(f"Calculating carbon footprint for {name}, age {age}, living in {country}.")

    st.markdown("---")
    st.header("Weekly Usage")

    # Travel
    car_km     = st.number_input("Car (km/week)",      min_value=0.0, format="%.2f")
    plane_km   = st.number_input("Airplane (km/week)", min_value=0.0, format="%.2f")

    # Home energy
    cooking_kwh = st.number_input("Cooking (kWh/week)", min_value=0.0, format="%.2f")
    heating_kwh = st.number_input("Heating (kWh/week)", min_value=0.0, format="%.2f")

    # Food
    dairy_kg    = st.number_input("Dairy (kg/week)",   min_value=0.0, format="%.2f")
    meat_kg     = st.number_input("Meat (kg/week)",    min_value=0.0, format="%.2f")

    submit = st.form_submit_button("Estimate Carbon Footprint")

if submit:
    usage = {
        "car":     car_km,
        "airplane":plane_km,
        "cooking": cooking_kwh,
        "heating": heating_kwh,
        "dairy":   dairy_kg,
        "meat":    meat_kg,
    }
    emissions = {cat: usage[cat] * factors_df.loc[cat, "factor"] for cat in usage}
    total = sum(emissions.values())

    for cat, em in emissions.items():
        log_entry(name, age, country, cat, usage[cat], em)

    st.success(f"Thanks {name}! Your estimated weekly CO₂e is **{total:.2f} kg**")
    fig, ax = plt.subplots()
    ax.pie(
        emissions.values(),
        labels=[c.capitalize() for c in emissions],
        autopct="%.1f%%"
    )
    ax.set_title("Emissions Breakdown by Category")
    st.pyplot(fig)
