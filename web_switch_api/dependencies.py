from base64 import decode
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from jose import JWTError
from .models import UserOut
from .jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserOut:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token_data = decode_access_token(token)
        return token_data.user
    except JWTError:
        raise credentials_exception
    except ValidationError:
        raise credentials_exception


async def get_token_header(x_token: str = Header(...)):
    if x_token != "todo-replace-with-jwt-token":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-Token header invalid"
        )
