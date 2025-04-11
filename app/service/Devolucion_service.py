from sqlalchemy.orm import Session
from app.model.Devolucion import Devolucion
from app.schema.Devolucion import DevolucionCreate

def crear_devolucion(db: Session, devolucion: DevolucionCreate):
    nueva_devolucion = Devolucion(
        FechaDevolucion=devolucion.FechaDevolucion,
        Motivo=devolucion.Motivo,
        idDetalleVenta=devolucion.idDetalleVenta
    )
    db.add(nueva_devolucion)
    db.commit()
    db.refresh(nueva_devolucion)
    return nueva_devolucion

def obtener_devoluciones(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Devolucion).offset(skip).limit(limit).all()
