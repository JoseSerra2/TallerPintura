from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.schema.precio_servicio_vehiculo import PrecioServicioVehiculoCreate, PrecioServicioVehiculoResponse
from app.service.psvservice import create_precio_servicio, get_all_precios_servicio, update_precio_servicio

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/pintura/POST/precioservicio", response_model=PrecioServicioVehiculoResponse)
def create(data: PrecioServicioVehiculoCreate, db: Session = Depends(get_db)):
    return create_precio_servicio(db, data)

@router.get("/pintura/GET/precioservicio", response_model=list[PrecioServicioVehiculoResponse])
def get_all(db: Session = Depends(get_db)):
    return get_all_precios_servicio(db)

@router.put("/pintura/PUT/precioservicio/{id}", response_model=PrecioServicioVehiculoResponse)
def update(id: int, data: PrecioServicioVehiculoCreate, db: Session = Depends(get_db)):
    updated = update_precio_servicio(db, id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="PrecioServicioVehiculo no encontrado")
    return updated
