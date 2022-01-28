from typing import Union, Optional
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel

from ..models import UserIn, UserOut
from .users import fake_users_db
from ..jwt import create_access_token

ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(username: str) -> Optional[UserIn]:
    user = next((x for x in fake_users_db if x.email == username), None)
    return user


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str) -> Union[bool, UserOut]:
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return UserOut(**user.dict())


router = APIRouter(
    tags=["authentication"],
)


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user, access_token_expires)
    return Token(access_token=access_token, token_type="bearer")
