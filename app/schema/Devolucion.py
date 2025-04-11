from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DevolucionBase(BaseModel):
    FechaDevolucion: datetime
    Motivo: str
    idDetalleVenta: Optional[int]

class DevolucionCreate(DevolucionBase):
    pass

class DevolucionResponse(DevolucionBase):
    idDevolucion: int
    CreatedAt: datetime
    UpdatedAt: datetime

    class Config:
        from_attributes = True
