from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_token_header

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

fake_users_db = [
    {
        "email": "user@email.org",
        "password": "$2a$10$V4CX.CtRz6uueDR3virsh.3YrvF2bXDHttitxTJ7fUWXhTEbOukwa",
        "username": "Some user",
        "roles": ["ROLE_SWITCH", "ROLE_CAPTIVE"],
        "id": 1,
    },
    {
        "email": "slave@email.org",
        "password": "$2a$10$l58.9OT8oL0HJ2G.WFKJbOCyK6nRjxtAddTY616C1FF.3Lqzon.HK",
        "username": "Simple slave",
        "roles": ["ROLE_SWITCH"],
        "id": 2,
    },
]


@router.get("/")
async def get_users():
    return fake_users_db


@router.get("/{user_id}")
async def update_switch(user_id: str):
    user = next((x for x in fake_users_db if x.id == user_id), dict())
    return {k: v for k, v in user.items() if k != "password"}
