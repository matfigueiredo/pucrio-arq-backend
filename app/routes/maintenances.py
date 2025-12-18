from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.maintenance import Maintenance
from app.models.bike import Bike
from app.schemas.maintenance import MaintenanceCreate, MaintenanceUpdate, MaintenanceResponse

router = APIRouter()


@router.get("/", response_model=List[MaintenanceResponse])
def get_maintenances(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    maintenances = db.query(Maintenance).offset(skip).limit(limit).all()
    return maintenances


@router.get("/{maintenance_id}", response_model=MaintenanceResponse)
def get_maintenance(maintenance_id: int, db: Session = Depends(get_db)):
    maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
    if not maintenance:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    return maintenance


@router.get("/bike/{bike_id}", response_model=List[MaintenanceResponse])
def get_maintenances_by_bike(bike_id: int, db: Session = Depends(get_db)):
    bike = db.query(Bike).filter(Bike.id == bike_id).first()
    if not bike:
        raise HTTPException(status_code=404, detail="Bike not found")
    
    maintenances = db.query(Maintenance).filter(Maintenance.bike_id == bike_id).all()
    return maintenances


@router.post("/", response_model=MaintenanceResponse, status_code=201)
def create_maintenance(maintenance: MaintenanceCreate, db: Session = Depends(get_db)):
    bike = db.query(Bike).filter(Bike.id == maintenance.bike_id).first()
    if not bike:
        raise HTTPException(status_code=404, detail="Bike not found")
    
    db_maintenance = Maintenance(**maintenance.model_dump())
    db.add(db_maintenance)
    db.commit()
    db.refresh(db_maintenance)
    return db_maintenance


@router.put("/{maintenance_id}", response_model=MaintenanceResponse)
def update_maintenance(
    maintenance_id: int, 
    maintenance_update: MaintenanceUpdate, 
    db: Session = Depends(get_db)
):
    maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
    if not maintenance:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    
    update_data = maintenance_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(maintenance, field, value)
    
    db.commit()
    db.refresh(maintenance)
    return maintenance


@router.delete("/{maintenance_id}", status_code=204)
def delete_maintenance(maintenance_id: int, db: Session = Depends(get_db)):
    maintenance = db.query(Maintenance).filter(Maintenance.id == maintenance_id).first()
    if not maintenance:
        raise HTTPException(status_code=404, detail="Maintenance not found")
    
    db.delete(maintenance)
    db.commit()
    return None

