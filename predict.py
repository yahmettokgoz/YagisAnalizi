import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import pickle

def tahmin_yap():
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
    future_dates = [df.index[-1] + pd.Timedelta(days=i) for i in range(1, 8)]
    future_exog = pd.DataFrame({
        'month': [date.month for date in future_dates],
        'day': [date.day for date in future_dates],
        'day_of_week': [date.dayofweek for date in future_dates]
    })
    forecast = model_fit.get_forecast(steps=7, exog=future_exog)
    forecast_mean = forecast.predicted_mean
    forecast_conf_int = forecast.conf_int()

    # Tahminlerin ortalamasını hesaplama
    average_forecast = forecast_mean.mean()

    return {
        'forecast_mean': forecast_mean,
        'forecast_conf_int': forecast_conf_int,
        'average_forecast': average_forecast,
        'future_dates': future_dates
    }