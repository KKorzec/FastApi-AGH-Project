from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends,APIRouter
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi import status,HTTPException

from FastApiProjekt import db
from FastApiProjekt.user.hash import hashuj, weryfikacja
from FastApiProjekt.auth import jwt
from db.repository.login import get_user
from core.security import create_access_token
from core.config import settings


router = APIRouter()


def authenticate_user(username: str, password: str, database: Session = Depends(db.get_db)):
    user = get_user(username=username, database=database)
    print(user)
    if not user:
        return False
    if not hashuj.weryfikacja(password, user.hashed_password):
        return False
    return user


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),db: Session= Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}