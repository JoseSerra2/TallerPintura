from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class TipoPintura(Base):
    __tablename__ = "tipopintura"

    idTipoPintura = Column(Integer, primary_key=True, autoincrement=True)
    NombreTipoPintura = Column(String(100), nullable=False)
    CreatedAt = Column(DateTime, default=func.now())
    UpdatedAt = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted = Column(Boolean, default=False, nullable=False)

    inventarios = relationship("Inventario", back_populates="tipo_pintura")
