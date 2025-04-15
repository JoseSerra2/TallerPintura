from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.service.tipovehiculo_service import get_tipovehiculos, create_tipovehiculo, update_tipovehiculo
from app.schema.tipovehiculo import TipoVehiculoSchema, TipoVehiculoCreate, TipoVehiculoUpdate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/pintura/GET/tipovehiculos", response_model=List[TipoVehiculoSchema])
def listar_tipovehiculos(db: Session = Depends(get_db)):
    return get_tipovehiculos(db)


@router.post("/pintura/POST/tipovehiculos", response_model=TipoVehiculoSchema)
def crear_tipovehiculo(tipovehiculo: TipoVehiculoCreate, db: Session = Depends(get_db)):
    return create_tipovehiculo(db, tipovehiculo)


@router.put("/pintura/PUT/tipovehiculos/{idTipoVehiculo}", response_model=TipoVehiculoSchema)
def actualizar_tipovehiculo(idTipoVehiculo: int, tipovehiculo_data: TipoVehiculoUpdate, db: Session = Depends(get_db)):
    tipovehiculo_actualizado = update_tipovehiculo(db, idTipoVehiculo, tipovehiculo_data)
    if not tipovehiculo_actualizado:
        raise HTTPException(status_code=404, detail="Tipo de Vehículo no encontrado")
    return tipovehiculo_actualizado


