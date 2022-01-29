from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from .routers import switches, captiveImage, users, authentication
from .react import ReactStaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/api")
router.include_router(switches.router)
router.include_router(captiveImage.router)
router.include_router(users.router)
router.include_router(authentication.router)

app.include_router(router)

react = ReactStaticFiles(directory='../web_switch_gui/build', html=True)
app.mount('/', react, name='whatever')


@app.get("/hello")
async def root():
    return {"message": "Hello world"}
