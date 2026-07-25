from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import engine
from app.core.config import get_settings
from app.models.base import Base

settings = get_settings()
    
@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(engine)
    yield

app = FastAPI(title="Meets", lifespan=lifespan)
app.add_middleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)