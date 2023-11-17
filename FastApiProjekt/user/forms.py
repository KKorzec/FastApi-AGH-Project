from typing import List
from fastapi import Request
from datetime import date


class FormUtworzUzytkownika:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.login = None
        self.haslo = None
        self.email = None
        self.data_urodzenia = date.today()

    async def load_data(self):
        form = await self.request.form()
        self.login = form.get("login")
        self.haslo = form.get("haslo")
        self.email = form.get("email")
        self.data_urodzenia = form.get("data_urodzenia")

    async def is_valid(self):
        if not self.login or not len(self.login) > 3:
            self.errors.append("Nazwa użytkownika powinna mieć przynajmniej 3 znaki")
        if not self.haslo or not len(self.haslo) >= 4:
            self.errors.append("Haslo powinno mieć przynajmniej 4 znaki")
        if not self.email or not (self.email.__contains__("@")):
            self.errors.append("E-mail jest wymagany w poprawnej formie")
        if not self.data_urodzenia:
            self.errors.append("Wymagana data urodzenia")
        if not self.errors:
            return True
        return False
