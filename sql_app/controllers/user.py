from fastapi import APIRouter,File, UploadFile, Depends,Form
from database import get_db
from services.user import *
from sqlalchemy.orm import Session
from schemas.user import UserTest
from schemas.user import UserIn

user_router = APIRouter( prefix="/user", tags=["user"])

service = UserService()

@user_router.post("/signup")
async def signup(
    user : UserIn,
    db: Session = Depends(get_db)):
    return service.signup(user,db)
