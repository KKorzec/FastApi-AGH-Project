from fastapi import Request
from fastapi.templating import Jinja2Templates
from FastApiProjekt.auth.forms import LoginForm
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from . import schema
from . import jwt as pomoc

from FastApiProjekt import db
from FastApiProjekt.user import hash
from FastApiProjekt.user.models import User

from .jwt import create_access_token
templates = Jinja2Templates(directory="templates")
router = APIRouter()

router = APIRouter(
    tags=['autoryzacja']
)


@router.get("/login/log")
def login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login/log")
async def login(request: Request, database: Session = Depends(db.get_db)):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            form.__dict__.update(msg="Login Successful :)")
            response = templates.TemplateResponse("auth/login.html", form.__dict__)
            login2(request=form, database=database)
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("auth/login.html", form.__dict__)
    return templates.TemplateResponse("auth/login.html", form.__dict__)


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), database: Session = Depends(db.get_db)):
    user = database.query(User).filter(User.email == request.username or User.login == request.username).first()
    look = hash.weryfikacja(request.password, user.haslo)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Nie ma takiego użytkownika')
    if not look:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Niepoprawne hasło')

    # Generate a JWT Token
    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/login2')
def login2(request: LoginForm = Depends(), database: Session = Depends(db.get_db)):
    user = database.query(User).filter(User.email == request.username or User.login == request.username).first()
    look = hash.weryfikacja(request.password, user.haslo)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Nie ma takiego użytkownika')
    if not look:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Niepoprawne hasło')

    # Generate a JWT Token
    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.get('/login/get')
def get_current_user_from_token(token: str = Depends(oauth2_scheme), database: Session = Depends(db.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, pomoc.SECRET_KEY, algorithms=[pomoc.ALGORITHM])
        username: str = payload.get("sub")
        print("username/email extracted is ", username)
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = schema.TokenData(username=login)
    if user is None:
        raise credentials_exception
    return username
