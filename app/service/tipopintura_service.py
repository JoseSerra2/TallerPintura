from sqlalchemy.orm import Session
from app.model.tipopintura import TipoPintura
from app.schema.tipopintura import TipoPinturaCreate, TipoPinturaUpdate


def get_tipopinturas(db: Session):
    return db.query(TipoPintura).all()


def create_tipopintura(db: Session, tipopintura_data: TipoPinturaCreate):
    nuevo_tipopintura = TipoPintura(**tipopintura_data.dict())
    db.add(nuevo_tipopintura)
    db.commit()
    db.refresh(nuevo_tipopintura)
    return nuevo_tipopintura


def update_tipopintura(db: Session, idTipoPintura: int, tipopintura_data: TipoPinturaUpdate):
    tipopintura = db.query(TipoPintura).filter(TipoPintura.idTipoPintura == idTipoPintura).first()
    if not tipopintura:
        return None  
    
    for key, value in tipopintura_data.dict(exclude_unset=True).items():
        setattr(tipopintura, key, value)

    db.commit()
    db.refresh(tipopintura)
    return tipopintura


