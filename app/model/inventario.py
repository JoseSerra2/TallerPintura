from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func

class Inventario(Base):
    __tablename__ = "inventario"

    idInventario = Column(Integer, primary_key=True, autoincrement=True)
    TipoInventario = Column(Integer, nullable=False)
    NombreProducto = Column(String(100), nullable=False)
    idTipoPintura = Column(Integer, ForeignKey("tipopintura.idTipoPintura"), nullable=True)
    Lote = Column(String(50), nullable=True)  
    CodigoColor = Column(String(100), nullable=True)
    CantidadDisponible = Column(Integer, nullable=False)
    FechaAdquisicion = Column(Date, nullable=True)
    FechaVencimiento = Column(Date, nullable=True)
    EstadoInventario = Column(Boolean, nullable=False)
    CreatedAt = Column(DateTime, server_default=func.now(), nullable=False)
    UpdatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)

    tipo_pintura = relationship("TipoPintura", back_populates="inventarios")
    vehiculos_inventarios = relationship("VehiculoInventario", back_populates="inventario")
    movimientos = relationship("Movimiento", back_populates="inventario")
