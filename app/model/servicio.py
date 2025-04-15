from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base
from sqlalchemy.orm import relationship

class Servicio(Base):
    __tablename__ = "Servicio"

    idServicio = Column(Integer, primary_key=True, autoincrement=True)
    NombreServicio = Column(String(100), nullable=False)
    DescripcionServicio = Column(String(150), nullable=False)
    ValidoDev = Column(Boolean, nullable=False)

    tiposervicios = relationship("TipoServicio", back_populates="servicio")  
    detalles = relationship("DetalleVenta", back_populates="servicio", cascade="all, delete-orphan")
