from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ClienteSchema(BaseModel):
    idCliente: int
    NitCliente: str
    NombreCliente: str
    ApellidoCliente: str
    Telefono: str
    Direccion: str
    CreatedAt: datetime
    UpdatedAt: datetime

    class Config:
        orm_mode = True


class ClienteCreate(BaseModel):
    NitCliente: str
    NombreCliente: str
    ApellidoCliente: str
    Telefono: str
    Direccion: str


class ClienteUpdate(BaseModel):
    NitCliente: Optional[str] = None
    NombreCliente: Optional[str] = None
    ApellidoCliente: Optional[str] = None
    Telefono: Optional[str] = None
    Direccion: Optional[str] = None
