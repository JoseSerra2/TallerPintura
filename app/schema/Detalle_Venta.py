from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DetalleVentaBase(BaseModel):
    idVenta: int
    idServicio: int
    Cantidad: int
    Subtotal: float
    Devolucion: bool

class DetalleVentaCreate(DetalleVentaBase):
    pass

class DetalleVentaUpdate(BaseModel):
    Cantidad: Optional[int] = None
    Subtotal: Optional[float] = None
    Devolucion: Optional[bool] = None

class DetalleVentaResponse(DetalleVentaBase):
    idDetalleVenta: int
    CreatedAt: datetime
    UpdatedAt: datetime

    class Config:
        from_attributes = True
