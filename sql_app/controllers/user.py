from fastapi import APIRouter,File, UploadFile, Depends,Form
from database import get_db
from services.user import *
from sqlalchemy.orm import Session
from schemas.user import UserTest

user_router = APIRouter( prefix="/user", tags=["user"])

service = UserService()

@user_router.post("/signup")
async def signup(
    user : UserTest,
    # nome : str = Form(...),
    #              email: str = Form(...),
    #              assinatura: str = Form(...),
    #              db: Session = Depends(get_db)
    db: Session = Depends(get_db)):
    return service.signup(user,db)
