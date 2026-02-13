from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import sys
from pathlib import Path

# Add the app directory to Python path for imports
# This allows Backend.* imports to work correctly
app_dir = Path(__file__).parent.parent
if str(app_dir) not in sys.path:
    sys.path.insert(0, str(app_dir))

# Import des routers
# Note: Importing Backend.routers will automatically import Backend,
# which executes Backend/__init__.py to set up the Python path
from Backend.api.v1 import auth
# Import routers modules
import Backend.api.v1.event as events_module
import Backend.api.v1.participants as participants_module 
import Backend.api.v1.wallets as wallets_module
import Backend.api.v1.transactions as transactions_module
#, organizers, events, participants, wallets, transactions
from Backend.database.base import Base 
from Backend.database.session import engine
import Backend.models.organizer  # register Organizer model
import Backend.models.event     # register Event model (if present)
import Backend.models.participants  # register Participant model      
import Backend.models.wallet
import Backend.models.transaction

# Crée l'application FastAPI
app = FastAPI(
    title="My Event App API",
    description="API pour gérer les événements, organisateurs et participants",
    version="1.0.0",
)

# Middleware CORS (optionnel mais souvent nécessaire)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # changer en production pour les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
#app.include_router(organizers.router, prefix="/organizers", tags=["organizers"])
if hasattr(events_module, "router"):
    app.include_router(events_module.router, prefix="/events", tags=["events"])
if hasattr(participants_module, "router"):
    app.include_router(participants_module.router, prefix="/participants", tags=["participants"])
if hasattr(participants_module, "router"):
    app.include_router(wallets_module.router, prefix="/wallets", tags=["wallets"])
if hasattr(transactions_module, "router"):
    app.include_router(transactions_module.router, prefix="/transactions", tags=["transactions"])

# Crée les tables dans la base de données (importe les modèles pour les enregistrer)

Base.metadata.create_all(bind=engine)

# Route racine
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur My Event App API"}


