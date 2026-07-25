from typing import Optional
from pydantic import BaseModel, ConfigDict

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