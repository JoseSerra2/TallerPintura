from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class VehiculoInventarioSchema(BaseModel):
    idVehiculoInventario: int
    CantidadRequerida: float
    idTipoVehiculo: int
    idInventario: int
    CreatedAt: datetime
    UpdatedAt: datetime

    class Config:
        orm_mode = True


class VehiculoInventarioCreate(BaseModel):
    CantidadRequerida: float
    idTipoVehiculo: int
    idInventario: int


class VehiculoInventarioUpdate(BaseModel):
    CantidadRequerida: Optional[float] = None
    idTipoVehiculo: Optional[int] = None
    idInventario: Optional[int] = None
