import streamlit as st
import pandas as pd
import requests

# OpenWeather API anahtarı
API_KEY = 'd6754a028a36fb8416e449a417437640'

# Arka plan görseli için CSS
def set_background_image():
    page_bg_img = """
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://raw.githubusercontent.com/yahmettokgoz/YagisAnalizi/8e5015b9898cf46724898dc20c0fb73d25bdd38b/Ads%C4%B1z%20tasar%C4%B1m-3.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.9); /* Yan menüyü şeffaf yapar */
    }
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Arka planı uygula
set_background_image()

# Kıta ve ülke seçimleri
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

st.write(f"Seçilen kıta: {continent}")
st.write(f"Seçilen ülke: {country}")

# Hava durumu verisini alma fonksiyonu
def get_weather_data(country):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={country}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Veri alınırken bir hata oluştu: {response.status_code}")
        return None

# Yağış verilerini işleme fonksiyonu
def extract_rain_data(weather_data):
    rain_data = []
    for item in weather_data['list']:
        date = pd.to_datetime(item['dt_txt'])
        rain = item.get('rain', {}).get('3h', 0)  # 3 saatlik yağış miktarı
        rain_data.append({"Date": date, "Rain (mm)": rain})
    return pd.DataFrame(rain_data)

# Hava durumu verilerini al
weather_data = get_weather_data(country)

if weather_data:
    # Yağış verilerini işle
    rain_df = extract_rain_data(weather_data)

    # Veriyi grafikle göster
    st.line_chart(rain_df.set_index("Date")["Rain (mm)"])

    # Veriyi tablo olarak göster
    st.write("Yağış verisi:", rain_df)
