from sqlalchemy.orm import Session
from Backend.models.wallet import Wallet
from decimal import Decimal
# Créer un wallet pour un participant
def create_wallet(db: Session, participant_id: int):
    wallet = Wallet(participant_id=participant_id, balance=0)
    db.add(wallet)
    db.commit()
    db.refresh(wallet)
    return wallet

# Voir le solde
def get_wallet(db: Session, participant_id: int):
    return db.query(Wallet).filter(Wallet.participant_id == participant_id).first()

# Ajouter ou dépenser des crédits
# Positif pour ajouter, négatif pour dépenser
def update_wallet(db: Session, participant_id: int, amount: Decimal):
    wallet = get_wallet(db, participant_id)
    if not wallet:
        return None
    if wallet.balance + amount < 0:
        return None  # solde insuffisant
    wallet.balance += amount
    db.commit()
    db.refresh(wallet)
    return wallet
