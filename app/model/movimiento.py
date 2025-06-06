from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship

class Movimiento(Base):
    __tablename__ = "movimiento"

    idMovimiento = Column(Integer, primary_key=True, autoincrement=True)
    idInventario = Column(Integer, ForeignKey("inventario.idInventario", ondelete="SET NULL"), nullable=True)
    TipoMovimiento = Column(String(100), nullable=False)
    Cantidad = Column(Integer, nullable=False)
    FechaMovimiento = Column(DateTime, nullable=False)
    CreatedAt = Column(DateTime, server_default=func.now(), nullable=False)
    UpdatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)

    inventario = relationship("Inventario", back_populates="movimientos", lazy="joined")
