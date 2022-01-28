from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..models import UserIn, UserOut
from .users import fake_users_db


def fake_hash_password(password: str) -> str:
    return password


router = APIRouter(
    tags=["authentication"],
)


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = next(
        (x for x in fake_users_db if x.email == form_data.username), None)
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    user = UserIn(**user_dict.dict())
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )

    return {"access_token": user.username, "token_type": "bearer"}
