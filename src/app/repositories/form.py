from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.schemas.form import FormSchema, FormCreateSchema, FormUpdateSchema
from app.models.form import FormORM

class FormNotFound(Exception):
    """Form not found"""

class FormRepository:
    def __init__(self, db: Session) -> None:
        self.db = db
        
    def get_all(self):
        return self.db.scalars(select(FormORM)).all()
    
    def get_by_id(self, form_id: str):
        form_by_id = self.db.get(FormORM, form_id)
        if not form_by_id:
            raise FormNotFound("Form not found")
        return form_by_id
    
    def create(self, payload: FormCreateSchema):
        new_form = FormORM(id=str(uuid4()), **payload.model_dump())
        self.db.add(new_form)
        self.db.commit()
        self.db.refresh(new_form)
        return new_form
    
    def update(self, form_id: str, payload: FormUpdateSchema):
        form_for_update = self.db.get(FormORM, form_id)
        if not form_for_update:
            raise FormNotFound("Form not found")
        
        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(form_for_update, key, value)
            
        self.db.commit()
        self.db.refresh(form_for_update)
        
        return form_for_update
    
    def delete(self, form_id: str) -> None:
        form_for_delete = self.db.get(FormORM, form_id)
        if not form_for_delete:
            raise FormNotFound("Form not found")
        
        self.db.delete(form_for_delete)
        self.db.commit()