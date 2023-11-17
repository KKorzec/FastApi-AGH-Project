from fastapi import HTTPException, status
from . import models
from typing import List


async def utworz_nowy_gatunek(request, database) -> models.Gatunek:
    nowy_gatunek = models.Gatunek(nazwa=request.nazwa)
    database.add(nowy_gatunek)
    database.commit()
    database.refresh(nowy_gatunek)
    return nowy_gatunek


async def wyswietl_gatunek(database) -> List[models.Gatunek]:
    gatunki = database.query(models.Gatunek).all()
    return gatunki


def wyswietl_gatunek2(database) -> List[models.Gatunek]:
    gatunki = database.query(models.Gatunek).all()
    return gatunki


async def wyswietl_gatunek_po_id(gatunek_id, database) -> models.Gatunek:
    gatunek_info = database.query(models.Gatunek).get(gatunek_id)
    if not gatunek_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie ma takiego gatunku")
    return gatunek_info


async def usun_gatunek_po_id(gatunek_id, database):
    database.query(models.Gatunek).filter(models.Gatunek.id == gatunek_id).delete()
    database.commit()


async def utworz_nowy_film(request, database) -> models.Film:
    nowy_film = models.Film(tytul=request.tytul,
                            gatunek_id=request.gatunek_id,
                            opis=request.opis,
                            cena=request.cena,
                            ocena=request.ocena)

    database.add(nowy_film)
    database.commit()
    database.refresh(nowy_film)
    return nowy_film


async def wyswietl_filmy(database) -> List[models.Film]:
    filmy = database.query(models.Film).all()
    return filmy


async def wyswietl_filmy2(database):
    filmy = database.query(models.Film).all()
    lista = List[models.Film]
    for film in filmy:
        film_gatunek = database.query(models.Gatunek.nazwa).filter(models.Film.gatunek_id == models.Gatunek.id).first()
        data = [["id", database.query(models.Film).get(film.id)],
                ["tytul", database.query(models.Film).get(film.tytul)],
                ["gatunek_id", film_gatunek],
                ["opis", database.query(models.Film).get(film.opis)],
                ["cena", database.query(models.Film).get(film.cena)],
                ["ocena", database.query(models.Film).get(film.ocena)]]
        lista.append(data)

    return lista


async def wyswietl_film_po_id(film_id, database) -> models.Film:
    film_info = database.query(models.Film).get(film_id)
    if not film_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie ma takiego filmu!")
    return film_info


def wyswietl_film_po_id2(film_id, database) -> models.Film:
    film_info = database.query(models.Film).get(film_id)
    if not film_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nie ma takiego filmu!")
    return film_info


async def usun_film_po_id(film_id, database):
    database.query(models.Film).filter(models.Film.id == film_id).delete()
    database.commit()
