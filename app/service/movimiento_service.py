from sqlalchemy.orm import Session
from app.model.movimiento import Movimiento
from app.schema.movimiento import MovimientoCreate
from sqlalchemy.sql import func

def crear_movimiento(db: Session, movimiento: MovimientoCreate):
    nuevo_movimiento = Movimiento(
        idInventario=movimiento.idInventario,
        TipoMovimiento=movimiento.TipoMovimiento,
        Cantidad=movimiento.Cantidad,
        FechaMovimiento=movimiento.FechaMovimiento
    )
    db.add(nuevo_movimiento)
    db.commit()
    db.refresh(nuevo_movimiento)
    return nuevo_movimiento

def obtener_movimientos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Movimiento).offset(skip).limit(limit).all()

def actualizar_movimiento(db: Session, movimiento_id: int, datos_actualizados: MovimientoCreate):
    movimiento = db.query(Movimiento).filter(Movimiento.idMovimiento == movimiento_id).first()
    if not movimiento:
        return None

    movimiento.idInventario = datos_actualizados.idInventario
    movimiento.TipoMovimiento = datos_actualizados.TipoMovimiento
    movimiento.Cantidad = datos_actualizados.Cantidad
    movimiento.FechaMovimiento = datos_actualizados.FechaMovimiento
    movimiento.UpdatedAt = func.now()

    db.commit()
    db.refresh(movimiento)
    return movimiento
