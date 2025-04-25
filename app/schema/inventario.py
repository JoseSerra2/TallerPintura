from pydantic import BaseModel
from datetime import date
from typing import Optional, Literal, Union


# ----------- MODELOS BASE -----------
class InventarioSchema(BaseModel):
    idInventario: int
    TipoInventario: int
    NombreProducto: str
    idTipoPintura: Optional[int] = None
    Lote: Optional[str] = None
    CodigoColor: Optional[str] = None
    CantidadDisponible: int
    FechaAdquisicion: Optional[date] = None
    FechaVencimiento: Optional[date] = None
    EstadoInventario: bool

    class Config:
        orm_mode = True


class InventarioCreate(BaseModel):
    TipoInventario: int
    NombreProducto: str
    idTipoPintura: Optional[int] = None
    Lote: Optional[str] = None
    CodigoColor: Optional[str] = None
    CantidadDisponible: int
    FechaAdquisicion: Optional[date] = None
    FechaVencimiento: Optional[date] = None
    EstadoInventario: bool


class InventarioUpdate(BaseModel):
    TipoInventario: Optional[int] = None
    NombreProducto: Optional[str] = None
    idTipoPintura: Optional[int] = None
    Lote: Optional[str] = None
    CodigoColor: Optional[str] = None
    CantidadDisponible: Optional[int] = None
    FechaAdquisicion: Optional[date] = None
    FechaVencimiento: Optional[date] = None
    EstadoInventario: Optional[bool] = None


# ----------- SOLICITUD DE INVENTARIO Y ACCIONES -----------

class AccionBase(BaseModel):
    accion: Literal["crear", "aumentar"]


class SolicitudCrearInventario(InventarioCreate, AccionBase):
    accion: Literal["crear"]


class SolicitudAumentoInventario(AccionBase):
    accion: Literal["aumentar"]
    idInventario: int
    cantidad: int
    origen: Literal["pintura", "admin"]


InventarioUnion = Union[SolicitudCrearInventario, SolicitudAumentoInventario]
