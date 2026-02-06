# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import cast
import jwt, datetime
from Backend.database.session import get_db
from Backend.models.organizer import Organizer
from Backend.schemas.schemas import OrganizerCreate, OrganizerRead, OrganizerLogin, Token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Security
import logging


SECRET_KEY = "CHANGE_ME"  # à mettre dans config.py

# Use bcrypt_sha256 to avoid bcrypt's 72-byte password limit
pwd_context = CryptContext(schemes=["argon2","bcrypt_sha256","bcrypt"], deprecated="auto")
#pwd_context = CryptContext(schemes=["bcrypt_sha256", "bcrypt"], deprecated="auto")
router = APIRouter()

# Inscription
@router.post("/register", response_model=OrganizerRead)
def register_organizer(data: OrganizerCreate, db: Session = Depends(get_db)):
    existing = db.query(Organizer).filter_by(email=data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email ou mot de passe incorrect")
    try:
        # Force bcrypt_sha256 scheme to avoid bcrypt 72-byte limit
        hashed = pwd_context.hash(data.password)
    except Exception:
        logging.exception("Error hashing password for organizer %s", data.email)
        raise
    organizer = Organizer(name=data.name, email=data.email, password_hash=hashed)
    db.add(organizer)
    db.commit()
    db.refresh(organizer)
    return organizer

# Login (OAuth2 form)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    organizer = db.query(Organizer).filter_by(email=form_data.username).first()
    if not organizer or not pwd_context.verify(form_data.password, cast(str, organizer.password_hash)):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

    payload = {
        "organizer_id": organizer.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}

def get_current_organizer(token: str = Security(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        organizer_id = payload.get("organizer_id")
        organizer = db.query(Organizer).get(organizer_id)
        if organizer is None:
            raise HTTPException(status_code=401, detail="Organisateur non trouvé")
        return organizer
    except Exception:
        raise HTTPException(status_code=401, detail="Token invalide")
