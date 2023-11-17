from pydantic import BaseModel
import datetime
from typing import Optional, List
from FastApiProjekt.filmy.schema import ListaFilmow


class PokazSzczegolyZamowienia(BaseModel):
    id: int
    id_zamowienia: int
    szczegoly_zamowienia_filmu: ListaFilmow

    class Config:
        orm_mode = True


class PokazZamowienie(BaseModel):
    id: Optional[int]
    data_zamowienia: datetime.datetime
    kwota_zamowienia: float
    status_zamowienia: str
    szczegoly_zamowienia: List[PokazSzczegolyZamowienia] = []

    class Config:
        orm_mode = True
