from pydantic import BaseModel
import datetime
from typing import List
from FastApiProjekt.filmy.schema import Film

class PokazPrzedmiotyKoszyka(BaseModel):
    id: int
    filmy: Film
    data_utworzenia: datetime.datetime

    class Config:
        orm_mode = True


class PokazKoszyk(BaseModel):
    id: int
    przedmioty_koszyka: List[PokazPrzedmiotyKoszyka] = []

    class Config:
        orm_mode = True
