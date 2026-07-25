from fastapi import APIRouter, Depends, HTTPException

from app.services.form import FormService
from app.schemas.form import FormSchema, FormUpdateSchema, FormCreateSchema
from app.api.dependencies import get_form_service

router = APIRouter(prefix="/forms")

@router.get("", tags=["GET-Methods"])
def get_forms(form_service: FormService = Depends(get_form_service)) -> list[FormSchema]:
    return form_service.list_forms()

@router.get("", tags=["GET-Methods"])
def get_random(form_service: FormService = Depends(get_form_service)) -> FormSchema:
    return form_service.get_random()

@router.post("", tags=["POST-Methods"])
def add_form(payload: FormCreateSchema, form_service: FormService = Depends(get_form_service)):
    return form_service.create_form(payload)

@router.patch("", tags=["PATCH-Methods"])
def upd_form(form_id: str, payload: FormUpdateSchema, form_service: FormService = Depends(get_form_service)) -> FormSchema:
    return form_service.update_form(form_id, payload)

@router.delete("", tags=["DELETE-Methods"])
def del_form(form_id: str, form_service: FormService = Depends(get_form_service)) -> None:
    return form_service.delete_form(form_id)