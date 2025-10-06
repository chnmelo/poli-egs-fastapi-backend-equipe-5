from typing import Optional, List

from fastapi import APIRouter, HTTPException, UploadFile, File, Request, Depends, Query
from controllers.ArtigosController import ArtigosController
from models.ArtigosModel import ArtigosModel
from models.ArtigosUpdateModel import ArtigosUpdateModel
import os
from controllers.StorageController import StorageController
from utils.checkAdminUser import check_if_admin, check_if_login

router = APIRouter()

###ARTIGOS

@router.post("/artigos_add/",  dependencies=[Depends(check_if_login)])
def criar_artigo(dados: ArtigosModel):
    return ArtigosController().setArtigo(dados)

@router.get("/artigos/")
def listar_artigos():
    return ArtigosController().getArtigos()

@router.get("/artigos/{id}/")
def obter_artigo(id: str):
    artigo = ArtigosController().getArtigoId(id)
    if not artigo:
        raise HTTPException(status_code=404, detail="Artigo não encontrado")
    return artigo

""" @router.put("/artigos/{id}/", dependencies=[Depends(check_if_admin)])
def atualizar_artigo(id: str, dados: ArtigosModel):
    dados.id = id
    return ArtigosController().updateArtigo(dados) """

@router.put("/artigos/{id}/", dependencies=[Depends(check_if_admin)])
def atualizar_artigo(id: str, dados: ArtigosUpdateModel):
    # Converte os dados para dicionário, ignorando campos que não foram fornecidos
    dados_dict = dados.dict(exclude_unset=True)
     # Adiciona o ID ao dicionário de dados
    if dados_dict:
        dados_dict["id"] = id
    else:
        raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização.")
    return ArtigosController().updateArtigo(dados_dict)

@router.delete("/artigos/{id}/", dependencies=[Depends(check_if_admin)])
def deletar_artigo(id: str):
    return ArtigosController().deleteArtigo(id)

@router.post("/upload_pdf_artigo/{id_artigo}")
async def upload_artigo(id_artigo: str, file: UploadFile = File(...)):
    try:
        return StorageController().upload_pdf_artigo(id_artigo, file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao fazer upload do arquivo: {str(e)}")

@router.get("/view_pdf_artigo/{id_projeto}")
async def view_pdf_artigo(id_projeto: str):
    return StorageController().view_pdf_artigo(id_projeto)

@router.get("/artigos_pendentes", dependencies=[Depends(check_if_admin)])
def pendentes():
    artigo = ArtigosController()
    return artigo.getArtigosPendentes()

@router.get("/artigos_aprovados", dependencies=[Depends(check_if_admin)])
def aprovados():
    artigo = ArtigosController()
    return artigo.getArtigosAprovados()

@router.get("/artigos_reprovados", dependencies=[Depends(check_if_admin)])
def reprovados():
    artigo = ArtigosController()
    return artigo.getArtigosReprovados()

@router.put("/artigo_revisado/{id}/", dependencies=[Depends(check_if_admin)])
async def atualizar_artigos_revisados(id: str, novo_revisado: str):
    artigo = ArtigosController()
    return artigo.updateRevisadoArtigo(id, novo_revisado)

@router.get("/filtrar_artigos/")
def filtrar_artigos(
    id: Optional[str] = None,
    titulo: Optional[str] = None,
    equipe: Optional[List[str]] = Query(None),
    tema: Optional[str] = None,
    data: Optional[str] = None,
    palavras_chave: Optional[List[str]] = Query(None)


):
    print(f"Id: {id}, Título: {titulo}, Equipe: {equipe}, Tema: {tema}, Data: {data}, Palavras-chave: {palavras_chave}")

    controller = ArtigosController()
    filtros = {}

    if id:
        filtros["id"] = id
    if titulo:
        filtros["titulo"] = titulo
    if equipe:
        filtros["equipe"] = equipe
    if tema:
        filtros["tema"] = tema
    if palavras_chave:
        filtros["palavras_chave"] = palavras_chave
    if data:
        filtros["data"] = data

    if filtros:
        return controller.getArtigoFiltroMultiplos(filtros)
    else:
        return {"msg": "Nenhum filtro foi fornecido."}


