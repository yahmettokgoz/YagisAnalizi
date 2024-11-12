import streamlit as st
import streamlit as st
import pandas as pd
import pydeck as pdk
st.title('Yağış analiz uygulaması')


st.markdown('Bu web sitesi ile belirlediğiniz tarih aralığındaki yağış verilerini inceleyebilir,grafikler ve tablolar üzerinde detaylı analiz yapabilirsiniz.')

'---'

st.title("Dünya Haritası")


data = pd.DataFrame({
    'lat': [40.7128, 34.0522, 37.7749],  
    'lon': [-74.0060, -118.2437, -122.4194]  
})


st.map(data)






'---'


st.title(" Türkiye Haritası")

data = pd.DataFrame({
    'lat': [41.0082, 39.9334, 38.4237, 38.6807, 38.3552, 40.5506],
    'lon': [28.9784, 32.8597, 27.1428, 39.2264, 38.3095, 34.9556],
    'şehir': ["İstanbul", "Ankara", "İzmir", "Elazığ", "Malatya", "Çorum"]
})

layer = pdk.Layer(
    "ScatterplotLayer",
    data,
    get_position="[lon, lat]",
    get_color="[255, 0, 0, 160]",  
    get_radius=20000,
)

view_state = pdk.ViewState(
    latitude=39.9334,
    longitude=32.8597,
    zoom=5,
    pitch=0,
)

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/light-v10"  
)

st.pydeck_chart(deck)

'---'

st.title("Hakkımızda")
st.write("TELEFON=0551 236 7530")
st.write("MAİL=FIRAT@gmail.com")
st.write("ADRES=Elazığ/Fırat Üniversitesi")