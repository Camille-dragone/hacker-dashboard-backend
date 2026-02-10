from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from datetime import datetime
from .database import Base

class Entreprise(Base):
    __tablename__ = "entreprises"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    pays = Column(String, nullable=False)
    acces = Column(String, nullable=False)         
    vulnerabilite = Column(String, nullable=False)  
    statut = Column(String, nullable=False)       

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    entreprise_id = Column(Integer, ForeignKey("entreprises.id"), nullable=True)

    message = Column(Text, nullable=False)
    type = Column(String, nullable=False) 

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
