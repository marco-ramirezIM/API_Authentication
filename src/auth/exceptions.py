from fastapi import HTTPException

credentials_exception = HTTPException(401,detail="Could not validate credentials")
incorrect_crendentilas_exception = HTTPException(401,detail="Incorrect username or password")
disabled_user_exception = HTTPException(401,detail="Disabled user")
user_not_found_exception = HTTPException(401,detail="User not found")
authenticate_user = HTTPException(500, detail="There was an error to authenticate_user")
get_user_profile = HTTPException(500, detail="There was an error trying to get user profile")
update_user_profile = HTTPException(500, detail="There was an error trying to update user profile")
introspection = HTTPException(500, detail="There was an error trying to introspection")