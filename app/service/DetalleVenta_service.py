from sqlalchemy.orm import Session
from app.model.Detalle_Venta import DetalleVenta
from app.schema.Detalle_Venta import DetalleVentaCreate, DetalleVentaUpdate
from sqlalchemy.sql import func

def crear_detalle(db: Session, detalle: DetalleVentaCreate):
    nuevo_detalle = DetalleVenta(**detalle.dict())
    db.add(nuevo_detalle)
    db.commit()
    db.refresh(nuevo_detalle)
    return nuevo_detalle

def obtener_detalles_por_venta(db: Session, idVenta: int):
    return db.query(DetalleVenta).filter(DetalleVenta.idVenta == idVenta).all()

def actualizar_detalle(db: Session, idDetalleVenta: int, detalle_data: DetalleVentaUpdate):
    detalle = db.query(DetalleVenta).filter(DetalleVenta.idDetalleVenta == idDetalleVenta).first()
    if not detalle:
        return None
    for key, value in detalle_data.dict(exclude_unset=True).items():
        setattr(detalle, key, value)
    detalle.UpdatedAt = func.now()
    db.commit()
    db.refresh(detalle)
    return detalle
