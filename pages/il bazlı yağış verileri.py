import streamlit as st
import pandas as pd
import psycopg2

# Arka plan görseli için CSS kodu
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
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Arka planı uygula
set_background_image()

# Veritabanı bağlantı bilgileri
DB_NAME = 'raindb'
DB_USER = 'postgres'
DB_PASSWORD = '134679'
DB_HOST = '10.196.254.3'  # PostgreSQL sunucusunun IP adresi
DB_PORT = '5432'  # PostgreSQL varsayılan portu

def connect_db():
    """Veritabanına bağlan."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, 
            user=DB_USER, 
            password=DB_PASSWORD, 
            host=DB_HOST, 
            port=DB_PORT
        )
        print("Veritabanı bağlantısı başarılı")
        return conn
    except Exception as e:
        print("Veritabanına bağlanırken hata:", e)
        return None

# Veritabanına bağlanma
conn = connect_db()

if conn:
    # Şehirlerin ID'lerini ve isimlerini veritabanından çekme
    query = "SELECT DISTINCT sehir_id, bolge FROM yagis_verisi;"  # 'bolge' şehri temsil eder
    cities_df = pd.read_sql_query(query, conn)

    if cities_df.empty:
        st.error("Şehir verisi bulunamadı.")
    else:
        # `selectbox` ile şehir seçme (şehir id'lerini kullanacağız)
        selected_city_id = st.selectbox("Bir şehir seçin:", cities_df['sehir_id'].tolist())  # 'sehir_id' kullanıyoruz

        # Şehir ID'sine göre sadece o şehre ait olan bölgeleri filtreleme
        city_bolges = cities_df[cities_df['sehir_id'] == selected_city_id]['bolge'].unique().tolist()

        # `selectbox` ile bölge seçme
        selected_bolge = st.selectbox("Bir bölge seçin:", city_bolges)  # Burada dinamik olarak bölge seçiyoruz

        # Seçilen şehir ve bölgeye göre veriyi sorgulama
        query = f"""
        SELECT tarih, yagis_miktari 
        FROM yagis_verisi 
        WHERE sehir_id = {selected_city_id} AND bolge = '{selected_bolge}';
        """
        weather_df = pd.read_sql_query(query, conn)

        # Veriyi Streamlit'te gösterme
        if weather_df.empty:
            st.error(f"{selected_city_id} şehri ve {selected_bolge} bölgesi için veri bulunamadı.")
        else:
            st.write(f"{selected_city_id} şehri ve {selected_bolge} bölgesi için Yağış Miktarı ve Tarih Verisi:")
            st.write(weather_df)

            # Veriyi bar chart için uygun hale getirme
            weather_df['tarih'] = pd.to_datetime(weather_df['tarih'])  # Tarihleri datetime formatına çeviriyoruz
            weather_df.set_index('tarih', inplace=True)  # Tarihleri indeks olarak ayarlıyoruz

            # Bar chart verisi hazırlama
            chart_data = weather_df['yagis_miktari']

            # Streamlit ile bar chart oluşturma
            st.bar_chart(chart_data)

    # Bağlantıyı kapatma
    conn.close()
else:
    st.error("Veritabanı bağlantısı sağlanamadı.")
