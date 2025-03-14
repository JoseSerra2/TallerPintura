from sqlalchemy.orm import Session
from app.model.tipovehiculo import TipoVehiculo
from app.schema.tipovehiculo import TipoVehiculoCreate, TipoVehiculoUpdate


def get_tipovehiculos(db: Session):
    return db.query(TipoVehiculo).all()


def create_tipovehiculo(db: Session, tipovehiculo_data: TipoVehiculoCreate):
    nuevo_tipovehiculo = TipoVehiculo(**tipovehiculo_data.dict())
    db.add(nuevo_tipovehiculo)
    db.commit()
    db.refresh(nuevo_tipovehiculo)
    return nuevo_tipovehiculo


def update_tipovehiculo(db: Session, idTipoVehiculo: int, tipovehiculo_data: TipoVehiculoUpdate):
    tipovehiculo = db.query(TipoVehiculo).filter(TipoVehiculo.idTipoVehiculo == idTipoVehiculo).first()
    if not tipovehiculo:
        return None  
    
    for key, value in tipovehiculo_data.dict(exclude_unset=True).items():
        setattr(tipovehiculo, key, value)

    db.commit()
    db.refresh(tipovehiculo)
    return tipovehiculo


