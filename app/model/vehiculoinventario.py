from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class VehiculoInventario(Base):
    __tablename__ = "VehiculoInventario"

    idVehiculoInventario = Column(Integer, primary_key=True, index=True)
    CantidadRequerida = Column(Float, nullable=False)
    idTipoVehiculo = Column(Integer, ForeignKey("TipoVehiculo.idTipoVehiculo"), nullable=False)
    idInventario = Column(Integer, ForeignKey("Inventario.idInventario"), nullable=False)

    tipo_vehiculo = relationship("TipoVehiculo", back_populates="vehiculos_inventarios")
    inventario = relationship("Inventario", back_populates="vehiculos_inventarios")
