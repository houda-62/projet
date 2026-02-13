# app/schemas.py
from pydantic import BaseModel, EmailStr

# Pour inscription
class OrganizerCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# Pour réponse API
class OrganizerRead(BaseModel):
    id: int
    name: str
    email: EmailStr

    # Pydantic v2: use model_config to enable reading from ORM objects
    model_config = {"from_attributes": True}

# Pour login
class OrganizerLogin(BaseModel):
    email: EmailStr
    password: str

# Pour token JWT
class Token(BaseModel):
    access_token: str
    token_type: str
