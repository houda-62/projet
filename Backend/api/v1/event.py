from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
import datetime
from Backend.database.session import get_db
from Backend.models.event import Event
from Backend.schemas.event import EventCreate, EventRead
from Backend.api.v1.auth import get_current_organizer
from Backend.models.organizer import Organizer

router = APIRouter(tags=["events"], prefix="/events")

@router.post("", response_model=EventRead)
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    current_user: Organizer = Security(get_current_organizer)
):
    db_event = Event(
        name=event.name,
        date=event.date or datetime.datetime.utcnow(),
        location=event.location,
        currency=event.currency, 
        price=event.price,
        organizer_id=current_user.id
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.get("/{event_id}", response_model=EventRead)
def get_event(
    event_id: int, 
    db: Session = Depends(get_db),
    current_user: Organizer = Security(get_current_organizer)
):
    db_event = db.query(Event).filter_by(id=event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event non trouvé")
    if db_event.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Vous n'avez pas les permissions pour accéder à cet événement")
    return db_event

"""
@router.get("/events/{event_id}/participants")
def list_participants(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: Organizer = Depends(get_current_organizer)
):
    event = db.query(Event).filter_by(id=event_id, organizer_id=current_user.id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event non trouvé ou pas autorisé")
    return event.participants
"""