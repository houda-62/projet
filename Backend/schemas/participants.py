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

    # Pydantic v2: enable reading attributes from ORM objects
    model_config = {"from_attributes": True}