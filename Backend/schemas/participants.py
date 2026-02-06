from pydantic import BaseModel

# Participant
class ParticipantCreate(BaseModel):
    name: str
    email: str

class ParticipantRead(BaseModel):
    id: int
    name: str
    email: str
    event_id: int

    class Config:
        orm_mode = True