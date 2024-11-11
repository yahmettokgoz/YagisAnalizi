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
        time.sleep(7)  #sayfanın yüklenmesi için geçici bekleme

        #tabloyu bulmak için bekleme
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="cph_body_pnlTablo"]/table'))
        )

        #tablo bulma
        table = self.driver.find_element(By.XPATH, '//*[@id="cph_body_pnlTablo"]/table')
        rows = table.find_elements(By.TAG_NAME, "tr")

        
        current_date = datetime.now().strftime("%Y-%m-%d")  

        for row in rows[1:]:  #ilk satırı atlama başlık olma durumu
            columns = row.find_elements(By.TAG_NAME, "td")
            if len(columns) > 0:
                city_name = columns[0].text.strip() if len(columns) > 0 else None
                
                
                rainfall_text = columns[1].text.strip() if len(columns) > 1 else '0'
                
                
                print(f"Çekilen yağış verisi: {rainfall_text}")

                # ',' varsa onu '.' ile değiştiriyoruz ve float'a çeviriyoruz
                rainfall = float(rainfall_text.replace(',', '.')) if rainfall_text else 0.0

                #db ekleme 
                self.insert_data(city_name, rainfall, current_date)

        self.driver.quit()
        self.conn.close()  

    def insert_data(self, city_name, rainfall, measurement_date):
        try:
            insert_query = """
            INSERT INTO rainfall_data (city_name, rainfall, measurement_date)
            VALUES (%s, %s, %s);
            """
            self.cursor.execute(insert_query, (city_name, rainfall, measurement_date))
            self.conn.commit()  
            print(f"Veri eklendi: {city_name}, {rainfall}, {measurement_date}")
        except Exception as e:
            print("Veri eklerken hata:", e)


rainfall_data = RainfallData()
rainfall_data.get_rainfall_data()
