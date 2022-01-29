from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..dependencies import RequireRole, oauth2_scheme, get_current_user
from ..models import UserIn, UserOut

fake_users_db = [
    UserIn(**{
        "email": "user@email.org",
        "password": "$2a$10$V4CX.CtRz6uueDR3virsh.3YrvF2bXDHttitxTJ7fUWXhTEbOukwa",
        "username": "Admin user",
        "roles": ["ROLE_SWITCH", "ROLE_CAPTIVE", "ROLE_USERS"],
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

require_role = RequireRole("ROLE_USERS")


router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(require_role)], response_model=List[UserOut])
async def get_users():
    return fake_users_db


@router.get("/me", response_model=UserOut)
async def get_current_user(current_user: UserOut = Depends(get_current_user)):
    user_id = current_user.id
    user = await get_user(user_id)
    return user


@router.get("/{user_id}", dependencies=[Depends(require_role)], response_model=UserOut)
async def get_user(user_id: int):
    user = next((x for x in fake_users_db if x.id == user_id), None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User is missing"
        )
    return UserOut(**user.dict())
