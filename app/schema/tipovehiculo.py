from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TipoVehiculoSchema(BaseModel):
    idTipoVehiculo: int
    NombreTipoVehiculo: str
    CreatedAt: datetime
    UpdatedAt: datetime
    deleted: Optional[bool] = False

    class Config:
        orm_mode = True


class TipoVehiculoCreate(BaseModel):
    NombreTipoVehiculo: str
    deleted: Optional[bool] = False


class TipoVehiculoUpdate(BaseModel):
    NombreTipoVehiculo: Optional[str] = None
    deleted: Optional[bool] = False
