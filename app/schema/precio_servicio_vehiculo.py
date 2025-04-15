from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PrecioServicioVehiculoBase(BaseModel):
    idTipoServicio: int
    idTipoVehiculo: int
    Precio: float
    CreatedAt: Optional[datetime] = None 
    UpdatedAt: Optional[datetime] = None

class PrecioServicioVehiculoCreate(PrecioServicioVehiculoBase):
    pass

class PrecioServicioVehiculoUpdate(PrecioServicioVehiculoBase):
    Precio: float

class PrecioServicioVehiculoResponse(PrecioServicioVehiculoBase):
    idPrecioServicioVehiculo: int
    CreatedAt: datetime
    UpdatedAt: datetime 

    class Config:
        orm_mode = True
