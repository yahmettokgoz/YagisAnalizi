import requests
import streamlit as st

NEWS_API_KEY = 'fe836839d1e14e27b208a1cc9a7ba426'
OPENWEATHER_API_KEY = 'd6754a028a36fb8416e449a417437640'  

def get_weather_and_news(city):
    # OpenWeather hava durumu alma
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&lang=tr"
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()# apı json sağlıyor

    if weather_data.get("cod") != 200:
        error_message = weather_data.get("message", "Bilinmeyen bir hata oluştu.")
        return f"API Hatası: {error_message}"

    weather_description = weather_data['weather'][0]['description']
    temperature = weather_data['main']['temp'] - 273.15  #Apide birim kelvin burada Celciusa çevirme işlemi 

    # Haber apisi
    news_url = f"https://newsapi.org/v2/everything?q=weather&apiKey={NEWS_API_KEY}"
    news_response = requests.get(news_url)
    news_data = news_response.json()

    #Haberleri şehir adıyla filtreleme işi (başlıklarda şehir adı geçiyorsa) burada başlıklar geçmiyorsa boş
    city_news_articles = [article for article in news_data['articles'] if city.lower() in article['title'].lower()]
    
    # Enson 5 haber eski haberler görünmesin diye
    city_news_articles = city_news_articles[:5]  

    return weather_description, temperature, city_news_articles

st.title("Hava Durumu ve Hava Haberleri")

city = st.text_input("Şehir Adı", "İstanbul")

if city:
    result = get_weather_and_news(city)
    if isinstance(result, tuple):
        weather, temp, news = result
        st.subheader(f"{city} Hava Durumu")
        st.write(f"Durum: {weather}")
        st.write(f"Sıcaklık: {temp:.2f}°C")
        st.subheader(f"{city} ile ilgili Son Hava Durumu Haberleri")
        if news:
            for article in news:
                st.write(f"Başlık: {article['title']}")
                st.write(f"Kaynak: {article['source']['name']}")
                st.write(f"Link: {article['url']}")
                st.write("\n")
        else:
            st.write("Bu şehirle ilgili haber bulunamadı.")
    else:
        st.error(result)  #except mesajları
