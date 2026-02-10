from faker import Faker
from sqlalchemy.orm import Session
from .models import Entreprise, Log
import random
from datetime import datetime, timedelta

fake = Faker("fr_FR")

STATUTS = ["compromis", "analyse", "securise"]
ACCES = ["user", "admin", "root"]
VULNERABILITES = [
    "Injection SQL",
    "XSS",
    "Mot de passe faible",
    "Port ouvert",
    "API non sécurisée"
]

PREFIXES = ["Cyber", "Neo", "Quantum", "Dark", "Nova", "Shadow"]
SUFFIXES = ["Corp", "Systems", "Solutions", "Industries", "Technologies", "Group"]

CINEMA_LOGS = [
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
    "Payload envoyé",
    "Réponse serveur OK",
    "Escalade privilèges...",
    "Session sécurisée",
    "Suppression des traces...",
    "Masquage adresse IP...",
]

def format_duree(secondes: int) -> str:
    m, s = divmod(secondes, 60)
    return f"{m:02d}:{s:02d}"

def random_past_time(hours_back: int = 24) -> datetime:
    """Donne une date répartie sur les dernières X heures."""
    now = datetime.utcnow()
    seconds_back = random.randint(0, hours_back * 3600)
    return now - timedelta(seconds=seconds_back)

def random_recent_time(minutes_back: int = 5) -> datetime:
    """Donne une date dans les dernières X minutes (pour activité récente)."""
    now = datetime.utcnow()
    seconds_back = random.randint(0, minutes_back * 60)
    return now - timedelta(seconds=seconds_back)

def generer_entreprises(db: Session, nb: int = 50):
    entreprises = []

    for _ in range(nb):
        nom_entreprise = f"{random.choice(PREFIXES)} {fake.word().capitalize()} {random.choice(SUFFIXES)}"
        created_at = random_past_time(24)

        e = Entreprise(
            nom=nom_entreprise,
            pays=fake.country(),
            acces=random.choice(ACCES),
            vulnerabilite=random.choice(VULNERABILITES),
            statut=random.choice(STATUTS),
            created_at=created_at
        )
        db.add(e)
        entreprises.append(e)

    db.commit()

    for e in entreprises:

        t0 = random_past_time(24)
        db.add(Log(
            entreprise_id=e.id,
            message=f"Analyse initiale de la cible {e.nom}",
            type="info",
            created_at=t0
        ))

        cinema_count = random.randint(2, 6)
        times = sorted([random_past_time(24) for _ in range(cinema_count)])
        for t in times:
            db.add(Log(
                entreprise_id=e.id,
                message=random.choice(CINEMA_LOGS),
                type="info",
                created_at=t
            ))

        t_dl = random_past_time(24)
        duree = random.randint(6, 18)
        taille_mo = random.randint(120, 900)
        progressions = [12, 34, 67, 100]

        db.add(Log(
            entreprise_id=e.id,
            message="Téléchargement données...",
            type="info",
            created_at=t_dl
        ))

        for i, p in enumerate(progressions):
            eta = max(0, duree - int(duree * (p / 100)))
            db.add(Log(
                entreprise_id=e.id,
                message=f"Téléchargement données… {p}% ({taille_mo} Mo) ETA {format_duree(eta)}",
                type="info",
                created_at=t_dl + timedelta(seconds=i + 1)
            ))

        db.add(Log(
            entreprise_id=e.id,
            message=f"Téléchargement terminé en {format_duree(duree)} ({taille_mo} Mo)",
            type="succes",
            created_at=t_dl + timedelta(seconds=len(progressions) + 2)
        ))

    db.commit()

    burst = random.randint(15, 30)
    for _ in range(burst):
        e = random.choice(entreprises)
        t = random_recent_time(5)
        db.add(Log(
            entreprise_id=e.id,
            message=random.choice(CINEMA_LOGS),
            type="info",
            created_at=t
        ))
    db.commit()
