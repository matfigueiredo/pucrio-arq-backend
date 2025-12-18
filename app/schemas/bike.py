from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class BikeBase(BaseModel):
    brand: str = Field(..., min_length=1, max_length=100)
    model: str = Field(..., min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=1900, le=2100)
    color: Optional[str] = Field(None, max_length=50)


class BikeCreate(BikeBase):
    pass


class BikeUpdate(BaseModel):
    brand: Optional[str] = Field(None, min_length=1, max_length=100)
    model: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=1900, le=2100)
    color: Optional[str] = Field(None, max_length=50)


class BikeResponse(BikeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

