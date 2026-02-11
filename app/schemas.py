from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum


class StatutEntreprise(str, Enum):
    cible = "cible"
    compromis = "compromis"
    analyse = "analyse"
    securise = "securise"


class EntrepriseCreate(BaseModel):
    nom: str
    pays: str
    acces: str
    vulnerabilite: str
    statut: StatutEntreprise


class EntrepriseOut(EntrepriseCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LogCreate(BaseModel):
    entreprise_id: Optional[int] = None
    message: str
    type: str


class LogOut(LogCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
