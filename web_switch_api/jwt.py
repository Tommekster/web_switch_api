from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from pydantic import BaseModel
from .models import UserOut


SECRET_KEY = "1840775961ba5d9a5cf997dcb5ae687edce580e28ac4e929c85b864df6ad309c"
ALGORITHM = "HS256"


class TokenData(BaseModel):
    user: UserOut
    iat: datetime
    exp: datetime
    sub: int


def create_access_token(user: UserOut, expires_delta: Optional[timedelta] = None) -> str:
    issued_at = datetime.utcnow()
    expire = issued_at + (expires_delta or timedelta(minutes=15))
    data = TokenData(
        user=UserOut(**user.dict()),
        iat=issued_at,
        exp=expire,
        sub=user.id
    )
    encoded_jwt = jwt.encode(data.dict(), SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> TokenData:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    data = TokenData(**payload)
    return data
