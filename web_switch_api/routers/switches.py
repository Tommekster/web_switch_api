from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from ..dependencies import get_token_header


class Switch(BaseModel):
    id: int
    label: str
    switched: bool


router = APIRouter(
    prefix="/switches",
    tags=["switches"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

fake_switches_db = [
    Switch(id=0, label="Swicth 1", switched=True),
    Switch(id=1, label="Swicth 2", switched=False),
]


@router.get("/", response_model=List[Switch])
async def get_switches():
    return fake_switches_db


@router.put("/{switch_id}", response_model=Switch)
async def update_switch(switch_id: int, update: Switch):
    switch = next((x for x in fake_switches_db if x.id == switch_id), None)
    if not switch:
        raise HTTPException(status_code=404, detail="Switch is missing")
    switch.switched = update.switched
    return switch
