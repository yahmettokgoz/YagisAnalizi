import streamlit as st
import pandas as pd

# Sayfa tasarımı için CSS
def set_custom_style():
    custom_css = """
    <style>
    body {
        background-color: #f5f5f5;
        font-family: 'Arial', sans-serif;
    }
    [data-testid="stAppViewContainer"] {
        padding: 2rem;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    }
    [data-testid="stSidebar"] {
        background-color: #e8eaf6;
        padding: 1rem;
        border-radius: 10px;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# CSS uygulaması
set_custom_style()

# Başlık
st.title("Yağış Verisi ve Harita Görüntüleyici 🌦")
st.markdown("Seçilen bir kıta ve ülkeye ait yağış verilerini, konumunu harita üzerinde görün ve yağış şiddeti karşılaştırmasını yapın.")

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

# Manuel koordinat verisi
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
    # Diğer ülkeler eklenebilir...
}

# Beklenen yağış miktarları (örnek veriler)
expected_rain = {
    "Türkiye": 50,
    "Germany": 40,
    "France": 30,
    "Italy": 45,
    "Spain": 35,
    "USA": 60,
    "Canada": 55,
    "Mexico": 40,
    "China": 70,
    "India": 80,
    # Diğer ülkeler için beklenen yağışlar eklenebilir...
}

# Örnek yağış verisi (gerçek zamanlı veri alabilirsiniz)
actual_rain = 45  # Burada örnek bir veri kullanılıyor, gerçek veri alınabilir.

# Yağış şiddeti açıklaması
def yagis_siddeti_karti(yagis_miktari, beklenen_miktar):
    st.subheader("Yağış Şiddeti ve Karşılaştırma")

    # Yağış farkını hesapla
    fark = yagis_miktari - beklenen_miktar
    if fark > 0:
        durum = f"Bu yıl beklenenden {fark:.2f} mm daha fazla yağmur yağdı."
        renk = "green"
    elif fark < 0:
        durum = f"Bu yıl beklenenden {abs(fark):.2f} mm daha az yağmur yağdı."
        renk = "red"
    else:
        durum = "Bu yıl beklenen miktarda yağmur yağdı."
        renk = "blue"

    # Yağış şiddetine göre kartı oluştur
    if yagis_miktari < 2.5:
        st.markdown(
            f"""
            <div style='border: 2px solid {renk}; padding: 10px; border-radius: 10px;'>
                <h3 style='color: {renk};'>Çok Hafif Yağış</h3>
                <p>Bu yağış miktarı (ör. {yagis_miktari:.2f} mm), zemini hafifçe nemlendirecek kadar azdır. {durum}</p>
            </div>
            """, unsafe_allow_html=True
        )
    elif 2.5 <= yagis_miktari < 7.6:
        st.markdown(
            f"""
            <div style='border: 2px solid {renk}; padding: 10px; border-radius: 10px;'>
                <h3 style='color: {renk};'>Hafif Yağış</h3>
                <p>Bu yağış miktarı (ör. {yagis_miktari:.2f} mm), şemsiyeye ihtiyaç duyabileceğiniz hafif bir yağış anlamına gelir. {durum}</p>
            </div>
            """, unsafe_allow_html=True
        )
    elif 7.6 <= yagis_miktari < 50:
        st.markdown(
            f"""
            <div style='border: 2px solid {renk}; padding: 10px; border-radius: 10px;'>
                <h3 style='color: {renk};'>Orta Şiddetli Yağış</h3>
                <p>Bu yağış miktarı (ör. {yagis_miktari:.2f} mm), sürekli bir yağış anlamına gelir ve yerel su birikintileri oluşabilir. {durum}</p>
            </div>
            """, unsafe_allow_html=True
        )
    elif 50 <= yagis_miktari < 100:
        st.markdown(
            f"""
            <div style='border: 2px solid {renk}; padding: 10px; border-radius: 10px;'>
                <h3 style='color: {renk};'>Şiddetli Yağış</h3>
                <p>Bu yağış miktarı (ör. {yagis_miktari:.2f} mm), taşkın riskine neden olabilecek kadar yoğundur. {durum}</p>
            </div>
            """, unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style='border: 2px solid {renk}; padding: 10px; border-radius: 10px;'>
                <h3 style='color: {renk};'>Aşırı Yağış</h3>
                <p>Bu yağış miktarı (ör. {yagis_miktari:.2f} mm), büyük sel riskine yol açabilecek kadar aşırıdır. {durum}</p>
            </div>
            """, unsafe_allow_html=True
        )

# Yağış şiddeti ve karşılaştırma
yagis_siddeti_karti(actual_rain, expected_rain.get(country, 50))  # Beklenen yağış 50 mm olarak varsayıldı

# Yağış verisini oluştur (örnek veriler)
rain_data = {
    "Tarih": pd.date_range(start="2024-01-01", periods=10, freq="D"),
    "Yağış (mm)": [5, 10, 3, 12, 7, 0, 8, 15, 20, 4]
}
rain_df = pd.DataFrame(rain_data)

# Yağış verilerini göster
st.subheader("Yağış Verisi Grafiği")
st.line_chart(rain_df.set_index("Tarih")["Yağış (mm)"])

# Koordinat kontrolü
if country in coordinates:
    latitude, longitude = coordinates[country]
    st.success(f"{country} konum bilgisi: {latitude}, {longitude}")
    
    # Harita için DataFrame oluştur
    map_data = pd.DataFrame({
        'lat': [latitude],
        'lon': [longitude]
    })
    
    # Streamlit haritasını göster
    st.subheader("Seçilen Ülke Haritası")
    st.map(map_data)
else:
    st.warning(f"{country} için koordinat bilgisi bulunamadı.")
