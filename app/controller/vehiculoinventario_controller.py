from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from typing import List
from app.service.vehiculoinventario_service import get_vehiculoinventarios, create_vehiculoinventario, update_vehiculoinventario
from app.schema.vehiculoinventario import VehiculoInventarioSchema, VehiculoInventarioCreate, VehiculoInventarioUpdate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/GET/vehiculoinventarios", response_model=List[VehiculoInventarioSchema])
def listar_vehiculoinventarios(db: Session = Depends(get_db)):
    return get_vehiculoinventarios(db)


@router.post("/POST/vehiculoinventarios", response_model=VehiculoInventarioSchema)
def crear_vehiculoinventario(vehiculo_inventario: VehiculoInventarioCreate, db: Session = Depends(get_db)):
    return create_vehiculoinventario(db, vehiculo_inventario)


@router.put("/PUT/vehiculoinventarios/{idVehiculoInventario}", response_model=VehiculoInventarioSchema)
def actualizar_vehiculoinventario(idVehiculoInventario: int, vehiculo_inventario_data: VehiculoInventarioUpdate, db: Session = Depends(get_db)):
    vehiculo_inventario_actualizado = update_vehiculoinventario(db, idVehiculoInventario, vehiculo_inventario_data)
    if not vehiculo_inventario_actualizado:
        raise HTTPException(status_code=404, detail="Vehículo inventario no encontrado")
    return vehiculo_inventario_actualizado
