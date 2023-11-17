from fastapi import APIRouter
from typing import Awaitable
from fastapi import Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from FastApiProjekt.auth.router import get_current_user_from_token
from FastApiProjekt import db


templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/user/detail")
async def detail(request: Request, database: Session = Depends(db.get_db)):
    user = await get_current_user_from_token(token = request, database=database)
    return templates.TemplateResponse(
        "user/detail.html", {"request": request, "user": user}
    )

