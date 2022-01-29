from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..dependencies import RequireRole, oauth2_scheme, get_current_user
from ..models import UserOut
from ..configuration import users

require_role = RequireRole("ROLE_USERS")

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", dependencies=[Depends(require_role)], response_model=List[UserOut])
async def get_users():
    return [UserOut(**u.dict()) for u in users.get_users()]


@router.get("/me", response_model=UserOut)
async def get_current_user(current_user: UserOut = Depends(get_current_user)):
    user_id = current_user.id
    user = await get_user(user_id)
    return user


@router.get("/{user_id}", dependencies=[Depends(require_role)], response_model=UserOut)
async def get_user(user_id: int):
    user = next((x for x in users.get_users() if x.id == user_id), None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User is missing"
        )
    return UserOut(**user.dict())
