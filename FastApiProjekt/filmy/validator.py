from sqlalchemy.orm import Session
from . models import Gatunek
from typing import Optional


async def zweryfikuj_gatunek(gatunek_id, db_session: Session) -> Optional[Gatunek]:
    return db_session.query(Gatunek).filter(Gatunek.id == gatunek_id).first()