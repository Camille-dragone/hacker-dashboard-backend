from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from . import models  
from .deps import get_db
from .seed import generer_entreprises
from .routers import entreprises, logs, stats

app = FastAPI(title="Hacker Dashboard API 😈")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://hackerdashboard.netlify.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(stats.router)
app.include_router(entreprises.router)
app.include_router(logs.router)

@app.get("/")
def home():
    return {"message": "API Hacker active 😈"}

@app.post("/seed")
def seed_database(nb: int = 100, db: Session = Depends(get_db)):
    generer_entreprises(db, nb)
    return {"message": f"{nb} entreprises fictives créées"}
