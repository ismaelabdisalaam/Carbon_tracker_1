# CarbonTrack Project

CarbonTrack is a personalized carbon‐footprint estimator that lets users enter their weekly usage across travel, home energy, and food categories, then returns an estimated CO₂e total along with a breakdown chart. It stores both emission factors and user logs in a local SQLite database.

## Features

- **Personal Details**: Name, age, country  
- **Usage Input**: Weekly values for Car, Airplane, Cooking, Heating, Dairy, Meat  
- **Estimation**: Calculates CO₂e per category using hard-coded factors  
- **Persistence**: Saves each estimate to `carbontrack.db`  
- **Visualization**: Displays a pie chart breakdown of emissions  

## Front-End
- **Path**: `app.py`
- **Framework**: Streamlit
- **Functionality**:  
  1. Prompts the user for name, age, and country.  
  2. Asks for weekly usage in six categories (car, airplane, cooking, heating, dairy, meat).  
  3. Calculates CO₂e per category using factors from the database.  
  4. Logs each entry to the `logs` table and displays the total weekly CO₂e with a pie-chart breakdown.
- **Dependencies**:
  ```text
  streamlit
  pandas
  matplotlib

## Back-End Fetcher
- **Path**: backend/fetch_emission_factors.py
- **Functionality**: Creates (if needed) the emission_factors table in carbontrack.db.
- Inserts or replaces six hard-coded emission factors covering travel, home energy, and food categories. `carbontrack.db`.
- **Setup**:
  ```
  cd backend
  pip install -r requirements.txt
  python fetch_emission_factors.py
  ```

