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

    class Config:
        orm_mode = True

# Pour login
class OrganizerLogin(BaseModel):
    email: EmailStr
    password: str

# Pour token JWT
class Token(BaseModel):
    access_token: str
    token_type: str
