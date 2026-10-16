import requests

url = "https://api.open-meteo.com/v1/forecast?latitude=35.68&longitude=139.76&daily=temperature_2m_max&timezone=Asia/Tokyo&forecast_days=1"

response = requests.get(url)


data = response.json()

print(data["daily"]['temperature_2m_max'][0])