from typing import List
from pydantic import BaseModel


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    roles: List[str]


class UserIn(UserOut):
    password: str
