from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from controllers.UserController import UserController
from models.UserModel import UserModel
import os
from pydantic import BaseModel 
from typing import Optional
from firebase_admin import auth as admin_auth
from routes import (
    UserRoutes, 
    ProjetoRoutes, 
    ArtigoRoutes, 
    ProdutoRoutes, 
    DuvidasRoutes, 
    AdminRoutes
)
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="API - UPE Projetos e-comp de EGS",
    version="1.0.1",
    description="RESP API ecomp - Disciplina de Engenharia da Computação - 2024.2",
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "https://www.observatorio.poli.br",
    "https://observatorio.poli.br",
    "*"
]


#Corpo da requisição, informação enviada pelo cliente para a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UserRoutes.router)
app.include_router(ProjetoRoutes.router)
app.include_router(ArtigoRoutes.router)
app.include_router(ProdutoRoutes.router)
app.include_router(DuvidasRoutes.router)
app.include_router(AdminRoutes.router)
