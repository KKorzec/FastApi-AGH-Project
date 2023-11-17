from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from FastApiProjekt import db
from FastApiProjekt.auth.jwt import get_current_user
from FastApiProjekt.user.schema import User
from . import services
from . import schema
from typing import List


router = APIRouter(
    tags=["Zamowienia"],
    prefix='/zamowienia'
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.PokazZamowienie)
async def zloz_zamowienie(database: Session = Depends(db.get_db),
                          current_user: User = Depends(get_current_user)):
    wynik = await services.zloz_zamowienie(current_user, database)
    return wynik


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schema.PokazZamowienie])
async def szczegoly_zamowienia(database: Session = Depends(db.get_db),
                               current_user: User = Depends(get_current_user)):
    wynik = await services.lista_zamowien(current_user, database)
    return wynik
