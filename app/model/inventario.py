from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func

class Inventario(Base):
    __tablename__ = "Inventario"

    idInventario = Column(Integer, primary_key=True, autoincrement=True)
    TipoInventario = Column(Integer, nullable=False)  # Cambié el tipo a Integer para que coincida con la tabla
    NombreProducto = Column(String(100), nullable=False)
    idTipoPintura = Column(Integer, ForeignKey("TipoPintura.idTipoPintura"), nullable=True)
    Lote = Column(String(50), nullable=True)  # Lote agregado
    CodigoColor = Column(String(100), nullable=True)
    CantidadDisponible = Column(Integer, nullable = False)
    FechaAdquisicion = Column(Date, nullable=True)  # FechaAdquisicion agregado
    FechaVencimiento = Column(Date, nullable=True)
    EstadoInventario = Column(Boolean, nullable=False)  # EstadoInventario agregado
    CreatedAt = Column(DateTime, server_default=func.now(), nullable=False)
    UpdatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    tipo_pintura = relationship("TipoPintura", back_populates="inventarios")
    vehiculos_inventarios = relationship("VehiculoInventario", back_populates="inventario")
