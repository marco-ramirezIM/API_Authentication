from datetime import timedelta
from http.client import HTTPException
from src.auth.schemas import Login, Token, UserProfile, UpdateUserProfile,TokenData
from fastapi import APIRouter, Form, Depends
import src.auth.service as service
from config.setup import settings
from src.auth.exceptions import incorrect_credentials_exception
import src.auth.dependencies as dependencies
import src.dependencies as dp
from config.db import Session
import src.auth.exceptions as exceptions

auth = APIRouter()

@auth.post("/login", response_model=Token)
async def login(form_data: Login, db: Session = Depends(dp.get_db)):
    try:
        user = service.authenticate_user(db, form_data.email, form_data.password)
        if not user:
            raise incorrect_credentials_exception
        access_token_expires = timedelta(minutes=settings.PROJECT_ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = service.create_access_token(
            data={"sub": user.email, "role": user.role.name } , expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        raise e
    except Exception:
        raise exceptions.authenticate_user

@auth.get("/user-profile/{id}", response_model=UserProfile)
async def get_user_profile(id: str, db: Session = Depends(dp.get_db)):
    try:
        return service.get_user_profile(db, id)
    except HTTPException as e:
        raise e
    except Exception:
        raise exceptions.get_user_profile

@auth.put("/user-profile/{id}", response_model=UserProfile)
async def update_user_profile(id: str, form_data: UpdateUserProfile, db: Session = Depends(dp.get_db)):
    try:
        return service.update_user_profile(db, id, form_data)
    except HTTPException as e:
        raise e
    except Exception:
        raise exceptions.update_user_profile

@auth.post("/introspection", response_model=TokenData)
async def introspection(token: str = Form()):
    try:
        return await dependencies.validate_token(token)
    except HTTPException as e:
        raise e
    except Exception:
        raise exceptions.introspection