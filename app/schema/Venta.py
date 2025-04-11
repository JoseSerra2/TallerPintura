from pydantic import BaseModel
from datetime import datetime
from typing import Optional

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
