from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from ..deps import get_db
from .. import models

router = APIRouter(prefix="/stats", tags=["Statistiques"])

@router.get("/entreprises")
def stats_entreprises(db: Session = Depends(get_db)):
    total = db.query(models.Entreprise).count()

    par_statut = (
        db.query(models.Entreprise.statut, func.count())
        .group_by(models.Entreprise.statut)
        .all()
    )

    par_vulnerabilite = (
        db.query(models.Entreprise.vulnerabilite, func.count())
        .group_by(models.Entreprise.vulnerabilite)
        .all()
    )

    return {
        "total": total,
        "par_statut": {statut: count for statut, count in par_statut},
        "par_vulnerabilite": {vuln: count for vuln, count in par_vulnerabilite},
    }

@router.get("/activite")
def stats_activite(db: Session = Depends(get_db)):
    maintenant = datetime.utcnow()
    derniere_heure = maintenant - timedelta(hours=1)
    dernieres_24h = maintenant - timedelta(hours=24)

    logs_1h = (
        db.query(models.Log)
        .filter(models.Log.created_at >= derniere_heure)
        .count()
    )

    logs_24h = (
        db.query(models.Log)
        .filter(models.Log.created_at >= dernieres_24h)
        .count()
    )

    dernier_log = (
        db.query(models.Log)
        .order_by(models.Log.created_at.desc())
        .first()
    )

    return {
        "logs_derniere_heure": logs_1h,
        "logs_dernieres_24h": logs_24h,
        "dernier_log": {
            "message": dernier_log.message if dernier_log else None,
            "type": dernier_log.type if dernier_log else None,
            "created_at": dernier_log.created_at if dernier_log else None,
        }
    }
