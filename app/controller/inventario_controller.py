from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app.service.inventario_service import (
    get_inventarios,
    create_inventario,
    update_inventario,
    procesar_solicitud_inventario
)

from app.schema.inventario import (
    InventarioSchema,
    InventarioUpdate,
    InventarioUnion
)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/pintura/GET/inventarios", response_model=List[InventarioSchema])
def listar_inventarios(db: Session = Depends(get_db)):
    return get_inventarios(db)


@router.post("/pintura/POST/inventarios")
def manejar_inventario(data: InventarioUnion, db: Session = Depends(get_db)):
    if data.accion == "crear":
        return create_inventario(db, data)
    elif data.accion == "aumentar":
        return procesar_solicitud_inventario(db, data.idInventario, data.cantidad, data.origen)
    raise HTTPException(status_code=400, detail="Acción no reconocida")


@router.put("/pintura/PUT/inventarios/{idInventario}", response_model=InventarioSchema)
def actualizar_inventario(idInventario: int, inventario_data: InventarioUpdate, db: Session = Depends(get_db)):
    inventario_actualizado = update_inventario(db, idInventario, inventario_data)
    if not inventario_actualizado:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return inventario_actualizado
