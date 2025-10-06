from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from controllers.UserController import UserController
from models.UserModel import UserModel
import os
from firebase_admin import auth as admin_auth
from routes.ProjetoRoutes import router as projeto_router
from routes.ArtigoRoutes import router as artigo_router
from routes.UserRoutes import router as user_router
from routes.ProdutoRoutes import router as produto_router
from routes.DuvidasRoutes import router as duvida_router

app = FastAPI(
    title="API - UPE Projetos e-comp de EGS",
    version="0.0.1",
    description="RESP API ecomp - Disciplina de Engenharia da Computação - 2024.2",
)

#Métodos ou ENDPOINT da RESP API

#Login dos admin
""" @app.post("/login/")
def login(login_data: UserModel):
    user = UserController()
    return user.login(login_data.username, login_data.password) """

#Corpo da requisição, informação enviada pelo cliente para a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
# app.include_router(projeto_router, prefix="/projetos")
app.include_router(produto_router)
app.include_router(projeto_router)
app.include_router(artigo_router)
app.include_router(user_router)
app.include_router(duvida_router)
