from jose import JWTError, jwt
from config.setup import settings
from src.auth.service import get_user_profile
from src.auth.exceptions import user_not_found_exception
from src.auth.schemas import TokenData

async def validate_token(token: str):
    try:
        result = jwt.decode(token, settings.PROJECT_SECRET_KEY, algorithms=[settings.PROJECT_PROJECT_ALGORITHM])
        return TokenData(sub=result["sub"], exp=result["exp"], active=True)
    except JWTError:
        return TokenData(active=False)

def verify_user_by_id(id):
    if not get_user_profile(id):
        raise user_not_found_exception
    return True