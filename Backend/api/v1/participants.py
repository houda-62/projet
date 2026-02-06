from Backend.models.participants import Participant
from Backend.schemas.participants import ParticipantCreate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Backend.database.session import get_db
from Backend.models.event import Event
from Backend.models.organizer import Organizer
from Backend.schemas.participants import ParticipantCreate
from Backend.schemas.participants import ParticipantRead 
from Backend.api.v1.auth import get_current_organizer
from fastapi import Security
import qrcode as qr
import uuid 
#from Backend.schemas.participants import ParticipantUpdate
#from Backend.schemas.participants import ParticipantDelete


router = APIRouter(tags=["participants"])

@router.post("/events/{event_id}/register")
def register_participant(
    event_id: int,
    participant: ParticipantCreate,
    db: Session = Depends(get_db), 
): 
    db_event = db.query(Event).filter_by(id=event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event non trouvé")
    db_participant = Participant(name=participant.name, email=participant.email, event_id=event_id)
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)

    # Génère un ticket_id et QR code dynamique
    ticket_id = str(uuid.uuid4())
    qr_url = f"https://monbackend.com/tickets/validate/{ticket_id}"
    qr_obj = qr.QRCode(version=1, box_size=10, border=4)
    qr_obj.add_data(qr_url)
    qr_obj.make(fit=True)
    img = qr_obj.make_image(fill_color="black", back_color="white")
    qr_filename = f"qrcode_{ticket_id}.png"
    img.save(qr_filename)

    return {
        "participant_id": db_participant.id,
        "ticket_id": ticket_id,
        "qr_code_file": qr_filename,
        "qr_url": qr_url
    }

@router.get("/events/{event_id}/participants")
def list_participants(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: Organizer = Security(get_current_organizer)
):
    db_event = db.query(Event).filter_by(id=event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event non trouvé")
    if db_event.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Vous n'avez pas les permissions pour lister les participants de cet événement")
    return db_event.participants

"""
@router.get("/events/{event_id}/participants")
def list_participants(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: Organizer = Depends(get_current_user)
):
    event = db.query(Event).filter_by(id=event_id, organizer_id=current_user.id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event non trouvé ou pas autorisé")
    return event.participants
"""