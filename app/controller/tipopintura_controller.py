from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.service.tipopintura_service import get_tipopinturas, create_tipopintura, update_tipopintura
from app.schema.tipopintura import TipoPinturaSchema, TipoPinturaCreate, TipoPinturaUpdate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/GET/pintura/tipopinturas", response_model=List[TipoPinturaSchema])
def listar_tipopinturas(db: Session = Depends(get_db)):
    return get_tipopinturas(db)


@router.post("/POST/pintura/tipopinturas", response_model=TipoPinturaSchema)
def crear_tipopintura(tipopintura: TipoPinturaCreate, db: Session = Depends(get_db)):
    return create_tipopintura(db, tipopintura)


@router.put("/PUT/pintura/tipopinturas/{idTipoPintura}", response_model=TipoPinturaSchema)
def actualizar_tipopintura(idTipoPintura: int, tipopintura_data: TipoPinturaUpdate, db: Session = Depends(get_db)):
    tipopintura_actualizado = update_tipopintura(db, idTipoPintura, tipopintura_data)
    if not tipopintura_actualizado:
        raise HTTPException(status_code=404, detail="Tipo de Pintura no encontrado")
    return tipopintura_actualizado


