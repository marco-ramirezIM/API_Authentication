from datetime import datetime, timedelta
from typing import Union
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from src.auth.schemas import UpdateUserProfile, User, UserProfile
from src.auth.models import User
from config.setup import settings
from src.auth.exceptions import disabled_user_exception, user_not_found_exception
from config.db import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except:
        return False

def authenticate_user(db: Session, email: str, password: str) -> User:
    user = get_user_by_email(db, email)
    if not user:
        return False
    if user.state != 1:
        raise disabled_user_exception
    if not verify_password(password, user.password):
        return False
    return user

def update_user_profile(db: Session, id: str, form_data: UpdateUserProfile) -> UserProfile:
    user = get_user_profile(db, id)
    encrypt_password = pwd_context.hash(form_data.password)
    db.query(User) \
        .filter(User.id == id) \
        .update({"first_name":form_data.first_name, "last_name":form_data.last_name, "password": encrypt_password, "photo": form_data.photo }) 
    db.commit()
    return user

def get_user_profile(db: Session, id: str) -> UserProfile:
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise user_not_found_exception
    return user

def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.PROJECT_SECRET_KEY , algorithm=settings.PROJECT_PROJECT_ALGORITHM)
    return encoded_jwt
