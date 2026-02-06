# app/models/organizer.py
from sqlalchemy import Column, Integer, String
from Backend.database.base import Base
from sqlalchemy.orm import relationship


class Organizer(Base):
    __tablename__ = "organizers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    events = relationship("Event", back_populates="organizer")