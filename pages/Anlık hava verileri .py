import requests
import streamlit as st

NEWS_API_KEY = 'fe836839d1e14e27b208a1cc9a7ba426'
OPENWEATHER_API_KEY = 'd6754a028a36fb8416e449a417437640'

# Arka plan görselini ayarlayan CSS kodu
def set_background_image():
    page_bg_img = """
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://raw.githubusercontent.com/yahmettokgoz/YagisAnalizi/4c8ce21bc2c0ac665898ea306147dbcb57ef753f/Ads%C4%B1z%20tasar%C4%B1m-2.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.9); /* Yan menüyü şeffaf yapar */
    }
    .emoji {
        font-size: 30px; /* Emoji boyutunu artır */
    }
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Arka planı uygula
set_background_image()

# Türkçe hava durumu açıklamalarına uygun emoji eşleştirme
weather_emojis = {
    "açık": "☀️",
    "az bulutlu": "🌤️",
    "parçalı az bulutlu": "⛅",
    "parçalı bulutlu": "☁️",
    "bulutlu": "🌥️",
    "sisli": "🌫️",
    "puslu": "🌫️",
    "yağmurlu": "🌧️",
    "hafif yağmur": "🌦️",
    "sağanak yağmur": "⛈️",
    "kar yağışlı": "❄️",
    "hafif kar": "🌨️",
    "gök gürültülü sağanak yağış": "⛈️",
    "hafif yağmur ve gök gürültüsü": "⛈️",
    "kapalı": "☁️",  # Kapalı durumu için bulut emojisi eklendi
}

def get_weather_and_news(city):
    # OpenWeather hava durumu alma
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&lang=tr"
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()  # API JSON sağlıyor

    if weather_data.get("cod") != 200:
        error_message = weather_data.get("message", "Bilinmeyen bir hata oluştu.")
        return f"API Hatası: {error_message}"

    weather_description = weather_data['weather'][0]['description']
    temperature = weather_data['main']['temp'] - 273.15  # Kelvin'den Celsius'a çevir

    # Haber API'si
    news_url = f"https://newsapi.org/v2/everything?q=weather&apiKey={NEWS_API_KEY}"
    news_response = requests.get(news_url)
    news_data = news_response.json()

    # Şehir adıyla başlıkları filtrele
    city_news_articles = [article for article in news_data['articles'] if city.lower() in article['title'].lower()]

    # Son 5 haberi göster
    city_news_articles = city_news_articles[:5]

    return weather_description, temperature, city_news_articles

st.title("Hava Durumu ve Hava Haberleri")

city = st.text_input("Şehir Adı", "İstanbul")

if city:
    result = get_weather_and_news(city)
    if isinstance(result, tuple):
        weather, temp, news = result
        emoji = weather_emojis.get(weather.lower(), "❓")  # Bilinmeyen bir durum için varsayılan emoji
        st.subheader(f"{city} Hava Durumu")
        st.markdown(
            f"""<div style="font-size: 24px;"><strong>Durum:</strong> {weather} <span class="emoji">{emoji}</span></div>""",
            unsafe_allow_html=True,
        )  # Durumun yanına büyütülmüş emoji ekledik
        st.markdown(f"**Sıcaklık:** {temp:.2f}°C")  # Sıcaklık kısmı kalın yazı
        
        st.subheader(f"{city} ile ilgili Son Hava Durumu Haberleri")
        if news:
            for article in news:
                st.markdown(f"**Başlık:** {article['title']}")
                st.write(f"Kaynak: {article['source']['name']}")
                st.write(f"Link: {article['url']}")
                st.write("\n")
        else:
            st.markdown("Bu şehirle ilgili haber bulunamadı.")
    else:
        st.error(result)
