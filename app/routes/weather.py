import os
from fastapi import APIRouter, HTTPException, Query
from app.services.weather import OpenWeatherService
from app.schemas.weather import WeatherForecast, GoodCyclingDays

router = APIRouter()


@router.get("/forecast", response_model=WeatherForecast)
async def get_forecast(city: str = Query(..., description="City name")):
    if not os.getenv("OPENWEATHER_API_KEY"):
        raise HTTPException(
            status_code=503,
            detail="OpenWeatherMap API key not configured. Please set OPENWEATHER_API_KEY environment variable.",
        )
    
    forecast = await OpenWeatherService.get_forecast(city)
    if not forecast:
        raise HTTPException(
            status_code=404, detail="City not found or API error"
        )
    return forecast


@router.get("/good-days", response_model=GoodCyclingDays)
async def get_good_cycling_days(
    city: str = Query(..., description="City name"),
):
    if not os.getenv("OPENWEATHER_API_KEY"):
        raise HTTPException(
            status_code=503,
            detail="OpenWeatherMap API key not configured. Please set OPENWEATHER_API_KEY environment variable.",
        )
    
    good_days = await OpenWeatherService.get_good_cycling_days(city)
    if not good_days:
        raise HTTPException(
            status_code=404, detail="City not found or API error"
        )
    return good_days

