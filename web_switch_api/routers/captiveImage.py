import base64
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ..dependencies import RequireRole
from .. import configuration


class CaptiveImage(BaseModel):
    filename: str
    mime: str
    data: bytes


config = configuration.provider.get_captive_portal_config()

require_role = RequireRole("ROLE_CAPTIVE")

router = APIRouter(
    prefix="/captiveImage",
    tags=["captiveImage"],
    dependencies=[Depends(require_role)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=CaptiveImage)
async def get_captive_image():
    with open(config.image_path, "rb") as f:
        data = base64.encodebytes(f.read())
        captive_image = CaptiveImage(
            filename="captive.jpg",
            mime="image/jpeg",
            data=data
        )
        return captive_image


@router.put("/", response_model=CaptiveImage)
async def update_captive_image(image: CaptiveImage):
    with open(config.image_path, "wb") as f:
        f.write(base64.decodebytes(image.data))
    return await get_captive_image()
