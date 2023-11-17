from fastapi import HTTPException, status
from typing import List, Optional
from . import models
from . import schema


async def zarejestruj_uzytkownika(request, database) -> models.User:
    nowy_uzytkownik = models.User(login=request.login, haslo=request.haslo, email=request.email,
                                  data_urodzenia=request.data_urodzenia)
    database.add(nowy_uzytkownik)
    database.commit()
    database.refresh(nowy_uzytkownik)
    return nowy_uzytkownik


async def all_users(database) -> List[models.User]:
    uzytkownicy = database.query(models.User).all()
    return uzytkownicy


async def wyswietl_uzytkownika_po_id(user_id, database) -> Optional[models.User]:
    uzytkownik_info = database.query(models.User).get(user_id)
    if not uzytkownik_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie ma takiego użytkownika!")
    return uzytkownik_info


async def usun_uzytkownika_po_id(user_id, database):
    database.query(models.User).filter(models.User.id == user_id).delete()
    database.commit()
