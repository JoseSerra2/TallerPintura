from sqlalchemy.orm import Session
from app.model.tiposervicio import TipoServicio
from app.schema.tiposervicio import TipoServicioCreate, TipoServicioUpdate


def get_tiposervicios(db: Session):
    return db.query(TipoServicio).all()


def create_tiposervicio(db: Session, tiposervicio_data: TipoServicioCreate):
    nuevo_tiposervicio = TipoServicio(**tiposervicio_data.dict())
    db.add(nuevo_tiposervicio)
    db.commit()
    db.refresh(nuevo_tiposervicio)
    return nuevo_tiposervicio


def update_tiposervicio(db: Session, idTipoServicio: int, tiposervicio_data: TipoServicioUpdate):
    tiposervicio = db.query(TipoServicio).filter(TipoServicio.idTipoServicio == idTipoServicio).first()
    if not tiposervicio:
        return None  

    for key, value in tiposervicio_data.dict(exclude_unset=True).items():
        setattr(tiposervicio, key, value)

    db.commit()
    db.refresh(tiposervicio)
    return tiposervicio
