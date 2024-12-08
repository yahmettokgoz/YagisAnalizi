import streamlit as st
import pandas as pd
import requests


API_KEY = 'd6754a028a36fb8416e449a417437640'


continents = {
    "Africa": ["Nigeria", "Kenya", "South Africa", "Egypt"],
    "Asia": ["China", "India", "Japan", "South Korea"],
    "Europe": ["Germany", "France", "Italy", "Spain", "Türkiye"],
    "North America": ["USA", "Canada", "Mexico", "Cuba"],
    "South America": ["Brazil", "Argentina", "Chile", "Peru"],
    "Oceania": ["Australia", "New Zealand", "Fiji", "Papua New Guinea"]
}

continent = st.selectbox("Kıta seçiniz", options=list(continents.keys()))
country = st.selectbox("Ülke seçiniz", options=continents[continent])

st.write(f"Selected continent: {continent}")
st.write(f"Selected country: {country}")


def get_weather_data(country):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={country}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Veri alınırken bir hata oluştu: {response.status_code}")
        return None

#  opendan yağış verisini alma
def extract_rain_data(weather_data):
    rain_data = []
    for item in weather_data['list']:
        date = pd.to_datetime(item['dt_txt'])
        rain = item.get('rain', {}).get('3h', 0)  #3 saatlik yağış miktarı
        rain_data.append({"Date": date, "Rain (mm)": rain})
    return pd.DataFrame(rain_data)

#veriyi getir
weather_data = get_weather_data(country)

if weather_data:
    rain_df = extract_rain_data(weather_data)

    #veriyi tabloya ekle 
    st.line_chart(rain_df.set_index("Date")["Rain (mm)"])

    st.write("Yağış verisi:", rain_df)
