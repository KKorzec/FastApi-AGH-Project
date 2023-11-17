from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from FastApiProjekt.db import Base
from FastApiProjekt.filmy.models import Film
from FastApiProjekt.user.models import User


class Koszyk(Base):
    __tablename__ = "koszyk"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"))
    przedmioty_koszyka = relationship("PrzedmiotyKoszyka", back_populates="koszyk")
    user_koszyka = relationship("User", back_populates="koszyk")
    data_utworzenia = Column(DateTime, default=datetime.now)

class PrzedmiotyKoszyka(Base):
    __tablename__ = "przemioty_koszyka"

    id = Column(Integer, primary_key=True, autoincrement=True)
    koszyk_id = Column(Integer, ForeignKey("koszyk.id", ondelete="CASCADE"))
    film_id = Column(Integer, ForeignKey(Film.id, ondelete="CASCADE"))
    koszyk = relationship("Koszyk", back_populates="przedmioty_koszyka")
    filmy = relationship("Film", back_populates="przedmioty_koszyka")
    data_utworzenia = Column(DateTime, default=datetime.now)

