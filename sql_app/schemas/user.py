from pydantic import BaseModel
from schemas.roles import Roles

class UserIn(BaseModel):
    name: str
    email: str
    password: str

class UserTest(BaseModel):
    name: str

class UserOut(BaseModel):
    name: str
    email: str
    role: Roles
    is_active: bool
    id: int
    