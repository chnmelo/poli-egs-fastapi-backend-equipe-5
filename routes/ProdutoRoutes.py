from typing import Optional, List

from fastapi import APIRouter, HTTPException, UploadFile, File, Request, Depends, Query
from controllers.ProdutosController import ProdutosController
from models.ProdutosModel import ProdutosModel
from models.ProdutosUpdateModel import ProdutosUpdateModel
import os
from controllers.StorageController import StorageController
from utils.checkAdminUser import check_if_admin, check_if_login

router = APIRouter()

###ARTIGOS

@router.post("/produtos_add/", dependencies=[Depends(check_if_login)])
def criar_produto(dados: ProdutosModel):
    return ProdutosController().setProduto(dados)

@router.get("/produtos/")
def listar_produtos():
    return ProdutosController().getProdutos()

@router.get("/produtos/{id}/")
def obter_produto(id: str):
    produto = ProdutosController().getProdutoId(id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@router.put("/produtos/{id}/", dependencies=[Depends(check_if_admin)])
def atualizar_produto(id: str, dados: ProdutosUpdateModel):
    # Converte os dados para dicionário, ignorando campos que não foram fornecidos
    dados_dict = dados.dict(exclude_unset=True)
     # Adiciona o ID ao dicionário de dados
    if dados_dict:
        dados_dict["id"] = id
    else:
        raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização.")
    return ProdutosController().updateProduto(dados_dict)

@router.delete("/produtos/{id}/", dependencies=[Depends(check_if_admin)])
def deletar_produto(id: str):
    return ProdutosController().deleteProduto(id)

@router.post("/upload_pdf_produto/{id_produto}")
async def upload_produto(id_produto: str, file: UploadFile = File(...)):
    try:
        return StorageController().upload_pdf_artigo(id_produto, file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao fazer upload do arquivo: {str(e)}")

@router.get("/view_pdf_produto/{id_produto}")
async def view_pdf_produto(id_produto: str):
    return StorageController().view_pdf_artigo(id_produto)

@router.get("/produtos_pendentes", dependencies=[Depends(check_if_admin)])
def pendentes():
    produto = ProdutosController()
    return produto.getProdutosPendentes()

@router.get("/produtos_aprovados", dependencies=[Depends(check_if_admin)])
def aprovados():
    produto = ProdutosController()
    return produto.getProdutosAprovados()

@router.get("/produtos_reprovados", dependencies=[Depends(check_if_admin)])
def reprovados():
    produto = ProdutosController()
    return produto.getProdutosReprovados()

@router.put("/produto_revisado/{id}/", dependencies=[Depends(check_if_admin)])
async def atualizar_produtos_revisados(id: str, novo_revisado: str):
    produto = ProdutosController()
    return produto.updateStatusProduto(id, novo_revisado)

@router.get("/filtrar_produtos/")
def filtrar_produtos(
    id: Optional[str] = None,
    titulo: Optional[str] = None,
    equipe: Optional[List[str]] = Query(None),
    tipo: Optional[str] = None,
    semestre: Optional[str] = None,
):
    print(f"Id: {id}, Título: {titulo}, Equipe: {equipe}, Tipo: {tipo}, Semestre: {semestre}")

    controller = ProdutosController()
    filtros = {}

    if id:
        filtros["id"] = id
    if titulo:
        filtros["titulo"] = titulo
    if equipe:
        filtros["equipe"] = equipe
    if tipo:
        filtros["tipo"] = tipo
    if semestre:
        filtros["semestre"] = semestre
    if filtros:
        return controller.getProdutoFiltroMultiplos(filtros)
    else:
        return {"msg": "Nenhum filtro foi fornecido."}
