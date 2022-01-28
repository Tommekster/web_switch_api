from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..dependencies import oauth2_scheme
from ..models import UserIn, UserOut

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}},
)

fake_users_db = [
    UserIn(**{
        "email": "user@email.org",
        "password": "$2a$10$V4CX.CtRz6uueDR3virsh.3YrvF2bXDHttitxTJ7fUWXhTEbOukwa",
        "username": "Some user",
        "roles": ["ROLE_SWITCH", "ROLE_CAPTIVE"],
        "id": 1,
    }),
    UserIn(**{
        "email": "slave@email.org",
        "password": "$2a$10$l58.9OT8oL0HJ2G.WFKJbOCyK6nRjxtAddTY616C1FF.3Lqzon.HK",
        "username": "Simple slave",
        "roles": ["ROLE_SWITCH"],
        "id": 2,
    }),
]


@router.get("/", response_model=List[UserOut])
async def get_users():
    return fake_users_db


@router.get("/{user_id}", response_model=UserOut)
async def update_switch(user_id: int):
    user = next((x for x in fake_users_db if x.id == user_id), None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User is missing"
        )
    return {k: v for k, v in user.items() if k != "password"}
