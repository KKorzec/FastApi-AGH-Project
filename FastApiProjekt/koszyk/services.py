from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from FastApiProjekt import db
from FastApiProjekt.filmy.models import Film
from FastApiProjekt.user.models import User
from . models import Koszyk, PrzedmiotyKoszyka
from . import schema


async def dodaj_produkty(koszyk_id, film_id, database: Session = Depends(db.get_db)):
    przedmioty_koszyka = PrzedmiotyKoszyka(koszyk_id=koszyk_id, film_id=film_id)
    database.add(przedmioty_koszyka)
    database.commit()
    database.refresh(przedmioty_koszyka)


async def dodaj_do_koszyka(film_id, current_user, database: Session = Depends(db.get_db)):
    film_info = database.query(Film).get(film_id)
    if not film_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie znaleziono takiego filmu")

    user_info = database.query(User).filter(User.email == current_user.email).first()

    koszyk_info = database.query(Koszyk).filter(Koszyk.user_id == user_info.id).first()

    if not koszyk_info:
        nowy_koszyk = Koszyk(user_id=user_info.id)
        database.add(nowy_koszyk)
        database.commit()
        database.refresh(nowy_koszyk)
        await dodaj_produkty(nowy_koszyk.id, film_info.id, database)
    else:
        await dodaj_produkty(koszyk_info.id, film_info.id, database)

    return {"status": "Produkt dodano do koszyka!"}


async def pokaz_produkty(database, current_user) -> schema.PokazKoszyk:
    user_info = database.query(User).filter(User.email == current_user.email).first()
    koszyk = database.query(Koszyk).filter(Koszyk.user_id == user_info.id).first()
    return koszyk


async def usun_film_z_koszyka(koszyk_film_id, current_user, database) -> None:
    user_info = database.query(User).filter(User.email == current_user.email).first()
    koszyk_id = database.query(Koszyk).filter(User.id == user_info.id).first()
    database.query(PrzedmiotyKoszyka).filter(PrzedmiotyKoszyka.id == koszyk_film_id,
                                             PrzedmiotyKoszyka.koszyk_id == koszyk_id.id).delete()
    database.commit()
    return
