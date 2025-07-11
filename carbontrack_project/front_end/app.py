import os
import sqlite3
import pandas as pd
import requests
import streamlit as st
from datetime import date

# Constants
CSV_URL = "https://raw.githubusercontent.com/climatiq/climatiq/main/climatiq/cli/data/emissions_factors.csv"
DB_FILE = "carbontrack.db"

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS factors (
            category TEXT PRIMARY KEY,
            co2e REAL,
            unit TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            log_date TEXT,
            category TEXT,
            amount REAL,
            emissions REAL
        )
    """)
    conn.commit()
    conn.close()

# Load and store emission factors (cached)
@st.cache_data
def load_and_cache_factors():
    df = pd.read_csv(CSV_URL, usecols=['category','co2e','unit'])
    df = df.drop_duplicates(subset=['category'])
    conn = sqlite3.connect(DB_FILE)
    df.to_sql('factors', conn, if_exists='replace', index=False)
    conn.close()
    return df

# Log an activity
def log_activity(log_date, category, amount, emissions):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO logs VALUES (?,?,?,?)", 
              (log_date, category, amount, emissions))
    conn.commit()
    conn.close()

# Fetch logs as DataFrame (cached)
@st.cache_data
def get_logs_df():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql("SELECT * FROM logs", conn, parse_dates=['log_date'])
    conn.close()
    return df

# Streamlit App
st.set_page_config(page_title="CarbonTrack", layout="wide")
st.title("CarbonTrack: Personal Carbon Footprint Tracker")
st.write("Log your activities and track your CO₂e emissions over time.")

# Setup
init_db()
factors_df = load_and_cache_factors()

# Tabs for input and dashboard
tab1, tab2 = st.tabs(["Log Activity", "Dashboard"])

with tab1:
    st.header("Log a New Activity")
    with st.form("activity_form"):
        log_date = st.date_input("Date", value=date.today())
        category = st.selectbox("Activity Category", factors_df['category'].tolist())
        unit = factors_df.loc[factors_df['category']==category, 'unit'].iloc[0]
        amount = st.number_input(f"Amount ({unit})", min_value=0.0, format="%.2f")
        submit = st.form_submit_button("Submit")
        if submit and amount > 0:
            factor = factors_df.loc[factors_df['category']==category, 'co2e'].iloc[0]
            emissions = factor * amount
            log_activity(log_date.isoformat(), category, amount, emissions)
            st.success(f"Logged {amount} {unit} of {category} → {emissions:.2f} kg CO₂e")

with tab2:
    st.header("Emissions Dashboard")
    logs_df = get_logs_df()
    if logs_df.empty:
        st.info("No activities logged yet.")
    else:
        st.subheader("Activity Logs")
        st.dataframe(logs_df)

        daily = logs_df.groupby('log_date')['emissions'].sum().reset_index()
        daily.columns = ['Date', 'Emissions (kg CO₂e)']
        st.subheader("Daily Emissions")
        st.line_chart(data=daily.set_index('Date'))

        total = daily['Emissions (kg CO₂e)'].sum()
        avg = daily['Emissions (kg CO₂e)'].mean()
        st.subheader("Summary Metrics")
        col1, col2 = st.columns(2)
        col1.metric("Total Emissions (kg CO₂e)", f"{total:.2f}")
        col2.metric("Average Daily Emissions", f"{avg:.2f}")

