from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.service.inventario_service import get_inventarios, create_inventario, update_inventario
from app.schema.inventario import InventarioSchema, InventarioCreate, InventarioUpdate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/GET/pintura/inventarios", response_model=List[InventarioSchema])
def listar_inventarios(db: Session = Depends(get_db)):
    return get_inventarios(db)


@router.post("/POST/pintura/inventarios", response_model=InventarioSchema)
def crear_inventario(inventario: InventarioCreate, db: Session = Depends(get_db)):
    return create_inventario(db, inventario)


@router.put("/PUT/inventarios/{idInventario}", response_model=InventarioSchema)
def actualizar_inventario(idInventario: int, inventario_data: InventarioUpdate, db: Session = Depends(get_db)):
    inventario_actualizado = update_inventario(db, idInventario, inventario_data)
    if not inventario_actualizado:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return inventario_actualizado
