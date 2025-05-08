from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import timedelta

# Import functions and variables from auth.py
from ..auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, fake_users_db

router = APIRouter(tags=["Authentication"])

# Define Pydantic models here or import them
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenRequestForm(BaseModel):
    username: str
    password: str

@router.post("/token", response_model=Token)
async def login(form_data: TokenRequestForm):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}