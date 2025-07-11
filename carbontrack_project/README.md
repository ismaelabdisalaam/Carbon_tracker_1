# CarbonTrack Project Skeleton

This project contains a minimal skeleton for the CarbonTrack application.

## Front-End (MVP)
- **Path**: front_end/app.py
- **Framework**: Streamlit
- **Functionality**: Takes user input and echoes it back.
- **Setup**:
  ```
  cd front_end
  pip install -r requirements.txt
  streamlit run app.py
  ```

## Back-End Fetcher
- **Path**: backend/fetch_emission_factors.py
- **Functionality**: Fetches emission factors from a public CSV and stores them into `factors.db`.
- **Setup**:
  ```
  cd backend
  pip install -r requirements.txt
  python fetch_emission_factors.py
  ```

