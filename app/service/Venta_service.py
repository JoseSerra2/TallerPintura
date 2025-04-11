from sqlalchemy.orm import Session
from app.model.Venta import Venta
from app.schema.Venta import VentaCreate
from sqlalchemy.sql import func

def crear_venta(db: Session, venta: VentaCreate):
    nueva_venta = Venta(
        idCliente=venta.idCliente,
        TotalVenta=venta.TotalVenta
    )
    db.add(nueva_venta)
    db.commit()
    db.refresh(nueva_venta)
    return nueva_venta

def obtener_ventas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Venta).offset(skip).limit(limit).all()

def actualizar_venta(db: Session, venta_id: int, venta_actualizada: VentaCreate):
    venta = db.query(Venta).filter(Venta.idVenta == venta_id).first()
    
    if not venta:
        return None
    
    venta.idCliente = venta_actualizada.idCliente
    venta.TotalVenta = venta_actualizada.TotalVenta
    venta.UpdatedAt = func.now()

    db.commit()
    db.refresh(venta)
    return venta

