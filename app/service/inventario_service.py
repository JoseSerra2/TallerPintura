from sqlalchemy.orm import Session
from app.model.inventario import Inventario
from app.model.movimiento import Movimiento  # Asegúrate de importar tu modelo Movimiento
from app.schema.inventario import InventarioCreate, InventarioUpdate
from datetime import datetime, timedelta
from fastapi import HTTPException

def get_inventarios(db: Session):
    return db.query(Inventario).all()

def create_inventario(db: Session, inventario_data: InventarioCreate):
    data = inventario_data.dict()
    data.pop("accion", None)
    nuevo_inventario = Inventario(**data)
    db.add(nuevo_inventario)
    db.commit()
    db.refresh(nuevo_inventario)

    # Registrar movimiento de entrada
    movimiento = Movimiento(
        idInventario=nuevo_inventario.idInventario,
        TipoMovimiento="entrada",
        Cantidad=nuevo_inventario.CantidadDisponible,
        FechaMovimiento=datetime.now(),
        deleted=False
    )
    db.add(movimiento)
    db.commit()

    return nuevo_inventario

def update_inventario(db: Session, idInventario: int, inventario_data: InventarioUpdate):
    inventario = db.query(Inventario).filter(Inventario.idInventario == idInventario).first()
    if not inventario:
        return None

    for key, value in inventario_data.dict(exclude_unset=True).items():
        setattr(inventario, key, value)

    db.commit()
    db.refresh(inventario)
    return inventario

def procesar_solicitud_inventario(db: Session, idInventario: int, cantidad: int, origen: str):
    inventario = db.query(Inventario).filter(Inventario.idInventario == idInventario).first()
    if not inventario:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if origen == "admin":
        inventario.CantidadDisponible += cantidad
        db.commit()
        db.refresh(inventario)

        # Registrar movimiento
        movimiento = Movimiento(
            idInventario=inventario.idInventario,
            TipoMovimiento="entrada",
            Cantidad=cantidad,
            FechaMovimiento=datetime.now(),
            deleted=False
        )
        db.add(movimiento)
        db.commit()

        return {
            "mensaje": "Inventario actualizado por administración",
            "inventario": inventario
        }

    elif origen == "pintura":
        return {
            "mensaje": "Solicitud registrada, en espera de aprobación",
            "idInventario": idInventario,
            "cantidadSolicitada": cantidad
        }

    else:
        raise HTTPException(status_code=400, detail="Origen inválido")

def aplicar_descuento_desgaste(db: Session, porcentaje: float = 10.0):
    fecha_corte = datetime.now().date() - timedelta(days=6*30)
    inventarios_antiguos = db.query(Inventario).filter(
        Inventario.FechaAdquisicion <= fecha_corte,
        Inventario.CantidadDisponible > 0
    ).all()

    for inventario in inventarios_antiguos:
        descuento = int(inventario.CantidadDisponible * (porcentaje / 100))
        if descuento > 0:
            inventario.CantidadDisponible -= descuento
            if inventario.CantidadDisponible < 0:
                inventario.CantidadDisponible = 0

    db.commit()
