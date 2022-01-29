from typing import Tuple, Union, Optional
import re
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel

from ..models import UserIn, UserOut
from ..configuration import users, provider as config_provider
from ..jwt import create_access_token


class Token(BaseModel):
    access_token: str
    token_type: str


class UserAndToken(BaseModel):
    accessToken: str
    user: UserOut


class LoginRequestBody(BaseModel):
    email: str
    password: str


config = config_provider.get_authentication_config()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(username: str) -> Optional[UserIn]:
    user = next((x for x in users.get_users() if x.email == username), None)
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


def login(email: str, password: str) -> Tuple[UserOut, str]:
    email_regex = re.compile(
        r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$")
    if not email_regex.match(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email format is invalid",
        )
    user = authenticate_user(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = config.expiration_time
    access_token = create_access_token(user, access_token_expires)
    return user, access_token


@router.post("/token", response_model=Token)
async def oauth2_login(form_data: OAuth2PasswordRequestForm = Depends()):
    _, access_token = login(form_data.username, form_data.password)
    return Token(access_token=access_token, token_type="bearer")


@router.post("/login", response_model=UserAndToken)
async def react_login(request: LoginRequestBody):
    user, access_token = login(request.email, request.password)
    return UserAndToken(user=user, accessToken=access_token)
