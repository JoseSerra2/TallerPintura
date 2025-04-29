from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MovimientoBase(BaseModel):
    idInventario: Optional[int]
    TipoMovimiento: str
    Cantidad: int
    FechaMovimiento: datetime
    deleted: Optional[bool] = False

class MovimientoCreate(MovimientoBase):
    pass

class MovimientoResponse(MovimientoBase):
    idMovimiento: int
    CreatedAt: datetime
    UpdatedAt: datetime
    deleted: Optional[bool] = False

    class Config:
        from_attributes = True
