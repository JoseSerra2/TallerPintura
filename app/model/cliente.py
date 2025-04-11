from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Cliente(Base):
    __tablename__ = "Cliente"

    idCliente = Column(Integer, primary_key=True, autoincrement=True)
    NitCliente = Column(String(50), unique=True, nullable=False)
    NombreCliente = Column(String(150), nullable=False)
    ApellidoCliente = Column(String(150), nullable=False)
    Telefono = Column(String(20), nullable=False)
    Direccion = Column(String(150), nullable=False)
    CreatedAt = Column(DateTime, server_default=func.now(), nullable=False)
    UpdatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    
    ventas = relationship("Venta", back_populates="cliente")
