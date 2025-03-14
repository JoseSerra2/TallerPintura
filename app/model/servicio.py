from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship

class Servicio(Base):
    __tablename__ = "Servicio"

    idServicio = Column(Integer, primary_key=True, autoincrement=True)
    NombreServicio = Column(String(100), nullable=False)
    DescripcionServicio = Column(String(150), nullable=False)

    tiposervicios = relationship("TipoServicio", back_populates="servicio")  
