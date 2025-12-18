from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class MaintenanceBase(BaseModel):
    service_type: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    cost: Optional[float] = Field(None, ge=0)
    workshop_name: Optional[str] = Field(None, max_length=200)
    workshop_cep: Optional[str] = Field(None, max_length=8)
    workshop_address: Optional[str] = None
    service_date: datetime


class MaintenanceCreate(MaintenanceBase):
    bike_id: int


class MaintenanceUpdate(BaseModel):
    service_type: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    cost: Optional[float] = Field(None, ge=0)
    workshop_name: Optional[str] = Field(None, max_length=200)
    workshop_cep: Optional[str] = Field(None, max_length=8)
    workshop_address: Optional[str] = None
    service_date: Optional[datetime] = None


class MaintenanceResponse(MaintenanceBase):
    id: int
    bike_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

