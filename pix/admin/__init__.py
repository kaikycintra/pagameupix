from fastapi import FastAPI, Request, APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from . import models
from database import get_db

from . import schemas

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)

router.mount("app/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app")

@router.get("/", response_class=HTMLResponse)
async def render_admin_app(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name="item.html", context={"id": id}
    )

@router.post("/people/", response_class=HTMLResponse)
def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db(models))):
    return insertions.create_person(db=db, person=person)

@router.post("/people/{person_id}/debts/", response_model=schemas.Debt)
def create_debt_for_person(person_id: int, debt: schemas.DebtCreate, db: Session = Depends(get_db(models))):
    return insertions.create_debt_for_person(db=db, debt=debt, person_id=person_id)

@router.delete("/people/{person_id}", response_class=HTMLResponse)
def delete_person(person_id: int, db: Session = Depends(get_db(models))):
    """Deletes a person and all of their associated debts."""
    db_person = removals.delete_person_by_id(db=db, person_id=person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person

@router.delete("/debts/{debt_id}", response_class=HTMLResponse)
def delete_debt(debt_id: int, db: Session = Depends(get_db(models))):
    """Deletes a single debt."""
    db_debt = removals.delete_debt_by_id(db=db, debt_id=debt_id)
    if db_debt is None:
        raise HTTPException(status_code=404, detail="Debt not found")
    return db_debt