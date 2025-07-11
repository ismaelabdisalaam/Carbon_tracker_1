import streamlit as st

st.title("CarbonTrack")

# User input
user_input = st.text_input("Type your activity and press Enter:")

if user_input:
    st.write("You entered ➞", user_input)
