from Backend.schemas.wallet import WalletResponse, WalletUpdate
from Backend.services import wallet_service as wallet_crud
from Backend.models.event import Event
from Backend.models.participant import Participant
from Backend.schemas.participants import ParticipantCreate
from Backend.schemas.participants import ParticipantRead
from Backend.database.session import get_db
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session  

router = APIRouter(tags=["wallets"])

# Créer un wallet lors de l'inscription
@router.post("/events/{event_id}/register", response_model=ParticipantRead)
def register_participant(event_id: int, participant: ParticipantCreate, db: Session = Depends(get_db)):
    db_event = db.query(Event).filter_by(id=event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event non trouvé")
    
    db_participant = Participant(name=participant.name, email=participant.email, event_id=event_id)
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)

    # Créer un wallet pour le participant
    wallet_crud.create_wallet(db, db_participant.id)

    return db_participant

# Voir le solde
@router.get("/participants/{participant_id}/wallet", response_model=WalletResponse)
def get_wallet_balance(participant_id: int, db: Session = Depends(get_db)):
    wallet = wallet_crud.get_wallet(db, participant_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet non trouvé")
    return wallet

# Ajouter ou dépenser des crédits
@router.post("/participants/{participant_id}/wallet", response_model=WalletResponse)
def modify_wallet(participant_id: int, update: WalletUpdate, db: Session = Depends(get_db)):
    wallet = wallet_crud.update_wallet(db, participant_id, update.amount)
    if not wallet:
        raise HTTPException(status_code=400, detail="Solde insuffisant ou wallet introuvable")
    return wallet
