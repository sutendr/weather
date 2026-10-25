import requests

url = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODE = {0 : "快晴" , 1 : "晴れ" , 2 : "一部曇り" , 3 : "曇り" , 45 : "霧" ,48 : "霧氷" ,  51 : "弱い霧雨" , 53 : "霧雨" , 55 : "強い霧雨" , 61 : "小雨" , 63 : "雨" , 65 : "強い雨" , 71 : "小雪" , 73 : "雪" , 75 : "大雪" , 80 : "弱いにわか雨" , 81 : "にわか雨" , 82 : "激しいにわか雨" , 95 : "雷雨"}
RAIN_THRESHOLD = 50

def fetch_weather():
    params = {"latitude" : 35.68 , "longitude" :139.76 , "daily" : ["temperature_2m_max" , "temperature_2m_min" , "precipitation_probability_max" , "weather_code"] , "hourly" : ["precipitation_probability"] , "timezone" : "Asia/Tokyo" , "forecast_days" :1}
    response = requests.get(url, params=params)
    data = response.json()
    return data

def get_rain_hours(times,probs,threshold):
    rain_hours = []
    for i in range(len(times)):
        if probs[i] >= threshold:
            rain_hours.append(f"{times[i][11:]} {probs[i]}%")
    return rain_hours

def main():
    data = fetch_weather()
    daily = data["daily"]
    hourly = data["hourly"]
    times = hourly["time"]
    probs = hourly["precipitation_probability"]
    max_temp = daily["temperature_2m_max"][0]
    min_temp = daily["temperature_2m_min"][0]
    rain = daily["precipitation_probability_max"][0]
    code = daily["weather_code"][0]

    weather = WEATHER_CODE.get(code, "不明")

    print(f"{daily['time'][0]} 東京：最高気温 {max_temp}℃ /最低気温 {min_temp}℃ /降水確率{rain}% /天気：{weather}")

    rain_hours = get_rain_hours(times, probs, RAIN_THRESHOLD)

    for hour in rain_hours:
        print(hour)


if __name__ == "__main__":
    main()