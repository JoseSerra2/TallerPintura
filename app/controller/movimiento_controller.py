from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.service.movimiento_service import crear_movimiento, obtener_movimientos
from app.schema.movimiento import MovimientoCreate, MovimientoResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/pintura/GET/movimiento", response_model=List[MovimientoResponse])
def listar_movimientos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return obtener_movimientos(db, skip, limit)

@router.post("/pintura/POST/movimiento", response_model=MovimientoResponse)
def crear_un_movimiento(movimiento: MovimientoCreate, db: Session = Depends(get_db)):
    return crear_movimiento(db, movimiento)

@router.put("/pintura/PUT/movimiento/{movimiento_id}", response_model=MovimientoResponse)
def actualizar_un_movimiento(movimiento_id: int, movimiento: MovimientoCreate, db: Session = Depends(get_db)):
    movimiento_actualizado = actualizar_movimiento(db, movimiento_id, movimiento)
    if not movimiento_actualizado:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    return movimiento_actualizado
