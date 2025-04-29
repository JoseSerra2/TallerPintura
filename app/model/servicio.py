from sqlalchemy import Column, Integer, String, Boolean ,DateTime
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Servicio(Base):
    __tablename__ = "Servicio"

    idServicio = Column(Integer, primary_key=True, autoincrement=True)
    NombreServicio = Column(String(100), nullable=False)
    DescripcionServicio = Column(String(150), nullable=False)
    ValidoDev = Column(Boolean, nullable=False)
    CreatedAt = Column(DateTime, server_default=func.now(), nullable=False)
    UpdatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)

    tiposervicios = relationship("TipoServicio", back_populates="servicio")  
    detalles = relationship("DetalleVenta", back_populates="servicio", cascade="all, delete-orphan")
