from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.service.servicio_service import get_servicios, create_servicio, update_servicio
from app.schema.servicio import ServicioSchema, ServicioCreate, ServicioUpdate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/GET/servicios", response_model=List[ServicioSchema])
def listar_servicios(db: Session = Depends(get_db)):
    return get_servicios(db)


@router.post("/POST/servicios", response_model=ServicioSchema)
def crear_servicio(servicio: ServicioCreate, db: Session = Depends(get_db)):
    return create_servicio(db, servicio)


@router.put("/PUT/servicios/{idServicio}", response_model=ServicioSchema)
def actualizar_servicio(idServicio: int, servicio_data: ServicioUpdate, db: Session = Depends(get_db)):
    servicio_actualizado = update_servicio(db, idServicio, servicio_data)
    if not servicio_actualizado:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio_actualizado


