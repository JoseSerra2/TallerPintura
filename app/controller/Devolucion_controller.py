from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.service.Devolucion_service import crear_devolucion, obtener_devoluciones
from app.schema.Devolucion import DevolucionCreate, DevolucionResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/GET/pintura/devolucion", response_model=List[DevolucionResponse])
def listar_devoluciones(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return obtener_devoluciones(db, skip, limit)

@router.post("/POST/pintura/devolucion", response_model=DevolucionResponse)
def crear_una_devolucion(devolucion: DevolucionCreate, db: Session = Depends(get_db)):
    return crear_devolucion(db, devolucion)
