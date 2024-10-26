import psycopg2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime  

class RainfallData:
    def __init__(self):
        self.url = "https://www.mgm.gov.tr/sondurum/toplam-yagis.aspx"
        self.driver = webdriver.Chrome()
        self.conn = self.connect_db()  # Veritabanına bağlan
        self.cursor = self.conn.cursor()

    def connect_db(self):
        try:
            conn = psycopg2.connect(
                dbname='raindb',  # Veritabanı adı
                user='postgres',    # Kullanıcı adı
                password='134679',       # Şifre
                host='localhost',        # Sunucu
                port='5432'              # PostgreSQL varsayılan portu
            )
            print("Veritabanı bağlantısı başarılı")
            return conn
        except Exception as e:
            print("Veritabanına bağlanırken hata:", e)

    def get_rainfall_data(self):
        self.driver.get(self.url)
        time.sleep(7)  # Sayfanın yüklenmesi için geçici bekleme

        # Tabloyu bulmak için bekleme
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="cph_body_pnlTablo"]/table'))
        )

        # Tabloyu bul
        table = self.driver.find_element(By.XPATH, '//*[@id="cph_body_pnlTablo"]/table')
        rows = table.find_elements(By.TAG_NAME, "tr")

        # Şu anki tarihi al
        current_date = datetime.now().strftime("%Y-%m-%d")  # Mevcut tarihi al

        for row in rows[1:]:  # Başlık satırını atla
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) > 0:
                city_name = columns[0].text.strip() if len(columns) > 0 else None
                
                # Yağış verisini 1. sütundan alıyoruz
                rainfall_text = columns[1].text.strip() if len(columns) > 1 else '0'
                
                # Yağış miktarını ekrana basarak kontrol edelim
                print(f"Çekilen yağış verisi: {rainfall_text}")

                # ',' varsa onu '.' ile değiştiriyoruz ve float'a çeviriyoruz
                rainfall = float(rainfall_text.replace(',', '.')) if rainfall_text else 0.0

                # Basitleştirilmiş veriyi ekle
                self.insert_data(city_name, rainfall, current_date)

        self.driver.quit()
        self.conn.close()  # Veritabanı bağlantısını kapat

    def insert_data(self, city_name, rainfall, measurement_date):
        try:
            insert_query = """
            INSERT INTO rainfall_data (city_name, rainfall, measurement_date)
            VALUES (%s, %s, %s);
            """
            self.cursor.execute(insert_query, (city_name, rainfall, measurement_date))
            self.conn.commit()  # Değişiklikleri kaydet
            print(f"Veri eklendi: {city_name}, {rainfall}, {measurement_date}")
        except Exception as e:
            print("Veri eklerken hata:", e)

# Kullanım
rainfall_data = RainfallData()
rainfall_data.get_rainfall_data()
