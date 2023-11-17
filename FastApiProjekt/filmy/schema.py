from typing import Optional
from pydantic import BaseModel, constr


class Gatunek(BaseModel):
    nazwa: constr(min_length=2, max_length=50)


class ListaGatunkow(BaseModel):
    id: int
    nazwa: str

    class Config:
        orm_mode = True


class FilmBase(BaseModel):
    id: Optional[int]
    tytul: str
    opis: str
    cena: float
    ocena: float

    class Config:
        orm_mode = True


class Film(FilmBase):
    gatunek_id: int


class ListaFilmow(FilmBase):
    gatunek: ListaGatunkow

    class Config:
        orm_mode = True
