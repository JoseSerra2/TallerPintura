from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.service.Devolucion_service import crear_devolucion, obtener_devoluciones
from app.schema.Devolucion import DevolucionCreate, DevolucionResponse
from app.model.Detalle_Venta import DetalleVenta
from app.model.servicio import Servicio
import httpx

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/pintura/GET/devolucion", response_model=List[DevolucionResponse])
def listar_devoluciones(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return obtener_devoluciones(db, skip, limit)

@router.post("/pintura/POST/devolucion", response_model=DevolucionResponse)
def crear_una_devolucion(devolucion: DevolucionCreate, db: Session = Depends(get_db)):
    # Verifica que el detalle de venta exista
    detalle = db.query(DetalleVenta).filter(DetalleVenta.idDetalleVenta == devolucion.idDetalleVenta).first()
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle de venta no encontrado")

    # Verifica si el servicio asociado permite devoluciones
    servicio = db.query(Servicio).filter(Servicio.idServicio == detalle.idServicio).first()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    if not servicio.ValidoDev:
        raise HTTPException(status_code=400, detail="Este servicio no permite devoluciones")

    # Construir payload para servicio de pagos
    payload = {
        "NoTransaccion": str(detalle.venta.noTransaccion),
        "Monto": str(detalle.Subtotal),
        "Descripcion": devolucion.Motivo
    }

    try:
        response = httpx.post("http://localhost:3001/pagos/devoluciones/crear", json=payload)
        response.raise_for_status()
        data = response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error del servicio de pagos: {e.response.text}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"No se pudo contactar al servicio de pagos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado procesando devolución: {str(e)}")

    # Verificar respuesta del servicio de pagos
    if data.get("Mensaje") != "Devolucion realizada correctamente":
        raise HTTPException(status_code=500, detail=f"Devolución rechazada por el servicio de pagos: {data}")

    # Registrar devolución en base de datos
    return crear_devolucion(db, devolucion)
