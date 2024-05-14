from fastapi import FastAPI
from controllers.entrevista_controller import *
import models_ as models_
from database import engine
from fastapi.middleware.cors import CORSMiddleware
from controllers.user import *
from models import user

models_.Base.metadata.create_all(bind=engine)
user.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # As origens que podem acessar este servidor
    allow_credentials=True,
    allow_methods=["*"],  # Métodos HTTP permitidos
    allow_headers=["*"],  # Cabeçalhos HTTP permitidos
)
app.include_router(entrevista_router)
app.include_router(user_router)
