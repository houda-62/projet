from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from Backend.database.base import Base

class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, index=True)
    participant_id = Column(Integer, ForeignKey("participants.id"))
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String, default="pending")  # pending, success, failed
    created_at = Column(DateTime, default=datetime.utcnow)

    participant = relationship("Participant", back_populates="transactions")
