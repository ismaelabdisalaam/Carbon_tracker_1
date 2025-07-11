import streamlit as st

st.title("CarbonTrack: Emissions Calculator")

categories = ["Vehicle travel", "Home energy use"]

# Prompt user to pick a category and enter an amount
category = st.selectbox("Select an activity category", categories)
amount = st.number_input(f"Enter amount for {category}", min_value=0.0, format="%.2f")

# When they click Calculate, echo back their choice
if st.button("Calculate"):
    if amount > 0:
        st.success(f"You selected **{category}** and entered **{amount}**.")
    else:
        st.error("Please enter an amount greater than zero.")
