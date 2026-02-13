"""from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from Backend.database.base import Base
from sqlalchemy.orm import relationship
import uuid     # pour le QR code (UUID)
from sqlalchemy.dialects.postgresql import UUID  # pour le QR code (UUID)  


ticket_id = Column(
    UUID(as_uuid=True),
    unique=True,
    nullable=False,
    default=uuid.uuid4  # note : pas de lambda
)

class Participant(Base):
    __tablename__ = "participants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"))
    ticket_id = Column(String, unique=True, default=lambda: str(uuid.uuid4())) # pour le QR code
    access_granted = Column(Boolean, default=False) 

    # Relation avec Event
    event = relationship("Event", back_populates="participants")
    wallet = relationship("Wallet", back_populates="participant", uselist=False)
    # Relation with Transaction(s)
    transactions = relationship("Transaction", back_populates="participant", cascade="all, delete-orphan")
"""