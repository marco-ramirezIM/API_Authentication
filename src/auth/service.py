from datetime import datetime, timedelta
from typing import Union

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from src.auth.schemas import UpdateUserProfile
from config.setup import settings

from config.db import engine
from src.auth.models import users

from src.auth.exceptions import disabled_user_exception

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except:
        return False

def authenticate_user(email: str, password: str):
    user = get_user(email)
    if not user:
        return False
    if user["state"] != 1:
        raise disabled_user_exception
    if not verify_password(password, user["password"]):
        return False
    return user

def update_user_profile(id: str, form_data: UpdateUserProfile):
    encrypt_password = pwd_context.hash(form_data.password)
    with engine.connect() as conn:
        conn.execute(users.update().values(first_name=form_data.first_name, last_name=form_data.last_name, 
        password=encrypt_password, photo=form_data.photo).where(users.c["id"] == id))
    return get_user_profile(id)

def get_user_profile(id: str):
    return __get_user_by_field("id", id)

def get_user(email: str):
    return __get_user_by_field("email", email)

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.PROJECT_SECRET_KEY , algorithm=settings.PROJECT_PROJECT_ALGORITHM)
    return encoded_jwt

def __get_user_by_field(field: str, value: str):
    with engine.connect() as conn:
        return conn.execute(users.select().where(users.c[field] == value)).first()
