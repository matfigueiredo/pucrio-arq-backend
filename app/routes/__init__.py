from fastapi import APIRouter
from .bikes import router as bikes_router
from .maintenances import router as maintenances_router
from .address import router as address_router
from .auth import router as auth_router
from .weather import router as weather_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(bikes_router, prefix="/bikes", tags=["bikes"])
api_router.include_router(
    maintenances_router, prefix="/maintenances", tags=["maintenances"]
)
api_router.include_router(address_router, prefix="/address", tags=["address"])
api_router.include_router(weather_router, prefix="/weather", tags=["weather"])

