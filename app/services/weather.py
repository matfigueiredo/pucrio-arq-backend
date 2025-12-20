import httpx
import os
from typing import Optional, List
from datetime import datetime, timedelta
from app.schemas.weather import WeatherDay, WeatherForecast, GoodCyclingDays


class OpenWeatherService:
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    API_KEY = os.getenv("OPENWEATHER_API_KEY")

    @staticmethod
    async def get_forecast(city: str, days: int = 5) -> Optional[WeatherForecast]:
        if not OpenWeatherService.API_KEY:
            print("Warning: OPENWEATHER_API_KEY not set")
            return None

        url = f"{OpenWeatherService.BASE_URL}/forecast"
        params = {
            "q": city,
            "appid": OpenWeatherService.API_KEY,
            "units": "metric",
            "lang": "pt_br",
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                weather_days = []
                processed_dates = set()

                for item in data.get("list", [])[:40]:
                    dt = datetime.fromtimestamp(item["dt"])
                    date_str = dt.strftime("%Y-%m-%d")

                    if date_str in processed_dates:
                        continue

                    if len(weather_days) >= days:
                        break

                    main = item.get("main", {})
                    weather = item.get("weather", [{}])[0]
                    wind = item.get("wind", {})
                    rain = item.get("rain", {})

                    temp = main.get("temp", 0)
                    min_temp = main.get("temp_min", 0)
                    max_temp = main.get("temp_max", 0)
                    humidity = main.get("humidity", 0)
                    wind_speed = wind.get("speed", 0) * 3.6
                    precipitation = rain.get("3h", 0)
                    description = weather.get("description", "")
                    icon = weather.get("icon", "")

                    is_good = OpenWeatherService._is_good_for_cycling(
                        temp, precipitation, wind_speed
                    )

                    weather_day = WeatherDay(
                        date=date_str,
                        temperature=round(temp, 1),
                        min_temp=round(min_temp, 1),
                        max_temp=round(max_temp, 1),
                        humidity=humidity,
                        wind_speed=round(wind_speed, 1),
                        precipitation=round(precipitation, 1),
                        description=description,
                        icon=icon,
                        is_good_for_cycling=is_good,
                    )

                    weather_days.append(weather_day)
                    processed_dates.add(date_str)

                return WeatherForecast(city=city, days=weather_days)

        except Exception as e:
            print(f"Error requesting OpenWeatherMap: {e}")
            return None

    @staticmethod
    def _is_good_for_cycling(
        temperature: float, precipitation: float, wind_speed: float
    ) -> bool:
        temp_ok = 15 <= temperature <= 30
        rain_ok = precipitation < 5.0
        wind_ok = wind_speed < 25.0
        return temp_ok and rain_ok and wind_ok

    @staticmethod
    async def get_good_cycling_days(city: str) -> Optional[GoodCyclingDays]:
        forecast = await OpenWeatherService.get_forecast(city)
        if not forecast:
            return None

        good_days = [day for day in forecast.days if day.is_good_for_cycling]
        return GoodCyclingDays(city=city, good_days=good_days)

