from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class ServicioSchema(BaseModel):
    idServicio: int
    NombreServicio: str
    DescripcionServicio: str
    ValidoDev: bool
    CreatedAt: datetime
    UpdatedAt: datetime

    class Config:
        orm_mode = True

class ServicioCreate(BaseModel):
    NombreServicio: str
    DescripcionServicio: str
    ValidoDev: bool

class ServicioUpdate(BaseModel):
    NombreServicio: Optional[str] = None
    DescripcionServicio: Optional[str] = None
    ValidoDev: Optional[bool] = None
