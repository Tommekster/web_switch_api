from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import switches, captiveImage, users, authentication

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(switches.router)
app.include_router(captiveImage.router)
app.include_router(users.router)
app.include_router(authentication.router)


@app.get("/")
async def root():
    return {"message": "Hello world"}
