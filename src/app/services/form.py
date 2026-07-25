import random

from sqlalchemy.orm import Session

from app.repositories.form import FormNotFound, FormRepository
from app.schemas.form import FormSchema, FormCreateSchema, FormUpdateSchema

class FormService:
    def __init__(self, db: Session):
        self.db = db
        self.form_repository = FormRepository(db=db)
        
    def list_forms(self):
        forms_orm = self.form_repository.get_all()
        return [FormSchema.model_validate(form) for form in forms_orm]
    
    def get_random(self):
        forms_orm = self.form_repository.get_all()
        
        if not forms_orm:
            raise FormNotFound("No forms found")
        
        forms_table = [FormSchema.model_validate(form) for form in forms_orm]
        form_model = forms_table[random.randint(0, len(forms_table) - 1)]
        return form_model
        
    def create_form(self, payload: FormCreateSchema):
        form_orm = self.form_repository.create(payload)
        return FormSchema.model_validate(form_orm)
    
    def update_form(self, form_id: str, payload: FormUpdateSchema):
        try:
            form_orm = self.form_repository.update(form_id, payload)
            return FormSchema.model_validate(form_orm)
        except Exception:
            raise FormNotFound("Form not found")
    
    def delete_form(self, form_id: str):
        try:
            self.form_repository.delete(form_id)
        except Exception:
            raise FormNotFound("Form not found")