from pydantic import BaseModel, constr, EmailStr
from datetime import date
from fastapi import Form


class User(BaseModel):
    id: int
    login: constr(min_length=2, max_length=50)
    haslo: str
    email: EmailStr
    data_urodzenia: date


class wyswietl_uzytkownikow(BaseModel):
    id: int
    login: str
    haslo: str
    email: str
    data_urodzenia: date

    class Config:
        orm_mode = True


class logowanie(BaseModel):
    login: str
    haslo: str

    @classmethod
    def as_form(
        cls,
        login: str = Form(...),
        haslo: str = Form(...)
    ):
        return cls(
            login=login,
            haslo=haslo
        )