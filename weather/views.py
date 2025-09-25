import requests
from django.shortcuts import render
from decouple import config

def weather_view(request):
    city = request.GET.get("city", "Berlin")
    config("OPENWEATHER_API_KEY")

    # 1. Aktuelles Wetter + Koordinaten
    current_url = (
        f"http://api.openweathermap.org/data/2.5/weather?"
        f"q={city}&units=metric&appid={api_key}&lang=de"
    )
    current_res = requests.get(current_url).json()

    if "coord" not in current_res:
        return render(request, "weather.html", {"weather": None})

    lat = current_res["coord"]["lat"]
    lon = current_res["coord"]["lon"]

    weather = {
        "city": current_res["name"],
        "temp": round(current_res["main"]["temp"]),
        "feels_like": round(current_res["main"]["feels_like"]),
        "description": current_res["weather"][0]["description"].capitalize(),
        "wind": round(current_res["wind"]["speed"], 1),
    }

    # 2. 7-Tage Forecast über One Call API
    forecast_url = (
        f"https://api.openweathermap.org/data/3.0/onecall?"
        f"lat={lat}&lon={lon}&exclude=minutely,hourly,alerts&units=metric&appid={api_key}&lang=de"
    )
    forecast_res = requests.get(forecast_url).json()

    forecast = []
    if "daily" in forecast_res:
        for day in forecast_res["daily"][:7]:
            forecast.append({
                "date": day["dt"],  # Unix Timestamp → später formatieren
                "temp_day": round(day["temp"]["day"]),
                "temp_night": round(day["temp"]["night"]),
                "description": day["weather"][0]["description"].capitalize(),
            })

    return render(request, "weather.html", {"weather": weather, "forecast": forecast})

