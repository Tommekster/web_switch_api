from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_token_header

router = APIRouter(
    prefix="/switches",
    tags=["switches"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

fake_switches_db = [
    {"id": 0, "label": "Swicth 1", "switched": True},
    {"id": 1, "label": "Swicth 2", "switched": False},
]


@router.get("/")
async def get_switches():
    return fake_switches_db


@router.put("/{switch_id}")
async def update_switch(switch_id: str):
    pass
