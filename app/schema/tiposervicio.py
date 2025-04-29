from pydantic import BaseModel
from decimal import Decimal
from typing import Optional
from datetime import datetime


class TipoServicioSchema(BaseModel):
    idTipoServicio: int
    NombreTipo: str
    idServicio: Optional[int]
    CreatedAt: datetime
    UpdatedAt: datetime
    deleted: Optional[bool] = False  

    class Config:
        orm_mode = True


class TipoServicioCreate(BaseModel):
    NombreTipo: str
    idServicio: Optional[int] = None
    deleted: Optional[bool] = False


class TipoServicioUpdate(BaseModel):
    NombreTipo: Optional[str] = None
    idServicio: Optional[int] = None
    deleted: Optional[bool] = False
