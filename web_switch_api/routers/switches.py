from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel
import requests
from ..dependencies import RequireRole
from .. import configuration


class Switch(BaseModel):
    id: int
    label: str
    switched: bool


config = configuration.provider.get_switches_config()

require_role = RequireRole("ROLE_SWITCH")

router = APIRouter(
    prefix="/switches",
    tags=["switches"],
    dependencies=[Depends(require_role)],
    responses={404: {"description": "Not found"}},
)


def __call_switch_api__(switch_id: Optional[int] = None, new_state: Optional[bool] = None) -> List[Switch]:
    action = "on" if new_state else "off"
    url = (
        config.api_url +
        (f"/{switch_id}/{action}" if switch_id is not None else "")
    )
    response = requests.get(url)
    switches = [
        Switch(
            id=int(k),
            switched=v,
            label=config.switch_names.get(int(k), f"switch {k}")
        )
        for k, v in response.json().items()
    ]
    return switches


@router.get("/", response_model=List[Switch])
async def get_switches():
    return __call_switch_api__()


@router.put("/{switch_id}", response_model=Switch)
async def update_switch(switch_id: int, update: Switch):
    switches = __call_switch_api__(switch_id, update.switched)
    switch = next((x for x in switches if x.id == switch_id), None)
    if not switch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Switch is missing"
        )
    return switch
