

import streamlit as st

# Kıtalar ve ülkeler verisi
continents = {
    "Africa": ["Nigeria", "Kenya", "South Africa", "Egypt"],
    "Asia": ["China", "India", "Japan", "South Korea"],
    "Europe": ["Germany", "France", "Italy", "Spain","Türkiye"],
    "North America": ["USA", "Canada", "Mexico", "Cuba"],
    "South America": ["Brazil", "Argentina", "Chile", "Peru"],
    "Oceania": ["Australia", "New Zealand", "Fiji", "Papua New Guinea"]
}


continent = st.selectbox("Kıta seçiniz", options=list(continents.keys()))


country = st.selectbox("Ülke seçiniz", options=continents[continent])

st.write(f"Selected continent: {continent}")