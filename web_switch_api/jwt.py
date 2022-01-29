from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from pydantic import BaseModel
from .models import UserOut
from . import configuration


class TokenData(BaseModel):
    user: UserOut
    iat: datetime
    exp: datetime
    sub: str


config = configuration.provider.get_jwt_config()


def create_access_token(user: UserOut, expires_delta: Optional[timedelta] = None) -> str:
    issued_at = datetime.utcnow()
    expire = issued_at + (expires_delta or timedelta(minutes=15))
    data = TokenData(
        user=UserOut(**user.dict()),
        iat=issued_at,
        exp=expire,
        sub=user.id
    )
    encoded_jwt = jwt.encode(
        data.dict(),
        config.secret_key,
        algorithm=config.algorithm
    )
    return encoded_jwt


def decode_access_token(token: str) -> TokenData:
    payload = jwt.decode(
        token,
        config.secret_key,
        algorithms=[config.algorithm]
    )
    data = TokenData(**payload)
    return data
