from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class WeatherDay(BaseModel):
    date: str
    temperature: float
    min_temp: float
    max_temp: float
    humidity: int
    wind_speed: float
    precipitation: float
    description: str
    icon: str
    is_good_for_cycling: bool


class WeatherForecast(BaseModel):
    city: str
    days: List[WeatherDay]


class GoodCyclingDays(BaseModel):
    city: str
    good_days: List[WeatherDay]

