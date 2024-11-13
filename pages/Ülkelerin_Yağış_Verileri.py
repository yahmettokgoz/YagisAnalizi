

import streamlit as st
import pandas as pd
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




# Örnek veri oluşturma
data = {
    "Yıl": [2020, 2021, 2022, 2023, 2024],
    "Satış": [200, 300, 400, 500, 600]
}

# Veri çerçevesi oluşturma
df = pd.DataFrame(data)

# Line chart (çizgi grafiği) oluşturma
st.line_chart(df.set_index("Yıl"))
