
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func

class Inventario(Base):
    __tablename__ = "Inventario"

    idInventario = Column(Integer, primary_key=True, autoincrement=True)
    TipoInventario = Column(String(100), nullable=False)
    NombreProducto = Column(String(100), nullable=False)
    CantidadDisponible = Column(Integer, nullable=False)
    CodigoColor = Column(String(100), nullable=True)
    idTipoPintura = Column(Integer, ForeignKey("TipoPintura.idTipoPintura"), nullable=True)
    FechaVencimiento = Column(Date, nullable=True)
    CreatedAt = Column(DateTime, server_default=func.now(), nullable=False)
    UpdatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    tipo_pintura = relationship("TipoPintura", back_populates="inventarios")
    vehiculos_inventarios = relationship("VehiculoInventario", back_populates="inventario")
