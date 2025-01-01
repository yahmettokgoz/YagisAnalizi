import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
from statsmodels.tsa.statespace.sarimax import SARIMAX
import pickle
import warnings
import sys
import os

# Uyarıları kapat
warnings.filterwarnings('ignore')

# Ana dizini Python path'ine ekle
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_dir)

# Sayfa başlığı
st.title("🌧️ Yağış Tahmini 🌧️")

# Veriyi okuma ve hazırlama
df = pd.read_csv('yagis_verisi.csv')
df['tarih'] = pd.to_datetime(df['tarih'])
df = df.drop_duplicates(subset=['tarih'])
df.set_index('tarih', inplace=True)
df = df.asfreq('D')  # Günlük frekans
df['yagis_miktari'] = df['yagis_miktari'].interpolate(method='time')

# Mevsimsel bileşenler ekleme
df['month'] = df.index.month
df['day'] = df.index.day
df['day_of_week'] = df.index.dayofweek

# SARIMA modeli ile zaman serisi tahmini
exog = df[['month', 'day', 'day_of_week']]
model = SARIMAX(df['yagis_miktari'], order=(2, 1, 2), seasonal_order=(1, 1, 1, 7), exog=exog)
model_fit = model.fit(disp=False)

# Bir hafta için tahmin yapma
future_dates = [df.index[-1] + timedelta(days=i) for i in range(1, 8)]
future_exog = pd.DataFrame({
    'month': [date.month for date in future_dates],
    'day': [date.day for date in future_dates],
    'day_of_week': [date.dayofweek for date in future_dates]
})
forecast = model_fit.get_forecast(steps=7, exog=future_exog)
forecast_mean = forecast.predicted_mean
forecast_conf_int = forecast.conf_int()

# Yağış şiddeti kartı fonksiyonu
def yagis_siddeti_karti(tarih, yagis_miktari):
    if yagis_miktari < 2.5:
        renk = 'green'
        seviye = 'Çok Hafif Yağış'
        aciklama = 'Bu yağış miktarı (ör. {0:.2f} mm), zemini hafifçe nemlendirecek kadar azdır.'.format(yagis_miktari)
    elif 2.5 <= yagis_miktari < 7.6:
        renk = 'blue'
        seviye = 'Hafif Yağış'
        aciklama = 'Bu yağış miktarı (ör. {0:.2f} mm), hafif bir yağış olarak kabul edilir.'.format(yagis_miktari)
    elif 7.6 <= yagis_miktari < 50:
        renk = 'orange'
        seviye = 'Orta Şiddetli Yağış'
        aciklama = 'Bu yağış miktarı (ör. {0:.2f} mm), orta şiddetli bir yağış olarak kabul edilir.'.format(yagis_miktari)
    else:
        renk = 'red'
        seviye = 'Şiddetli Yağış'
        aciklama = 'Bu yağış miktarı (ör. {0:.2f} mm), şiddetli bir yağış olarak kabul edilir.'.format(yagis_miktari)

    st.markdown(
        f"""
        <div style='border: 2px solid {renk}; padding: 10px; border-radius: 10px; margin-bottom: 10px;'>
            <h3 style='color: {renk};'>{tarih} - {seviye}</h3>
            <p>{aciklama}</p>
        </div>
        """, unsafe_allow_html=True
    )

# Sonuçları kart formatında gösterme
st.subheader("📅 Günlük Yağış Tahminleri 📅")
for i, date in enumerate(future_dates):
    yagis_siddeti_karti(date.strftime('%Y-%m-%d'), forecast_mean[i])

# Tahmin sonuçlarını görselleştirme
fig = px.line(df, x=df.index, y='yagis_miktari', title='Yağış Miktarı Tahmini', labels={'yagis_miktari': 'Yağış Miktarı (mm)'})
fig.add_scatter(x=future_dates, y=forecast_mean, mode='lines+markers', name='Tahmin Edilen Yağış Miktarı', line=dict(color='red'))
fig.add_scatter(x=future_dates, y=forecast_conf_int.iloc[:, 0], mode='lines', name='Alt Güven Sınırı', line=dict(width=0.5, color='orange'))
fig.add_scatter(x=future_dates, y=forecast_conf_int.iloc[:, 1], mode='lines', name='Üst Güven Sınırı', line=dict(width=0.5, color='orange'))
st.plotly_chart(fig)

# Bilgilendirme
st.markdown("""
### Nasıl Çalışır?
- Model, geçmiş yağış verilerini kullanarak bir hafta için genel bir yağış tahmini yapar.
- Bu tahmin tüm Türkiye için ortalama bir tahmindir.
""", unsafe_allow_html=True)