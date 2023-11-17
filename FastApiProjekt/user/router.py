from fastapi import APIRouter, Depends, status, Response, HTTPException, responses
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from FastApiProjekt import db
from FastApiProjekt.auth.jwt import get_current_user
from typing import List
from fastapi import Request
from . import schema
from . import services
from . import validator
from FastApiProjekt.user.forms import FormUtworzUzytkownika
from FastApiProjekt.user.models import User
from FastApiProjekt.user.schema import User as U2
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=['Użytkownicy'], prefix='/user')
templates = Jinja2Templates(directory="templates")


# Templatki Jinja2 do rejestracji
@router.get("/zarejestruj/")
def zarejestruj(request: Request):
    return templates.TemplateResponse("user/zarejestruj.html", {"request": request})


@router.post("/zarejestruj/")
async def zarejestruj(request: Request, database: Session = Depends(db.get_db)):
    form = FormUtworzUzytkownika(request)
    await form.load_data()
    if await form.is_valid():
        user = U2(
            id=0, login=form.login, haslo=form.haslo, email=form.email, data_urodzenia=form.data_urodzenia
        )
        try:
            user = await utworz_uzytkownika(request=user, database=database)
            return responses.RedirectResponse(
                "/?msg=Poprawnie%20Zarejestrowano", status_code=status.HTTP_302_FOUND)
        except IntegrityError:
            form.__dict__.get("errors").append("Użytkownik o podanym adresie email już istnieje w systemie.")
            return templates.TemplateResponse("user/zarejestruj.html", form.__dict__)
    return templates.TemplateResponse("user/zarejestruj.html", form.__dict__)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def utworz_uzytkownika(request: schema.User, database: Session = Depends(db.get_db)):
    login = await validator.verify_email_exist(request.email, database)

    if login:
        raise HTTPException(
            status_code=400,
            detail="Użytkownik o podanym adresie email już istnieje w systemie."
        )

    nowy_uzytkownik = await services.zarejestruj_uzytkownika(request, database)
    return nowy_uzytkownik


@router.get('/', response_model=List[schema.wyswietl_uzytkownikow])
async def wyswietl_uzytkownikow(database: Session = Depends(db.get_db),
                                get_current_user: schema.User = Depends(get_current_user)):
    return await services.all_users(database)


@router.get('/{user_id}', response_model=schema.wyswietl_uzytkownikow)
async def wyswietl_uzytkownika_po_id(user_id: int, database: Session = Depends(db.get_db),
                                     get_current_user: schema.User = Depends(get_current_user)):
    return await services.wyswietl_uzytkownika_po_id(user_id, database)


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def usun_uzytkownika_po_id(user_id: int, database: Session = Depends(db.get_db),
                                 get_current_user: schema.User = Depends(get_current_user)):
    return await services.usun_uzytkownika_po_id(user_id, database)

