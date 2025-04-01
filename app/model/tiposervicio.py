from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from app.database import Base

class TipoServicio(Base):
    __tablename__ = "TipoServicio"

    idTipoServicio = Column(Integer, primary_key=True, autoincrement=True)
    NombreTipo = Column(String(100), nullable=False)
    idServicio = Column(Integer, ForeignKey("Servicio.idServicio", ondelete="SET NULL"), nullable=True)

    servicio = relationship("Servicio", back_populates="tiposervicios")  
