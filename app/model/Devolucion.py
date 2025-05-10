from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Devolucion(Base):
    __tablename__ = "Devolucion"

    idDevolucion = Column(Integer, primary_key=True, autoincrement=True)
    FechaDevolucion = Column(DateTime, nullable=False)
    Motivo = Column(String(200), nullable=False)
    idDetalleVenta = Column(Integer, ForeignKey("DetalleVenta.idDetalleVenta", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    CreatedAt = Column(DateTime, server_default=func.now(), nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)

    detalle = relationship("DetalleVenta", back_populates="devolucion")  # ✅ Relación correcta

