from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from Backend.database.base import Base
import uuid


class Participant(Base):
    __tablename__ = "participants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"))
    ticket_id = Column(String, unique=True, default=lambda: str(uuid.uuid4()))  # pour le QR code
    access_granted = Column(Boolean, default=False)

    # Relation avec Event
    event = relationship("Event", back_populates="participants")
    wallet = relationship("Wallet", back_populates="participant", uselist=False)
    # Relation with Transaction(s)
    transactions = relationship("Transaction", back_populates="participant", cascade="all, delete-orphan")

