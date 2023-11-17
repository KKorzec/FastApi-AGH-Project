from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from FastApiProjekt.db import Base


class Gatunek(Base):
    __tablename__ = "gatunek"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nazwa = Column(String(50))

    film = relationship("Film", back_populates="gatunek")


class Film(Base):
    __tablename__ = "filmy"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tytul = Column(String(50))
    gatunek_id = Column(Integer, ForeignKey('gatunek.id', ondelete="CASCADE"))
    gatunek = relationship("Gatunek", back_populates="film")
    opis = Column(Text)
    cena = Column(Float)
    ocena = Column(Float)
    przedmioty_koszyka = relationship("PrzedmiotyKoszyka", back_populates="filmy")
    szczegoly_zamowienia = relationship("SzczegolyZamowienia", back_populates="szczegoly_zamowienia_filmu")
