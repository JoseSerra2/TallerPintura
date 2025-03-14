from sqlalchemy.orm import Session
from app.model.servicio import Servicio
from app.schema.servicio import ServicioCreate, ServicioUpdate


def get_servicios(db: Session):
    return db.query(Servicio).all()


def create_servicio(db: Session, servicio_data: ServicioCreate):
    nuevo_servicio = Servicio(**servicio_data.dict())  
    db.add(nuevo_servicio)
    db.commit()
    db.refresh(nuevo_servicio)
    return nuevo_servicio


def update_servicio(db: Session, idServicio: int, servicio_data: ServicioUpdate):
    servicio = db.query(Servicio).filter(Servicio.idServicio == idServicio).first()
    if not servicio:
        return None  
    
    for key, value in servicio_data.dict(exclude_unset=True).items():
        setattr(servicio, key, value)

    db.commit()
    db.refresh(servicio)
    return servicio


