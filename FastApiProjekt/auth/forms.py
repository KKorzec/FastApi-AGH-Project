from typing import List
from typing import Optional

from fastapi import Request


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.username = None
        self.password = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get("username")  # since outh works on username field we are considering email as username
        self.password = form.get("password")

    async def is_valid(self):
        if not self.username:
            self.errors.append("Musisz podać login")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("Hasło powinno mieć 4 znaki")
        if not self.errors:
            return True
        return False
