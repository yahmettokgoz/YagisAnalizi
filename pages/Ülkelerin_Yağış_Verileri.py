import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Sayfa tasarımı için dinamik CSS
def set_custom_style():
    custom_css = """
    <style>
    body {
        font-family: 'Arial', sans-serif;
    }
    [data-testid="stAppViewContainer"] {
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    }
    [data-testid="stSidebar"] {
        padding: 1rem;
        border-radius: 10px;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

set_custom_style()

# Kıta ve ülke seçimleri
continents = {
    "Africa": ["Nigeria", "Kenya", "South Africa", "Egypt"],
    "Asia": ["China", "India", "Japan", "South Korea"],
    "Europe": ["Germany", "France", "Italy", "Spain", "Türkiye"],
    "North America": ["USA", "Canada", "Mexico", "Cuba"],
    "South America": ["Brazil", "Argentina", "Chile", "Peru"],
    "Oceania": ["Australia", "New Zealand", "Fiji", "Papua New Guinea"]
}

st.sidebar.header("Kıta ve Ülke Seçimi")
continent = st.sidebar.selectbox("Kıta seçiniz", options=list(continents.keys()))
country = st.sidebar.selectbox("Ülke seçiniz", options=continents[continent])

st.write(f"**Seçilen Kıta:** {continent}")
st.write(f"**Seçilen Ülke:** {country}")

# CSV dosyasını oku
try:
    # CSV dosyasını okuma
    df = pd.read_csv("ulke_data.csv")

    # Ülkeler ve yağış verilerini bir sözlüğe dönüştürme
    rain_data_10_years = dict(zip(df['country'], df['ten_year_avg_rainfall']))
    current_year_rain = dict(zip(df['country'], df['current_year_rainfall']))
except FileNotFoundError:
    st.error("ulke_data.csv dosyası bulunamadı.")
    rain_data_10_years = {}
    current_year_rain = {}

# Koordinat verisi
coordinates = {
    "Türkiye": [39.9208, 32.8541],
    "Germany": [51.1657, 10.4515],
    "France": [46.6034, 1.8883],
    "Italy": [41.8719, 12.5674],
    "Spain": [40.4637, -3.7492],
    "USA": [37.0902, -95.7129],
    "Canada": [56.1304, -106.3468],
    "Mexico": [23.6345, -102.5528],
    "China": [35.8617, 104.1954],
    "India": [20.5937, 78.9629],
    "Japan": [36.2048, 138.2529],
    "South Korea": [35.9078, 127.7669],
    "Nigeria": [9.0820, 8.6753],
    "Kenya": [-1.2864, 36.8172],
    "South Africa": [-30.5595, 22.9375],
    "Egypt": [26.8206, 30.8025],
    "Brazil": [-14.2350, -51.9253],
    "Argentina": [-38.4161, -63.6167],
    "Chile": [-35.6751, -71.5430],
    "Peru": [-9.1899, -75.0152],
    "Australia": [-25.2744, 133.7751],
    "New Zealand": [-40.9006, 174.8860],
    "Fiji": [-17.7134, 178.0650],
    "Papua New Guinea": [-6.314993, 143.95555],
    "Cuba": [21.5218, -77.7812]
}

# Yağış şiddeti açıklaması
def yagis_siddeti_karti(ulke, gecmis_ortalama, bu_yil):
    st.subheader(f"{ulke} Yağış Verisi Karşılaştırması")

    fark = bu_yil - gecmis_ortalama
    if fark > 0:
        durum = f"Bu yıl, son 10 yılın ortalamasına göre {fark:.2f} mm daha fazla yağmur yağdı."
        renk = "green"
    elif fark < 0:
        durum = f"Bu yıl, son 10 yılın ortalamasına göre {abs(fark):.2f} mm daha az yağmur yağdı."
        renk = "red"
    else:
        durum = "Bu yıl, son 10 yılın ortalamasına eşit miktarda yağmur yağdı."
        renk = "blue"

    st.markdown(
        f"""
        <div style='border: 2px solid {renk}; padding: 10px; border-radius: 10px; margin-bottom: 15px;'>
            <p style='color: {renk};'>{durum}</p>
        </div>
        """, unsafe_allow_html=True
    )

    # Grafik oluşturma
    if ulke in rain_data_10_years and ulke in current_year_rain:
        fig, ax = plt.subplots()
        ax.bar(['Bu Yıl', '10 Yıl Ortalaması'], [bu_yil, gecmis_ortalama], color=['blue', 'orange'])
        ax.set_title(f"{ulke} Yağış Karşılaştırması")
        ax.set_ylabel("Yağış (mm)")
        st.pyplot(fig)

# Seçilen ülke için yağış karşılaştırmasını göster
if country in rain_data_10_years and country in current_year_rain:
    yagis_siddeti_karti(country, rain_data_10_years[country], current_year_rain[country])
else:
    st.warning(f"{country} için eksik veri mevcut.")

# Harita bilgileri
if country in coordinates:
    latitude, longitude = coordinates[country]
    st.success(f"{country} konum bilgisi: {latitude}, {longitude}")

    # Harita için DataFrame oluştur
    map_data = pd.DataFrame({'lat': [latitude], 'lon': [longitude]})
    st.subheader("Seçilen Ülke Haritası")
    st.map(map_data)
else:
    st.warning(f"{country} için koordinat bilgisi bulunamadı.")
