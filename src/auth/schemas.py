from pydantic import BaseModel, EmailStr, Field, constr
from typing import Set

class Token(BaseModel):
    access_token: str
    token_type: str

class Login(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserProfile(BaseModel):
    email: str
    first_name: str
    last_name: str
    photo: str

    class Config:
        orm_mode = True

class User(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    photo: str
    state: str
    password: str

    class Config:
        orm_mode = True

class UpdateUserProfile(BaseModel):
    first_name: str
    last_name: str
    photo: str
    password: constr(regex="^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$")

class TokenData(BaseModel):
    sub: str = ""
    exp: int = 0
    active: bool