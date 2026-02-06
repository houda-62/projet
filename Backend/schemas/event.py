from pydantic import BaseModel
import datetime
from datetime import datetime
from typing import Optional




# Event
class EventCreate(BaseModel):
    name: str
    #description: str | None = None
    date: Optional[datetime] = None
    location: str | None = None
    currency: str | None = "EUR"
    price: float | None = None 

class EventRead(BaseModel):
    id: int
    name: str
    date: datetime
    location: str | None
    currency: str
    organizer_id: int 
    price: float | None = None 
    class Config:
        orm_mode = True