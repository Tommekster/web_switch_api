from fastapi import Depends, FastAPI

from .dependencies import get_token_header
from .routers import switches, captiveImage, users

app = FastAPI(dependencies=[Depends(get_token_header)])

app.include_router(switches.router)
app.include_router(captiveImage.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "Hello world"}
