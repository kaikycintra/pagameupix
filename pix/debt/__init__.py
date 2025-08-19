from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from . import service
from . import models

router = APIRouter(
    prefix="/debt",
    tags=["Debt"],
)

templates = Jinja2Templates(directory="debt/templates")


@router.get("/", response_class=HTMLResponse)
async def render_debt_app(request: Request):
    return templates.TemplateResponse(
        request=request, name="pages/index.html"
    )

@router.get("/people/", response_class=HTMLResponse)
def search_people(request: Request, q: Optional[str] = None, limit: int = 10, db: Session = Depends(get_db)):
    """
    Searches for people by name. If no query 'q' is provided,
    it returns a list of all people up to the limit.
    """
    people_names = service.search_people_by_name(db=db, q=q, field_name="name", limit=limit)
    return templates.TemplateResponse(
        request=request, name="partials/people.html", context={"people_names": people_names}
    )

@router.get("/people/top/", response_class=HTMLResponse)
def get_top_debtors(request: Request, limit: int = 5, db: Session = Depends(get_db)):
    """
    Get a list of the top debtors, sorted by the total amount owed.
    """
    top_debtors = service.get_top_debtors(db=db, limit=limit)
    return templates.TemplateResponse(
        request=request, name="partials/topdebtors.html", context={"top_debtors": top_debtors}
    )