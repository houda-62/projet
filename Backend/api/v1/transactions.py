from decimal import Decimal
from Backend.services import wallet_service as wallet_services
from Backend.models.participant import Participant
from Backend.schemas.participants import ParticipantCreate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Backend.database.session import get_db

router = APIRouter(tags=["transactions"])


@router.post("/participants/{ticket_id}/access")
def grant_access(ticket_id: str, db: Session = Depends(get_db)):
    participant = db.query(Participant).filter_by(ticket_id=ticket_id).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Ticket invalide")

    if participant.access_granted:
        return {"participant_id": participant.id, "access_granted": False, "message": "Déjà entré"}

    participant.access_granted = True
    db.commit()
    return {"participant_id": participant.id, "access_granted": True}


@router.post("/participants/{ticket_id}/pay")
def pay_participant(ticket_id: str, amount: Decimal, db: Session = Depends(get_db)):
    participant = db.query(Participant).filter_by(ticket_id=ticket_id).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant non trouvé")

    wallet = wallet_services.get_wallet(db, participant.id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet non trouvé")

    if wallet.balance < amount:
        raise HTTPException(status_code=400, detail="Solde insuffisant")

    wallet_services.update_wallet(db, participant.id, -amount)
    return {"participant_id": participant.id, "amount_paid": amount, "new_balance": wallet.balance}

@router.get("/participants/{ticket_id}")
def get_participant(ticket_id: str, db: Session = Depends(get_db)):
    participant = db.query(Participant).filter_by(ticket_id=ticket_id).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Ticket invalide")
    wallet = participant.wallet
    return {
        "participant_id": participant.id,
        "name": participant.name,
        "access_granted": participant.access_granted,
        "wallet_balance": wallet.balance if wallet else 0
    }



"""
import stripe
from fastapi import HTTPException

stripe.api_key = "sk_test_ton_cle_secrete"  # mettre dans variables d'environnement en prod

def create_payment_intent(participant_name: str, event_id: int, amount: float, currency: str):
    ""
    Crée un PaymentIntent Stripe pour l'inscription d'un participant
    ""
    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Stripe attend en centimes
            currency=currency.lower(),
            description=f"Inscription {participant_name} pour l'événement {event_id}",
            metadata={"event_id": event_id, "participant_name": participant_name}
        )
        return payment_intent.client_secret
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))

"""
