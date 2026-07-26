from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.session import engine
from core.config import get_settings
from models.base import Base
from api.routers.form import router as form_router

settings = get_settings()
    
@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(engine)
    yield

app = FastAPI(title="Meets", lifespan=lifespan)
app.include_router(form_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["🔍 GET-Methods"])
def get_api_status():
    return {"API_ENABLED": True}