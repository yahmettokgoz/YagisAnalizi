import streamlit as st
import requests

# API anahtarı
OPENWEATHER_API_KEY = 'd6754a028a36fb8416e449a417437640'

# Yağmur animasyonu CSS'i
def add_rain_animation():
    st.markdown("""
    <style>
    @keyframes rain {
        0% { transform: translateY(-100vh); }
        100% { transform: translateY(100vh); }
    }
    .raindrop {
        position: fixed;
        width: 2px;
        height: 20px;
        background: #add8e6;
        opacity: 0.5;
        animation: rain 1.5s linear infinite;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Yağmur damlalarını oluştur
    drops = "".join([
        f'<div class="raindrop" style="left: {i}%; animation-delay: {i/20}s;"></div>'
        for i in range(0, 100, 2)
    ])
    st.markdown(
        f'<div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none;">{drops}</div>',
        unsafe_allow_html=True
    )

# Başlık
st.title("Anlık Hava Durumu")

# Şehir listesi
cities = [
    "Adana", "Adıyaman", "Afyonkarahisar", "Ağrı", "Aksaray", "Amasya", "Ankara", "Antalya", "Ardahan", "Artvin", 
    "Aydın", "Balıkesir", "Bartın", "Batman", "Bayburt", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", 
    "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Düzce", "Edirne", "Elazığ", "Erzincan", "Erzurum", 
    "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Iğdır", "Isparta", "İstanbul", 
    "İzmir", "Kahramanmaraş", "Karabük", "Karaman", "Kars", "Kastamonu", "Kayseri", "Kırıkkale", "Kırklareli", 
    "Kırşehir", "Kilis", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Mardin", "Mersin", "Muğla", "Muş", 
    "Nevşehir", "Niğde", "Ordu", "Osmaniye", "Rize", "Sakarya", "Samsun", "Şanlıurfa", "Siirt", "Sinop", 
    "Şırnak", "Sivas", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Uşak", "Van", "Yalova", "Yozgat", "Zonguldak"
]

# Şehir seçimi
selected_city = st.selectbox("Şehir Seçin:", cities)

if st.button("Hava Durumunu Göster"):
    try:
        # API isteği
        url = f"http://api.openweathermap.org/data/2.5/weather?q={selected_city},TR&appid={OPENWEATHER_API_KEY}&units=metric&lang=tr"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Hava durumu bilgilerini göster
            st.write(f"Sıcaklık: {data['main']['temp']}°C")
            st.write(f"Nem: {data['main']['humidity']}%")
            weather_desc = data['weather'][0]['description'].lower()
            
            # Hava durumu açıklaması ve emojiler
            emoji = ""
            if "parçalı bulutlu" in weather_desc:
                emoji = " :cloud:"
            elif "parçalı az bulutlu" in weather_desc:
                emoji = " :cloud:"
            elif "sisli" in weather_desc:
                emoji = " :fog:"
            elif "yağmur" in weather_desc:
                add_rain_animation()
                emoji = " 🌧️"

            st.write(f"Durum: {weather_desc}{emoji}")
        else:
            st.error("Hava durumu bilgisi alınamadı!")
            
    except Exception as e:
        st.error(f"Bir hata oluştu: {str(e)}")
