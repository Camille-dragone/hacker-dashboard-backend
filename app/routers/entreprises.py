from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from .. import models, schemas
from ..deps import get_db

router = APIRouter(prefix="/entreprises", tags=["Entreprises"])


@router.post("", response_model=schemas.EntrepriseOut)
def creer_entreprise(payload: schemas.EntrepriseCreate, db: Session = Depends(get_db)):
    data = payload.model_dump()
    data["statut"] = payload.statut.value

    entreprise = models.Entreprise(**data)
    db.add(entreprise)
    db.commit()
    db.refresh(entreprise)

    db.add(models.Log(
        entreprise_id=entreprise.id,
        message=f"Nouvelle cible ajoutée : {entreprise.nom}",
        type="succes"
    ))
    db.commit()

    return entreprise


@router.get("", response_model=list[schemas.EntrepriseOut])
def lister_entreprises(
    limit: int = 20,
    offset: int = 0,
    statut: Optional[str] = None,
    pays: Optional[str] = None,
    acces: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Entreprise)

    if statut:
        query = query.filter(models.Entreprise.statut == statut)
    if pays:
        query = query.filter(models.Entreprise.pays == pays)
    if acces:
        query = query.filter(models.Entreprise.acces == acces)

    return (
        query
        .order_by(models.Entreprise.created_at.desc(), models.Entreprise.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


@router.get("/{entreprise_id}", response_model=schemas.EntrepriseOut)
def lire_entreprise(entreprise_id: int, db: Session = Depends(get_db)):
    entreprise = db.get(models.Entreprise, entreprise_id)
    if not entreprise:
        raise HTTPException(status_code=404, detail="Entreprise introuvable")
    return entreprise


@router.put("/{entreprise_id}", response_model=schemas.EntrepriseOut)
def modifier_entreprise(
    entreprise_id: int,
    payload: schemas.EntrepriseCreate,
    db: Session = Depends(get_db)
):
    entreprise = db.get(models.Entreprise, entreprise_id)
    if not entreprise:
        raise HTTPException(status_code=404, detail="Entreprise introuvable")

    entreprise.nom = payload.nom
    entreprise.pays = payload.pays
    entreprise.acces = payload.acces
    entreprise.vulnerabilite = payload.vulnerabilite
    entreprise.statut = payload.statut.value

    db.commit()
    db.refresh(entreprise)

    db.add(models.Log(
        entreprise_id=entreprise.id,
        message=f"Mise à jour de la cible : {entreprise.nom}",
        type="info"
    ))
    db.commit()

    return entreprise


@router.delete("/{entreprise_id}")
def supprimer_entreprise(entreprise_id: int, db: Session = Depends(get_db)):
    entreprise = db.get(models.Entreprise, entreprise_id)
    if not entreprise:
        raise HTTPException(status_code=404, detail="Entreprise introuvable")

    nom = entreprise.nom

    db.query(models.Log).filter(models.Log.entreprise_id == entreprise_id).delete()

    db.delete(entreprise)
    db.commit()

    db.add(models.Log(
        entreprise_id=None,
        message=f"Suppression de la cible : {nom}",
        type="erreur"
    ))
    db.commit()

    return {"message": f"Entreprise {nom} supprimée"}


@router.get("/{entreprise_id}/logs", response_model=list[schemas.LogOut])
def logs_par_entreprise(entreprise_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.Log)
        .filter(models.Log.entreprise_id == entreprise_id)
        .order_by(models.Log.created_at.asc(), models.Log.id.asc())
        .limit(200)
        .all()
    )
