from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func

class TipoServicio(Base):
    __tablename__ = "tiposervicio"

    idTipoServicio = Column(Integer, primary_key=True, autoincrement=True)
    NombreTipo = Column(String(100), nullable=False)
    idServicio = Column(Integer, ForeignKey("servicio.idServicio", ondelete="SET NULL"), nullable=True)
    CreatedAt = Column(DateTime, server_default=func.now(), nullable=False)
    UpdatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)

    servicio = relationship("Servicio", back_populates="tiposervicios")
    precios_servicio = relationship("PrecioServicioVehiculo", back_populates="tipo_servicio")
