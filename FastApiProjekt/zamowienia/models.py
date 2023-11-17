from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from FastApiProjekt.user.models import User
from FastApiProjekt.filmy.models import Film
from FastApiProjekt.db import Base


class Zamowienie(Base):
    __tablename__ = "zamowienie"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data_zamowienia = Column(DateTime, default=datetime.now)
    kwota_zamowienia = Column(Float, default=0.0)
    status_zamowienia = Column(String(50), default="PRZETWARZANIE", index=True)
    id_klienta = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"))
    szczegoly_zamowienia = relationship("SzczegolyZamowienia", back_populates="zamowienie")
    user_info = relationship("User", back_populates="zamowienie")


class SzczegolyZamowienia(Base):
    __tablename__ = "szczegoly_zamowienia"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_zamowienia = Column(Integer, ForeignKey('zamowienie.id', ondelete="CASCADE"))
    id_filmu = Column(Integer, ForeignKey(Film.id, ondelete="CASCADE"))
    zamowienie = relationship("Zamowienie", back_populates="szczegoly_zamowienia")
    szczegoly_zamowienia_filmu = relationship("Film", back_populates="szczegoly_zamowienia")
    data_utworzenia = Column(DateTime, default=datetime.now)
