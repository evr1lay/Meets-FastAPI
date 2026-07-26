from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Union

from repositories.form import FormNotFound
from services.form import FormService
from schemas.form import FormSchema, FormUpdateSchema, FormCreateSchema
from api.dependencies import get_form_service

router = APIRouter(prefix="/forms")

@router.get("", tags=["🔍 GET-Methods"])
def get_forms(form_service: FormService = Depends(get_form_service)) -> list[FormSchema]:
    return form_service.list_forms()

@router.get("/random", tags=["🔍 GET-Methods"])
def get_random(form_service: FormService = Depends(get_form_service)) -> Union[FormSchema, dict]:
    try:
        return form_service.get_random()
    except FormNotFound:
        return {"message": "There are no suitable forms", "data": None}

@router.post("", tags=["📚 POST-Methods"], status_code=status.HTTP_201_CREATED)
def add_form(payload: FormCreateSchema, form_service: FormService = Depends(get_form_service)):
    return form_service.create_form(payload)

@router.patch("", tags=["✏️ PATCH-Methods"])
def upd_form(form_id: str, payload: FormUpdateSchema, form_service: FormService = Depends(get_form_service)) -> FormSchema:
    return form_service.update_form(form_id, payload)

@router.delete("", tags=["🗑️ DELETE-Methods"], status_code=status.HTTP_204_NO_CONTENT)
def del_form(form_id: str, form_service: FormService = Depends(get_form_service)) -> None:
    return form_service.delete_form(form_id)