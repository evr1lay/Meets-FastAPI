from contextlib import asynccontextmanager
import random
from typing import Optional
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict

from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase, Mapped, mapped_column

from config import get_settings
settings = get_settings()

engine = create_engine(url=settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    
class FormORM(Base):
    __tablename__ = "Forms"
    title: Mapped[str]
    description: Mapped[str]
    likes: Mapped[int]
    
@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(engine)
    yield

app = FastAPI(title="Meets", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FormSchema(BaseModel):
    id: str
    title: str
    description: str
    likes: int
    
    model_config = ConfigDict(from_attributes=True)
    
class FormCreateSchema(BaseModel):
    title: str
    description: str
    likes: int
    
class FormUpdateSchema(BaseModel):
    title: Optional[str] | None = None
    description: Optional[str] | None = None
    likes: Optional[int] | None = None
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def form_orm_to_model(ORM: FormORM):
    return FormSchema(id=ORM.id, title=ORM.title, description=ORM.description, likes=ORM.likes)

@app.get("/forms/random", tags=["GET-Methods"])
def get_random(db: Session = Depends(get_db)) -> FormSchema:
    forms_orm = db.scalars(select(FormORM)).all()
    if not forms_orm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No forms found")
    forms_table = [FormSchema.model_validate(form) for form in forms_orm]
    return forms_table[random.randint(0, len(forms_table) - 1)]

@app.post("/forms", tags=["POST-Methods"], status_code=status.HTTP_201_CREATED)
def create_form(payload: FormCreateSchema, db: Session = Depends(get_db)) -> FormSchema:
    new_form = FormORM(id=str(uuid4()), **payload.model_dump())
    db.add(new_form)
    db.commit()
    db.refresh(new_form)
    return form_orm_to_model(new_form)

@app.patch("/forms", tags=["PATCH-Methods"])
def update_form(form_id: str, payload: FormUpdateSchema, db: Session = Depends(get_db)) -> FormSchema:
    form_for_update = db.get(FormORM, form_id)
    if not form_for_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(form_for_update, key, value)
        
    db.commit()
    db.refresh(form_for_update)
    
    return form_orm_to_model(form_for_update)

@app.delete("/forms", tags=["DELETE-Methods"], status_code=status.HTTP_204_NO_CONTENT)
def delete_form(form_id: str, db: Session = Depends(get_db)) -> None:
    form_for_delete = db.get(FormORM, form_id)
    if not form_for_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    db.delete(form_for_delete)
    db.commit()
    db.refresh(form_for_delete)