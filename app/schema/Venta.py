from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class VentaBase(BaseModel):
    idCliente: Optional[int]
    TotalVenta: float

class VentaCreate(VentaBase):
    pass

class VentaResponse(VentaBase):
    idVenta: int
    FechaVenta: datetime
    CreatedAt: datetime
    UpdatedAt: datetime

    class Config:
        from_attributes = True

class VentaUpdate(VentaBase):
    idCliente: Optional[int] = None  
    TotalVenta: Optional[float] = None  

    class Config:
        orm_mode = True  
        
class DetalleProducto(BaseModel):
    Producto: str
    Cantidad: int
    Precio: float
    Descuento: float  # en decimal: 0.30 -> 30%

class MetodoPago(BaseModel):
    NoTarjeta: Optional[str]
    IdMetodo: str
    Monto: float
    IdBanco: Optional[str]

class VentaConPagoRequest(BaseModel):
    Nit: str
    IdCaja: str
    IdServicioTransaccion: str
    Detalle: List[DetalleProducto]
    MetodosPago: List[MetodoPago]