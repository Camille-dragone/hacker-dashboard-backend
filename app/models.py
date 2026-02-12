from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

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

    logs = relationship(
        "Log",
        back_populates="entreprise",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)

    entreprise_id = Column(
        Integer,
        ForeignKey("entreprises.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    message = Column(Text, nullable=False)
    type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    entreprise = relationship("Entreprise", back_populates="logs")
