from fastapi import FastAPI
from controller.entrevista_controller import *
import models
from database import engine
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173/"],  # As origens que podem acessar este servidor
    allow_credentials=True,
    allow_methods=[""],  # Métodos HTTP permitidos
    allow_headers=[""],  # Cabeçalhos HTTP permitidos
)
app.include_router(entrevista_router)
