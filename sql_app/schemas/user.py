from pydantic import BaseModel
from schemas.roles import Roles

class UserIn(BaseModel):
    name: str
    email: str
    password: str

class UserTest(BaseModel):
    name: str