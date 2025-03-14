from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class InventarioSchema(BaseModel):
    idInventario: int
    TipoInventario: str
    NombreProducto: str
    CantidadDisponible: int
    CodigoColor: Optional[str]
    idTipoPintura: Optional[int]
    FechaVencimiento: Optional[date]
    CreatedAt: datetime
    UpdatedAt: datetime

    class Config:
        orm_mode = True


class InventarioCreate(BaseModel):
    TipoInventario: str
    NombreProducto: str
    CantidadDisponible: int
    CodigoColor: Optional[str]
    idTipoPintura: Optional[int]
    FechaVencimiento: Optional[date]


class InventarioUpdate(BaseModel):
    TipoInventario: Optional[str] = None
    NombreProducto: Optional[str] = None
    CantidadDisponible: Optional[int] = None
    CodigoColor: Optional[str] = None
    idTipoPintura: Optional[int] = None
    FechaVencimiento: Optional[date] = None
