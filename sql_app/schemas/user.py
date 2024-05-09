from pydantic import BaseModel
from schemas.roles import Roles

class User(BaseModel):
    name: str
    email: str
    disabled: bool = False
    roles: Roles = Roles.free

class UserTest(BaseModel):
    name: str