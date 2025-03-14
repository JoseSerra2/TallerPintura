from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.service.tiposervicio_service import get_tiposervicios, create_tiposervicio, update_tiposervicio
from app.schema.tiposervicio import TipoServicioSchema, TipoServicioCreate, TipoServicioUpdate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/GET/tiposervicios", response_model=List[TipoServicioSchema])
def listar_tiposervicios(db: Session = Depends(get_db)):
    return get_tiposervicios(db)


@router.post("/POST/tiposervicios", response_model=TipoServicioSchema)
def crear_tiposervicio(tiposervicio: TipoServicioCreate, db: Session = Depends(get_db)):
    return create_tiposervicio(db, tiposervicio)


@router.put("/PUT/tiposervicios/{idTipoServicio}", response_model=TipoServicioSchema)
def actualizar_tiposervicio(idTipoServicio: int, tiposervicio_data: TipoServicioUpdate, db: Session = Depends(get_db)):
    tiposervicio_actualizado = update_tiposervicio(db, idTipoServicio, tiposervicio_data)
    if not tiposervicio_actualizado:
        raise HTTPException(status_code=404, detail="Tipo de Servicio no encontrado")
    return tiposervicio_actualizado
