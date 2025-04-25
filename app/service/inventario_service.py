from sqlalchemy.orm import Session
from app.model.inventario import Inventario
from app.schema.inventario import InventarioCreate, InventarioUpdate


def get_inventarios(db: Session):
    return db.query(Inventario).all()


def create_inventario(db: Session, inventario_data: InventarioCreate):
    data = inventario_data.dict()
    data.pop("accion", None)  # <-- elimina "accion" si viene en el dict
    nuevo_inventario = Inventario(**data)
    db.add(nuevo_inventario)
    db.commit()
    db.refresh(nuevo_inventario)
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
        return {
            "mensaje": "Inventario actualizado por administración",
            "inventario": inventario
        }

    elif origen == "pintura":
        # Simulamos guardar la solicitud (en real se guardaría en una tabla aparte o se notifica)
        return {
            "mensaje": "Solicitud registrada, en espera de aprobación",
            "idInventario": idInventario,
            "cantidadSolicitada": cantidad
        }

    else:
        raise HTTPException(status_code=400, detail="Origen inválido")