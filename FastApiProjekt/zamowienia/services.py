from fastapi import HTTPException, status
from FastApiProjekt.koszyk.models import Koszyk, PrzedmiotyKoszyka
from FastApiProjekt.zamowienia.models import Zamowienie, SzczegolyZamowienia
from FastApiProjekt.user.models import User
from typing import List
from . import tasks


async def zloz_zamowienie(current_user, database) -> Zamowienie:
    user_info = database.query(User).filter(User.email == current_user.email).first()
    koszyk = database.query(Koszyk).filter(Koszyk.user_id == user_info.id).first()

    przedmioty_w_koszyku = database.query(PrzedmiotyKoszyka).filter(Koszyk.id == koszyk.id)
    if not przedmioty_w_koszyku.count():
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Nie znaleziono żadnych produktów w koszyku")

    Calkkoszt = 0.0
    for przedmiot in przedmioty_w_koszyku:
        Calkkoszt += przedmiot.filmy.cena

    nowe_zamowienie = Zamowienie(kwota_zamowienia=Calkkoszt,
                                 id_klienta=user_info.id)
    database.add(nowe_zamowienie)
    database.commit()
    database.refresh(nowe_zamowienie)

    lista_obiektow = list()

    for przedmiot in przedmioty_w_koszyku:
        szczegoly_nowego_zamowienia = SzczegolyZamowienia(id_zamowienia=nowe_zamowienie.id,
                                                          id_filmu=przedmiot.filmy.id)
        lista_obiektow.append(szczegoly_nowego_zamowienia)

    database.bulk_save_objects(lista_obiektow)
    database.commit()

    tasks.send_email(current_user.email)

    database.query(PrzedmiotyKoszyka).filter(PrzedmiotyKoszyka.koszyk_id == koszyk.id).delete()
    database.commit()

    return nowe_zamowienie


async def lista_zamowien(current_user, database) -> List[Zamowienie]:
    user_info = database.query(User).filter(User.email == current_user.email).first()
    zamowienia = database.query(Zamowienie).filter(Zamowienie.id_klienta == user_info.id).all()
    return zamowienia
