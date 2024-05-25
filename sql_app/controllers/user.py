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

@user_router.post("/token")
async def token(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)):
    user = service.authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@user_router.get("/me")
async def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    current_user = service.get_current_user(db, token)
    return current_user
