from pydantic import BaseModel
from decimal import Decimal
from typing import Optional
from datetime import datetime


class TipoServicioSchema(BaseModel):
    idTipoServicio: int
    NombreTipo: str
    PrecioBase: Decimal
    idServicio: Optional[int]  

    class Config:
        orm_mode = True


class TipoServicioCreate(BaseModel):
    NombreTipo: str
    PrecioBase: Decimal
    idServicio: Optional[int] = None


class TipoServicioUpdate(BaseModel):
    NombreTipo: Optional[str] = None
    PrecioBase: Optional[Decimal] = None
    idServicio: Optional[int] = None
