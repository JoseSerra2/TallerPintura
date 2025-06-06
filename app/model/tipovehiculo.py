from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class TipoVehiculo(Base):
    __tablename__ = "tipovehiculo"

    idTipoVehiculo = Column(Integer, primary_key=True, autoincrement=True)
    NombreTipoVehiculo = Column(String(150), nullable=False)
    CreatedAt = Column(DateTime, server_default=func.now(), nullable=False)
    UpdatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)

    vehiculos_inventarios = relationship("VehiculoInventario", back_populates="tipo_vehiculo")
    precios_servicio = relationship("PrecioServicioVehiculo", back_populates="tipo_vehiculo")
