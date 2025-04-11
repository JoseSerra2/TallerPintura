from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class TipoPintura(Base):
    __tablename__ = "TipoPintura"

    idTipoPintura = Column(Integer, primary_key=True, autoincrement=True)
    NombreTipoPintura = Column(String(100), nullable=False)
    CreatedAt = Column(DateTime, default=func.now())
    UpdatedAt = Column(DateTime, default=func.now(), onupdate=func.now())

    inventarios = relationship("Inventario", back_populates="tipo_pintura")
