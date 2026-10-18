import requests

url = "https://api.open-meteo.com/v1/forecast"

params = {"latitude" : 35.68 , "longitude" :139.76 , "daily" : ["temperature_2m_max" , "temperature_2m_min" , "precipitation_probability_max"] , "timezone" : "Asia/Tokyo" , "forecast_days" :1 }
response = requests.get(url, params=params)
data = response.json()

daily = data["daily"]
max_temp = daily["temperature_2m_max"][0]
min_temp = daily["temperature_2m_min"][0]
rain = daily["precipitation_probability_max"][0]

print(f"{daily['time'][0]} 東京：最高気温 {max_temp}℃ /最低気温 {min_temp}℃ /降水確率{rain}%")