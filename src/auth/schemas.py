from pydantic import BaseModel
class Token(BaseModel):
    access_token: str
    token_type: str

class Login(BaseModel):
    email: str
    password: str

class UserProfile(BaseModel):
    email: str
    first_name: str
    last_name: str
    photo: str

class UpdateUserProfile(BaseModel):
    first_name: str
    last_name: str
    photo: str
    password: str

class TokenData(BaseModel):
    sub: str = ""
    exp: int = 0
    active: bool