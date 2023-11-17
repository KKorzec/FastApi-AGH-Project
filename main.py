import uvicorn
from celery import Celery
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from FastApiProjekt.user import router as user_router
from FastApiProjekt.user.schema import logowanie
from FastApiProjekt.filmy import router as filmy_router
from FastApiProjekt.koszyk import router as koszyk_router
from FastApiProjekt.zamowienia import router as zamowienia_router
from FastApiProjekt.auth import router as auth_router
from FastApiProjekt.api.general_pages.route_homepage import general_pages_router
from FastApiProjekt.webapps.film import route_film as frouter
from FastApiProjekt import config

app = FastAPI(title="Wypozyczalnia filmow", description="Wypozyczalnia w REST API", version='0.1a')
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_router.router)
app.include_router(filmy_router.router)
app.include_router(koszyk_router.router)
app.include_router(zamowienia_router.router)
app.include_router(auth_router.router)
app.include_router(frouter.router)

#Webówka
def include_router(app):
    app.include_router(general_pages_router)

#Celery i Redis
celery = Celery(
    __name__,
    broker=f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}/{config.REDIS_DB}",
    backend=f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}/{config.REDIS_DB}"
)

celery.conf.imports = [
    'FastApiProjekt.zamowienia.tasks'
]


@app.get('/')
def hello_world(request: Request):
    return templates.TemplateResponse("shared/base.html", {"request": request})


# Prosty endpoint na próbę z wyświetleniem ID przedmiotu zadanego w URI
@app.get("/przedmiot")
@app.get("/przedmiot/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id=None):
    return templates.TemplateResponse("general_pages/item.html", {"request": request, "id": id})


# Próba zrobienia formularza logowania - tutaj i w user/services
#@app.get("/login", response_class=HTMLResponse)
#def get_login(request: Request):
#    return templates.TemplateResponse("general_pages/login.html", {"request": request})


#@app.post("/login", response_class=HTMLResponse)
#def post_login(request: Request, form_data: logowanie = Depends(logowanie.as_form)):
#    print(form_data)
#    return templates.TemplateResponse("general_pages/login.html", context={"request": request})


#Próba zrobienia wyświetlania filmów
@app.get("/tytuly")
@app.get("/tytuly", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("general_pages/homepage.html", {"request": request})


if __name__ == '__main__':
    uvicorn.run(app)
