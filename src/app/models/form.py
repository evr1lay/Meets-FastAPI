from sqlalchemy.orm import Mapped
from app.models.base import Base

class FormORM(Base):
    __tablename__ = "Forms"
    title: Mapped[str]
    description: Mapped[str]
    likes: Mapped[int]