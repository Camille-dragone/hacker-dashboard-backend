from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta
import random

from .. import models, schemas
from ..deps import get_db

router = APIRouter(prefix="/logs", tags=["Logs"])


@router.get("", response_model=list[schemas.LogOut])
def lister_logs(
    limit: int = 50,
    since_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Log)

    if since_id is not None:
        query = query.filter(models.Log.id > since_id)

    return (
        query
        .order_by(models.Log.created_at.desc(), models.Log.id.desc())
        .limit(limit)
        .all()
    )


@router.post("/cinema")
def lancer_sequence_cinema(
    entreprise_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    if entreprise_id is not None:
        entreprise = (
            db.query(models.Entreprise)
            .filter(
                models.Entreprise.id == entreprise_id,
                models.Entreprise.statut == "analyse",
            )
            .first()
        )
    else:
        entreprise = (
            db.query(models.Entreprise)
            .filter(models.Entreprise.statut == "analyse")
            .order_by(models.Entreprise.id.desc())
            .first()
        )

    if not entreprise:
        return {"message": "Aucune entreprise en analyse. Lance /seed ou change le statut."}

    lignes = [
        "Initialisation du module darknet...",
        "Chargement des clés AES...",
        "Connexion au réseau TOR...",
        "Proxy actif 127.0.0.1",
        "Scan des ports...",
        "Port 21 ouvert",
        "Port 22 ouvert",
        "Port 80 ouvert",
        "Analyse des vulnérabilités...",
        "CVE-2023-1142 détecté",
        "Injection SQL...",
        "Payload envoyé",
        "Réponse serveur OK",
        "Bypass authentification...",
        "Escalade privilèges...",
        "Accès root obtenu",
        "Téléchargement données...",
    ]

    taille_mo = random.randint(120, 900)
    duree = random.randint(8, 22)
    progressions = [12, 34, 67, 100]

    def format_duree(secondes: int) -> str:
        m, s = divmod(secondes, 60)
        return f"{m:02d}:{s:02d}"

    maintenant = datetime.utcnow()
    t = maintenant
    last_log_id = None

    def add_log(message: str, type_: str = "info", delta_min=0.25, delta_max=0.75):
        nonlocal t, last_log_id
        t = t + timedelta(seconds=random.uniform(delta_min, delta_max))
        log = models.Log(
            entreprise_id=entreprise.id,
            message=message,
            type=type_,
            created_at=t
        )
        db.add(log)
        db.flush()
        last_log_id = log.id

    for line in lignes:
        add_log(f"> {line}", "info")

    for p in progressions:
        eta = max(0, duree - int(duree * (p / 100)))
        add_log(f"> {p}%... ({taille_mo} Mo) ETA {format_duree(eta)}", "info", 0.4, 0.9)

    add_log(f"> 100% terminé — durée {format_duree(duree)} ({taille_mo} Mo)", "succes", 0.6, 1.2)

    fin = [
        "Suppression des traces...",
        "Masquage adresse IP...",
        "Session sécurisée"
    ]
    for line in fin:
        add_log(f"> {line}", "info", 0.4, 1.0)

    entreprise.statut = "compromis"
    add_log("> STATUS ▸ Cible hackée.", "succes", 0.15, 0.35)

    db.commit()

    return {
        "message": "Séquence cinéma injectée",
        "entreprise_id": entreprise.id,
        "dernier_log_id": last_log_id
    }
