from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def weryfikacja(proste_haslo, hash_haslo):
    return pwd_context.verify(proste_haslo, hash_haslo)


def hashuj(haslo):
    return pwd_context.hash(haslo)
