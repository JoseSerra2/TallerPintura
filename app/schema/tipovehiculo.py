from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TipoVehiculoSchema(BaseModel):
    idTipoVehiculo: int
    NombreTipoVehiculo: str
    CreatedAt: datetime
    UpdatedAt: datetime

    class Config:
        orm_mode = True


class TipoVehiculoCreate(BaseModel):
    NombreTipoVehiculo: str


class TipoVehiculoUpdate(BaseModel):
    NombreTipoVehiculo: Optional[str] = None
