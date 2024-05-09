from pydantic import BaseModel
from enum import Enum

class Roles(str, Enum):
    admin = 'admin'
    premium = 'premium'
    free = 'free'
    