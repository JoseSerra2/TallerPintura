from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TipoPinturaSchema(BaseModel):
    idTipoPintura: int
    NombreTipoPintura: str
    CreatedAt: datetime
    UpdatedAt: datetime
    deleted: Optional[bool] = False

    class Config:
        orm_mode = True


class TipoPinturaCreate(BaseModel):
    NombreTipoPintura: str
    deleted: Optional[bool] = False


class TipoPinturaUpdate(BaseModel):
    NombreTipoPintura: Optional[str] = None
    deleted: Optional[bool] = False
