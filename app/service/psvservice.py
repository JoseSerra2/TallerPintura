from sqlalchemy.orm import Session
from app.model.precio_servicio_vehiculo import PrecioServicioVehiculo
from app.schema.precio_servicio_vehiculo import PrecioServicioVehiculoCreate

def create_precio_servicio(db: Session, data: PrecioServicioVehiculoCreate):
    nuevo_precio = PrecioServicioVehiculo(**data.dict())
    db.add(nuevo_precio)
    db.commit()
    db.refresh(nuevo_precio)
    return nuevo_precio

def get_all_precios_servicio(db: Session):
    return db.query(PrecioServicioVehiculo).all()

def update_precio_servicio(db: Session, id: int, data: PrecioServicioVehiculoCreate):
    precio = db.query(PrecioServicioVehiculo).filter(PrecioServicioVehiculo.idPrecioServicioVehiculo == id).first()
    if not precio:
        return None

    for key, value in data.dict().items():
        setattr(precio, key, value)

    db.commit()
    db.refresh(precio)
    return precio
