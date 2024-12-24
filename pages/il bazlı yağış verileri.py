import streamlit as st
import pandas as pd
import psycopg2
from datetime import datetime, timedelta
import plotly.express as px

# Veritabanı bağlantı bilgileri
DB_NAME = 'raindb'
DB_USER = 'postgres'
DB_PASSWORD = '134679'
DB_HOST = '192.168.34.192'  # PostgreSQL sunucusunun IP adresi
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

# Yağış miktarı açıklama kartı
def yagis_siddeti_karti(yagis_miktari):
    st.subheader("Yağış Şiddeti Açıklaması")

    if yagis_miktari < 2.5:
        st.markdown(
            """
            <div style='border: 2px solid green; padding: 10px; border-radius: 10px;'>
                <h3 style='color: green;'>Çok Hafif Yağış</h3>
                <p>Bu yağış miktarı (ör. {0:.2f} mm), zemini hafifçe nemlendirecek kadar azdır.</p>
            </div>
            """.format(yagis_miktari), unsafe_allow_html=True
        )
    elif 2.5 <= yagis_miktari < 7.6:
        st.markdown(
            """
            <div style='border: 2px solid blue; padding: 10px; border-radius: 10px;'>
                <h3 style='color: blue;'>Hafif Yağış</h3>
                <p>Bu yağış miktarı (ör. {0:.2f} mm), şemsiyeye ihtiyaç duyabileceğiniz hafif bir yağış anlamına gelir.</p>
            </div>
            """.format(yagis_miktari), unsafe_allow_html=True
        )
    elif 7.6 <= yagis_miktari < 50:
        st.markdown(
            """
            <div style='border: 2px solid orange; padding: 10px; border-radius: 10px;'>
                <h3 style='color: orange;'>Orta Şiddetli Yağış</h3>
                <p>Bu yağış miktarı (ör. {0:.2f} mm), sürekli bir yağış anlamına gelir ve yerel su birikintileri oluşabilir.</p>
            </div>
            """.format(yagis_miktari), unsafe_allow_html=True
        )
    elif 50 <= yagis_miktari < 100:
        st.markdown(
            """
            <div style='border: 2px solid red; padding: 10px; border-radius: 10px;'>
                <h3 style='color: red;'>Şiddetli Yağış</h3>
                <p>Bu yağış miktarı (ör. {0:.2f} mm), taşkın riskine neden olabilecek kadar yoğundur.</p>
            </div>
            """.format(yagis_miktari), unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style='border: 2px solid darkred; padding: 10px; border-radius: 10px;'>
                <h3 style='color: darkred;'>Aşırı Yağış</h3>
                <p>Bu yağış miktarı (ör. {0:.2f} mm), büyük sel riskine yol açabilecek kadar aşırıdır.</p>
            </div>
            """.format(yagis_miktari), unsafe_allow_html=True
        )

# Veritabanına bağlanma
conn = connect_db()

if conn:
    # Şehirlerin ID'lerini ve isimlerini veritabanından çekme
    query = "SELECT DISTINCT sehir_id, bolge FROM yagis_verisi;"  # 'bolge' şehri temsil eder
    cities_df = pd.read_sql_query(query, conn)

    if cities_df.empty:
        st.error("Şehir verisi bulunamadı.")
    else:
        # selectbox ile şehir seçme (şehir id'lerini kullanacağız)
        selected_city_id = st.selectbox("Bir şehir seçin:", cities_df['sehir_id'].tolist())  # 'sehir_id' kullanıyoruz

        # Şehir ID'sine göre sadece o şehre ait olan bölgeleri filtreleme
        city_bolges = cities_df[cities_df['sehir_id'] == selected_city_id]['bolge'].unique().tolist()

        # selectbox ile bölge seçme
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

            # Tarih sütununu datetime formatına çevirme
            weather_df['tarih'] = pd.to_datetime(weather_df['tarih'])

            # Son 30 günün verisini filtreleme
            son_30_gun = datetime.now() - timedelta(days=30)
            son_30_gun_verisi = weather_df[weather_df['tarih'] >= son_30_gun]

            # Son 30 günün verilerini çizgi grafiği ile gösterme
            st.subheader("Son 30 Günün Yağış Miktarları")
            fig = px.line(son_30_gun_verisi, x='tarih', y='yagis_miktari', title='Son 30 Günün Yağış Miktarları')
            st.plotly_chart(fig)

            # Ortalama yağış miktarını hesaplama
            ortalama_yagis = son_30_gun_verisi['yagis_miktari'].mean()
            st.subheader(f"Son 30 günde {selected_bolge} bölgesinde ortalama yağış miktarı: {ortalama_yagis:.2f} mm")

            # Yağış miktarına göre bilgi kartını gösterme
            yagis_siddeti_karti(ortalama_yagis)

    # Bağlantıyı kapatma
    conn.close()
else:
    st.error("Veritabanı bağlantısı sağlanamadı.")