import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Şehir seçimi ve veri görselleştirme
st.title("Şehirler")

sehir = st.selectbox(  # Şehir seçme
    "Şehir seçiniz",
    ("Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir",
     "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli",
     "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane",
     "Hakkâri", "Hatay", "Iğdır", "Isparta", "İstanbul", "İzmir", "Kahramanmaraş", "Karabük", "Karaman",
     "Kars", "Kastamonu", "Kayseri", "Kırıkkale", "Kırklareli", "Kırşehir", "Kilis", "Kocaeli", "Konya",
     "Kütahya", "Malatya", "Manisa", "Mardin", "Mersin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu",
     "Osmaniye", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Şanlıurfa", "Şırnak", "Tekirdağ",
     "Tokat", "Trabzon", "Tunceli", "Uşak", "Van", "Yalova", "Yozgat", "Zonguldak", "Aksaray", "Bayburt",
     "Batman", "Bartın", "Ardahan", "Karabük", "Osmaniye", "Düzce"),
)

st.info(f" {sehir} şehrinin anlık yağış durumu ", icon="ℹ️")

cities = [
    "Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir",
    "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli",
    "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane",
    "Hakkâri", "Hatay", "Iğdır", "Isparta", "İstanbul", "İzmir", "Kahramanmaraş", "Karabük", "Karaman",
    "Kars", "Kastamonu", "Kayseri", "Kırıkkale", "Kırklareli", "Kırşehir", "Kilis", "Kocaeli", "Konya",
    "Kütahya", "Malatya", "Manisa", "Mardin", "Mersin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu",
    "Osmaniye", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Şanlıurfa", "Şırnak", "Tekirdağ",
    "Tokat", "Trabzon", "Tunceli", "Uşak", "Van", "Yalova", "Yozgat", "Zonguldak", "Aksaray", "Bayburt",
     "Batman", "Bartın", "Ardahan", "Karabük", "Osmaniye", "Düzce"
]

# Rastgele 12 aylık yağış verisi oluşturma
np.random.seed(0)
rain_data = {city: np.random.uniform(10, 100, 12) for city in cities}

# DataFrame oluşturma
rain_df = pd.DataFrame(rain_data, index=["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"])

# Seçilen şehrin verilerini görselleştirme
st.subheader(f"{sehir} Şehrinin 12 Aylık Ortalama Yağış Verisi")

# Veriyi uygun formata çevirme
selected_city_data = rain_df[sehir].reset_index()
selected_city_data.columns = ["Ay", "Yağış (mm)"]

# Plotly ile grafik oluşturma
fig = px.bar(
    selected_city_data,
    x="Ay",
    y="Yağış (mm)",
    title=f"{sehir} Şehrinin 12 Aylık Yağış Verisi",
    labels={"Yağış (mm)": "Yağış Miktarı (mm)", "Ay": "Aylar"},
    template="plotly_white",
    color="Yağış (mm)",
    color_continuous_scale="Blues"
)

st.plotly_chart(fig)
