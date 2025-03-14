from sqlalchemy.orm import Session
from app.model.inventario import Inventario
from app.schema.inventario import InventarioCreate, InventarioUpdate


def get_inventarios(db: Session):
    return db.query(Inventario).all()


def create_inventario(db: Session, inventario_data: InventarioCreate):
    nuevo_inventario = Inventario(**inventario_data.dict())
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
