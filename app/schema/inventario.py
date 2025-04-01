from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional


class InventarioSchema(BaseModel):
    idInventario: int
    TipoInventario: int  # TipoInventario como Integer
    NombreProducto: str
    idTipoPintura: Optional[int] = None
    Lote: Optional[str] = None  # Lote es opcional
    CodigoColor: Optional[str] = None
    CantidadDisponible: int  # CantidadDisponible como Integer
    FechaAdquisicion: Optional[date] = None  # FechaAdquisicion es opcional
    FechaVencimiento: Optional[date] = None
    EstadoInventario: bool  # EstadoInventario como Booleano

    class Config:
        orm_mode = True


class InventarioCreate(BaseModel):
    TipoInventario: int
    NombreProducto: str
    idTipoPintura: Optional[int] = None
    Lote: Optional[str] = None
    CodigoColor: Optional[str] = None
    CantidadDisponible: int  # CantidadDisponible es obligatorio para crear el inventario
    FechaAdquisicion: Optional[date] = None
    FechaVencimiento: Optional[date] = None
    EstadoInventario: bool


class InventarioUpdate(BaseModel):
    TipoInventario: Optional[int] = None
    NombreProducto: Optional[str] = None
    idTipoPintura: Optional[int] = None
    Lote: Optional[str] = None
    CodigoColor: Optional[str] = None
    CantidadDisponible: Optional[int] = None  # CantidadDisponible es opcional para actualizar
    FechaAdquisicion: Optional[date] = None
    FechaVencimiento: Optional[date] = None
    EstadoInventario: Optional[bool] = None
