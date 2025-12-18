from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.bike import Bike
from app.schemas.bike import BikeCreate, BikeUpdate, BikeResponse

router = APIRouter()


@router.get("/", response_model=List[BikeResponse])
def get_bikes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bikes = db.query(Bike).offset(skip).limit(limit).all()
    return bikes


@router.get("/{bike_id}", response_model=BikeResponse)
def get_bike(bike_id: int, db: Session = Depends(get_db)):
    bike = db.query(Bike).filter(Bike.id == bike_id).first()
    if not bike:
        raise HTTPException(status_code=404, detail="Bike not found")
    return bike


@router.post("/", response_model=BikeResponse, status_code=201)
def create_bike(bike: BikeCreate, db: Session = Depends(get_db)):
    db_bike = Bike(**bike.model_dump())
    db.add(db_bike)
    db.commit()
    db.refresh(db_bike)
    return db_bike


@router.put("/{bike_id}", response_model=BikeResponse)
def update_bike(bike_id: int, bike_update: BikeUpdate, db: Session = Depends(get_db)):
    bike = db.query(Bike).filter(Bike.id == bike_id).first()
    if not bike:
        raise HTTPException(status_code=404, detail="Bike not found")
    
    update_data = bike_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(bike, field, value)
    
    db.commit()
    db.refresh(bike)
    return bike


@router.delete("/{bike_id}", status_code=204)
def delete_bike(bike_id: int, db: Session = Depends(get_db)):
    bike = db.query(Bike).filter(Bike.id == bike_id).first()
    if not bike:
        raise HTTPException(status_code=404, detail="Bike not found")
    
    db.delete(bike)
    db.commit()
    return None

