from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from FastApiProjekt import db
from FastApiProjekt.auth.jwt import get_current_user
from FastApiProjekt.user.schema import User
from . import services
from . import schema

router = APIRouter(
    tags=['Koszyk'],
    prefix='/koszyk'
)


@router.get('/dodaj',status_code=status.HTTP_201_CREATED)
async def dodaj_film_do_koszyka(film_id: int, database: Session = Depends(db.get_db),
                                current_user: User = Depends(get_current_user)):
    wynik = await services.dodaj_do_koszyka(film_id, current_user, database)
    return wynik


@router.get('/', response_model=schema.PokazKoszyk)
async def pokaz_produkty_w_koszyku(database: Session = Depends(db.get_db),
                                   current_user: User = Depends(get_current_user)):
    wynik = await services.pokaz_produkty(database, current_user)
    return wynik


@router.delete('/{koszyk_film_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def usun_film_z_koszyka_po_id(koszyk_film_id, database: Session = Depends(db.get_db),
                                    current_user: User = Depends(get_current_user)):
    await services.usun_film_z_koszyka(koszyk_film_id, current_user, database)
