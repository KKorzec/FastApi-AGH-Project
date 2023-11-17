from fastapi import APIRouter
from typing import Awaitable
from fastapi import Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from FastApiProjekt.filmy.services import wyswietl_filmy, wyswietl_gatunek, wyswietl_film_po_id2, wyswietl_gatunek2
from FastApiProjekt import db


templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/")
async def home(request: Request, database: Session = Depends(db.get_db), msg:str = None):
    filmy = await wyswietl_filmy(database=database)
    gatunki = await wyswietl_gatunek(database=database)
    return templates.TemplateResponse(
        "general_pages/homepage.html", {"request": request, "filmy": filmy, "gatunki": gatunki, "msg":msg}
    )


@router.get('/film/detail/{id}')
def szczegoly_filmu(id: int, request: Request, database: Session = Depends(db.get_db)):
    film = wyswietl_film_po_id2(film_id=id, database=database)
    gatunki = wyswietl_gatunek2(database=database)
    return templates.TemplateResponse(
        "film/detail.html", {"request": request, "film": film, "gatunki": gatunki}
    )
