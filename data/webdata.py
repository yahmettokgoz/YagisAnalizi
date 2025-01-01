import psycopg2
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import schedule
import time

class RainfallData:
    def __init__(self):
        self.url = "https://www.mgm.gov.tr/sondurum/toplam-yagis.aspx"
        self.driver = webdriver.Chrome()
        self.conn = self.connect_db()  
        self.cursor = self.conn.cursor()

    def connect_db(self):
        try:
            conn = psycopg2.connect(
                dbname='raindb',  
                user='postgres',  
                password='134679',  
                host='localhost',  
                port='5432'  
            )
            print("Veritabanı bağlantısı başarılı")
            return conn
        except Exception as e:
            print("Veritabanına bağlanırken hata:", e)

    def get_rainfall_data(self):
        self.driver.get(self.url)
        time.sleep(7)  #page bekleme

        #Tabloyu bulmak için bekleme
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="cph_body_pnlTablo"]/table'))
        )

        #tablo  bul xpath
        table = self.driver.find_element(By.XPATH, '//*[@id="cph_body_pnlTablo"]/table')
        rows = table.find_elements(By.TAG_NAME, "tr")

      
        current_date = datetime.now().strftime("%Y-%m-%d")  

        for row in rows[1:]:  #Başlık satırını atla
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) > 0:
                full_address = columns[0].text.strip() if len(columns) > 0 else None

                
                rainfall_text = columns[1].text.strip() if len(columns) > 1 else '0'

                #Yağış miktarını float'a çeviriyoruz
                rainfall = float(rainfall_text.replace(',', '.')) if rainfall_text else 0.0

                #şehir adı ve bölgeyi ayrıştır
                city_name = full_address.split(",")[0].strip()  # İlk kısım şehir adı
                bolge = ",".join(full_address.split(",")[1:]).strip()  # Geri kalan kısım bölge

                #tablodan plaka bul
                sehir_id = self.get_sehir_id(city_name)

                if sehir_id:
                    
                    self.insert_data(sehir_id, bolge, rainfall, current_date)
                else:
                    print(f"Şehir ID bulunamadı: {city_name}")

        self.driver.quit()
        self.conn.close()  

    def get_sehir_id(self, city_name):
        try:
            query = "SELECT id FROM sehir WHERE sehir_adi= %s;"
            self.cursor.execute(query, (city_name,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print("Şehir ID alınırken hata:", e)
            return None

    def insert_data(self, sehir_id, bolge, rainfall, measurement_date):
        try:
            insert_query = """
            INSERT INTO yagis_verisi (sehir_id, bolge, yagis_miktari, tarih)
            VALUES (%s, %s, %s, %s);
            """
            self.cursor.execute(insert_query, (sehir_id, bolge, rainfall, measurement_date))
            self.conn.commit()  
            print(f"Veri eklendi: Şehir ID: {sehir_id}, Bölge: {bolge}, Yağış: {rainfall}, Tarih: {measurement_date}")
        except Exception as e:
            print("Veri eklerken hata:", e)

def job():
    rainfall_data = RainfallData()
    rainfall_data.get_rainfall_data()

# Her gün saat 23:40'da çalışacak şekilde zamanla
schedule.every().day.at("23:40").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)