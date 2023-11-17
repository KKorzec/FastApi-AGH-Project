from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from FastApiProjekt.db import Base
from . import hash


class User(Base):
    __tablename__ = "uzytkownicy"

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(50))
    haslo = Column(String(255))
    email = Column(String(255), unique=True)
    data_urodzenia = Column(Date)
    koszyk = relationship("Koszyk", back_populates="user_koszyka")
    zamowienie = relationship("Zamowienie", back_populates="user_info")

    def __init__(self, login, haslo, email, data_urodzenia, *args, **kwargs):
        self.login = login
        self.haslo = hash.hashuj(haslo)
        self.email = email
        self.data_urodzenia = data_urodzenia

    def sprawdz_haslo(self, haslo):
        return hash.weryfikacja(self.haslo, haslo)
