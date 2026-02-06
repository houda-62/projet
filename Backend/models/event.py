# app/models/event.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from Backend.database.base import Base
import datetime
from sqlalchemy.orm import relationship

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    location = Column(String, nullable=True)
    currency = Column(String, default="EUR")
    organizer_id = Column(Integer, ForeignKey("organizers.id"))
    organizer = relationship("Organizer", back_populates="events")

    # Relation avec Participant
    participants = relationship("Participant", back_populates="event", cascade="all, delete-orphan")