from sqlalchemy import Column, Integer, ForeignKey, Boolean, Numeric, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class DetalleVenta(Base):
    __tablename__ = "DetalleVenta"

    idDetalleVenta = Column(Integer, primary_key=True, autoincrement=True)
    idVenta = Column(Integer, ForeignKey("Venta.idVenta", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    idServicio = Column(Integer, ForeignKey("Servicio.idServicio", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    Cantidad = Column(Integer, nullable=False)
    Subtotal = Column(Numeric(10, 2), nullable=False)
    Devolucion = Column(Boolean, nullable=False)
    CreatedAt = Column(DateTime, server_default=func.now(), nullable=False)
    UpdatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)


    venta = relationship("Venta", back_populates="detalles")
    servicio = relationship("Servicio", back_populates="detalles")
    devolucion = relationship("Devolucion", back_populates="detalle", uselist=False)

