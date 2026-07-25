from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.form import FormService

def get_form_service(db: Session = Depends(get_db)):
    """Dependency injection function FormService"""
    return FormService(db)