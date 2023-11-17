from FastApiProjekt.filmy import router as frouter
from FastApiProjekt.user import router as urouter
from FastApiProjekt.auth import router as lrouter
from fastapi import APIRouter


api_router = APIRouter()
api_router.include_router(frouter.router, prefix="", tags=["film-webapp"])
api_router.include_router(urouter.router, prefix="", tags=["user-webapp"])
api_router.include_router(lrouter.router, prefix="", tags=["login-webapp"])
