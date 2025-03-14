from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.service.cliente_service import get_clientes, create_cliente, update_cliente
from app.schema.cliente import ClienteSchema, ClienteCreate, ClienteUpdate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/GET/clientes", response_model=List[ClienteSchema])
def listar_clientes(db: Session = Depends(get_db)):
    return get_clientes(db)


@router.post("/POST/clientes", response_model=ClienteSchema)
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    return create_cliente(db, cliente)


@router.put("/PUT/clientes/{idCliente}", response_model=ClienteSchema)
def actualizar_cliente(idCliente: int, cliente_data: ClienteUpdate, db: Session = Depends(get_db)):
    cliente_actualizado = update_cliente(db, idCliente, cliente_data)
    if not cliente_actualizado:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente_actualizado
