from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Venta(Base):
    __tablename__ = "venta"

    idVenta = Column(Integer, primary_key=True, autoincrement=True)
    idCliente = Column(Integer, nullable=True)
    noTransaccion = Column(Integer, nullable=True)
    FechaVenta = Column(DateTime, server_default=func.now(), nullable=False)
    TotalVenta = Column(Numeric(10, 2), nullable=False)
    CreatedAt = Column(DateTime, server_default=func.now(), nullable=False)
    UpdatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)
    
    detalles = relationship("DetalleVenta", back_populates="venta", cascade="all, delete-orphan")
