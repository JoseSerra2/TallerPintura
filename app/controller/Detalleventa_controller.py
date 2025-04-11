from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.service.DetalleVenta_service import crear_detalle, obtener_detalles_por_venta, actualizar_detalle
from app.schema.Detalle_Venta import DetalleVentaCreate, DetalleVentaUpdate, DetalleVentaResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/POST/pintura/detalleventas", response_model=DetalleVentaResponse)
def crear_un_detalle(detalle: DetalleVentaCreate, db: Session = Depends(get_db)):
    return crear_detalle(db, detalle)

@router.get("/GET/pintura/detalleventas/{idVenta}", response_model=List[DetalleVentaResponse])
def listar_detalles_por_venta(idVenta: int, db: Session = Depends(get_db)):
    detalles = obtener_detalles_por_venta(db, idVenta)
    if not detalles:
        raise HTTPException(status_code=404, detail="No se encontraron detalles para esta venta")
    return detalles

@router.put("/PUT/pintura/detalleventas/{idDetalleVenta}", response_model=DetalleVentaResponse)
def actualizar_un_detalle(idDetalleVenta: int, detalle: DetalleVentaUpdate, db: Session = Depends(get_db)):
    actualizado = actualizar_detalle(db, idDetalleVenta, detalle)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return actualizado
