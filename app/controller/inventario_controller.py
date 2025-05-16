from fastapi import APIRouter, Depends, HTTPException, Request
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
    SolicitudCrearInventario,
    SolicitudAumentoInventario,
    InventarioUnion
)
from pydantic import ValidationError

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


@router.post("/pintura/POST/inventarios", response_model=InventarioSchema)
async def manejar_inventario(request: Request, db: Session = Depends(get_db)):
    body = await request.json()

    # Detectar si proviene del servicio de administración
    if "idProducto" in body and "cantidad" in body:
        body = {
            "accion": "aumentar",
            "idInventario": body["idProducto"],
            "cantidad": body["cantidad"],
            "origen": "admin"  # Nota: en el esquema esperas "admin" en minúscula, no "Admin"
        }

    try:
        # Aquí parseamos bien dependiendo del tipo
        if body.get("accion") == "crear":
            data = SolicitudCrearInventario.parse_obj(body)
        elif body.get("accion") == "aumentar":
            data = SolicitudAumentoInventario.parse_obj(body)
        else:
            raise HTTPException(status_code=400, detail="Acción no reconocida")
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())

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
