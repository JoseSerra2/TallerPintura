from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class VentaBase(BaseModel):
    idCliente: Optional[str]
    noTransaccion: int
    TotalVenta: float
    deleted: Optional[bool] = False

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
    idCliente: Optional[str] = None  
    TotalVenta: Optional[float] = None 
    deleted: Optional[bool] = False 

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

class FacturaEmpresa(BaseModel):
    nitEmpresa: str
    nombreEmpresa: str
    telefonoEmpresa: str
    direccionEmpresa: str

class FacturaCliente(BaseModel):
    idCliente: str
    nitCliente: str
    nombreCliente: str
    apellidoCliente: str
    direccionCliente: str

class Factura(BaseModel):
    noFactura: str
    serie: str
    empresa: FacturaEmpresa
    cliente: FacturaCliente
    detalle: List[DetalleProducto]  # <-- Aquí se adapta el campo
    total: float
    totalDescontado: float
    estado: int
    fecha: str
    notasCredito: List[dict]
    createdAt: str
    updatedAt: str

class VentaConPagoRequest(BaseModel):
    Nit: str
    IdCaja: str
    IdServicioTransaccion: str
    factura: Factura
    MetodosPago: List[MetodoPago]
    
class VentaSimpleDetalle(BaseModel):
    Producto: str
    Cantidad: int
    Precio: float
    Descuento: float

class VentaSimpleRequest(BaseModel):
    Nit: str
    IdCaja: str
    IdServicioTransaccion: str
    Detalle: List[VentaSimpleDetalle]
    MetodosPago: List[MetodoPago]