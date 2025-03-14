from sqlalchemy.orm import Session
from app.model.vehiculoinventario import VehiculoInventario
from app.schema.vehiculoinventario import VehiculoInventarioCreate, VehiculoInventarioUpdate


def create_vehiculoinventario(db: Session, vehiculo_inventario_data: VehiculoInventarioCreate):
    db_vehiculo_inventario = VehiculoInventario(
        CantidadRequerida=vehiculo_inventario_data.CantidadRequerida,
        idTipoVehiculo=vehiculo_inventario_data.idTipoVehiculo,
        idInventario=vehiculo_inventario_data.idInventario
    )
    db.add(db_vehiculo_inventario)
    db.commit()
    db.refresh(db_vehiculo_inventario)
    return db_vehiculo_inventario


def get_vehiculoinventarios(db: Session):
    return db.query(VehiculoInventario).all()


def update_vehiculoinventario(db: Session, idVehiculoInventario: int, vehiculo_inventario_data: VehiculoInventarioUpdate):
    db_vehiculo_inventario = db.query(VehiculoInventario).filter(VehiculoInventario.idVehiculoInventario == idVehiculoInventario).first()
    if db_vehiculo_inventario:
        for key, value in vehiculo_inventario_data.dict(exclude_unset=True).items():
            setattr(db_vehiculo_inventario, key, value)
        db.commit()
        db.refresh(db_vehiculo_inventario)
        return db_vehiculo_inventario
    return None
