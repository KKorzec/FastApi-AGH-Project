from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from typing import List
from FastApiProjekt import db
from FastApiProjekt.auth.jwt import get_current_user
from . import schema
from . import services
from . import validator

router = APIRouter(
    tags=['Filmy i gatunki filmowe'],
    prefix='/filmy'
)


@router.post('/gatunek', status_code=status.HTTP_201_CREATED)
async def utworz_gatunek(request: schema.Gatunek, database: Session = Depends(db.get_db)):
    nowy_gatunek = await services.utworz_nowy_gatunek(request, database)
    return nowy_gatunek


@router.get('/gatunek', response_model=List[schema.ListaGatunkow])
async def wyswietl_gatunek(database: Session = Depends(db.get_db)):
    return await services.wyswietl_gatunek(database)


@router.get('/gatunek/{gatunek_id}', response_model=schema.ListaGatunkow)
async def wyswietl_gatunki_po_id(gatunek_id: int, database: Session = Depends(db.get_db)):
    return await services.wyswietl_gatunek_po_id(gatunek_id, database)


@router.delete('/gatunek/{gatunek_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def usun_gatunek_po_id(gatunek_id: int, database: Session = Depends(db.get_db)):
    return await services.usun_gatunek_po_id(gatunek_id, database)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def utworz_film(request: schema.Film, database: Session = Depends(db.get_db)):
    gatunek = await validator.zweryfikuj_gatunek(request.gatunek_id, database)
    if not gatunek:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wprowadzono niewłaściwe id gatunku filmowego")
    film = await services.utworz_nowy_film(request, database)
    return film


@router.get('/', response_model=List[schema.ListaFilmow])
async def wyswietl_filmy(database: Session = Depends(db.get_db)):
    return await services.wyswietl_filmy(database)


@router.get('/{film_id}',response_model=schema.ListaFilmow)
async def wyswietl_film_po_id(film_id: int, database: Session = Depends(db.get_db)):
    return await services.wyswietl_film_po_id(film_id, database)


@router.delete('/{film_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def usun_film_po_id(film_id: int, database: Session = Depends(db.get_db)):
    return await services.usun_film_po_id(film_id, database)
