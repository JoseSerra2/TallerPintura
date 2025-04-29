from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PrecioServicioVehiculoBase(BaseModel):
    idTipoServicio: int
    idTipoVehiculo: int
    Precio: float
    CreatedAt: Optional[datetime] = None 
    UpdatedAt: Optional[datetime] = None
    deleted: Optional[bool] = False

class PrecioServicioVehiculoCreate(PrecioServicioVehiculoBase):
    pass

class PrecioServicioVehiculoUpdate(PrecioServicioVehiculoBase):
    Precio: float
    deleted: Optional[bool] = False

class PrecioServicioVehiculoResponse(PrecioServicioVehiculoBase):
    idPrecioServicioVehiculo: int
    CreatedAt: datetime
    UpdatedAt: datetime 
    deleted: Optional[bool] = False

    class Config:
        orm_mode = True
