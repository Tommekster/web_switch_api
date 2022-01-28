from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .models import UserIn, UserOut

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def decode_token(token: str) -> UserOut:
    return UserOut(username=token, email="john@doe.com", roles=[])


async def get_token_header(x_token: str = Header(...)):
    if x_token != "todo-replace-with-jwt-token":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-Token header invalid"
        )
