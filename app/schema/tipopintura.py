from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TipoPinturaSchema(BaseModel):
    idTipoPintura: int
    NombreTipoPintura: str
    CreatedAt: datetime
    UpdatedAt: datetime

    class Config:
        orm_mode = True


class TipoPinturaCreate(BaseModel):
    NombreTipoPintura: str


class TipoPinturaUpdate(BaseModel):
    NombreTipoPintura: Optional[str] = None
