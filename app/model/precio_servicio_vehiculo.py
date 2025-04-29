from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class PrecioServicioVehiculo(Base):
    __tablename__ = "precioserviciovehiculo"

    idPrecioServicioVehiculo = Column(Integer, primary_key=True, index=True)
    idTipoServicio = Column(Integer, ForeignKey("TipoServicio.idTipoServicio"), nullable=False)
    idTipoVehiculo = Column(Integer, ForeignKey("TipoVehiculo.idTipoVehiculo"), nullable=False)
    Precio = Column(DECIMAL(10, 2), nullable=False)
    CreatedAt = Column(DateTime, server_default=func.now())
    UpdatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted = Column(Boolean, default=False, nullable=False)

    tipo_servicio = relationship("TipoServicio", back_populates="precios_servicio")
    tipo_vehiculo = relationship("TipoVehiculo", back_populates="precios_servicio")
