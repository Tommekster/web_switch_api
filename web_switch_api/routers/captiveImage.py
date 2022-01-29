from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ..dependencies import RequireRole


class CaptiveImage(BaseModel):
    filename: str
    mime: str
    data: bytes


require_role = RequireRole("ROLE_CAPTIVE")

router = APIRouter(
    prefix="/captiveImage",
    tags=["captiveImage"],
    dependencies=[Depends(require_role)],
    responses={404: {"description": "Not found"}},
)

fake_captive_image = CaptiveImage(**{
    "filename": "captive.jpg",
    "mime": "image/jpeg",
    "data": "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",
})


@router.get("/", response_model=CaptiveImage)
async def get_captive_image():
    return fake_captive_image


@router.put("/", response_model=CaptiveImage)
async def update_captive_image(image: CaptiveImage):
    fake_captive_image.data = image.data
    return fake_captive_image
