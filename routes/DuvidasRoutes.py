from fastapi import APIRouter, HTTPException, UploadFile, File, Request, Depends, Query
from controllers.DuvidasController import DuvidasController
from models.DuvidasModel import DuvidasModel
from models.DuvidasUpdateModel import DuvidasUpdateModel
from utils.checkAdminUser import check_if_admin, check_if_login

router = APIRouter()

### DÚVIDAS/SUGESTÓES

@router.post("/duvidas_add/")
def criar_duvida(dados: DuvidasModel):
    return DuvidasController().setDuvida(dados)

@router.get("/duvidas/")
def listar_duvidas():
    return DuvidasController().getDuvidas()

@router.put("/duvida_publicado/{id}/", dependencies=[Depends(check_if_admin)])
async def publicacao_duvida(id: str):
    return DuvidasController().updatePostadoDuvidas(id)

@router.put("/duvidas/{id}/")
def atualizar_duvida(id: str, dados: DuvidasUpdateModel):
    dados_dict = dados.dict(exclude_unset=True)
    if dados_dict:
        dados_dict["id"] = id
    else:
        raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização.")
    return DuvidasController().updateDuvida(dados_dict)

@router.delete("/duvidas/{id}/")
def deletar_duvida(id: str):
    return DuvidasController().deleteDuvida(id)
  
@router.put("/duvida_visualizacao/{id}/{email}/", dependencies=[Depends(check_if_admin)])
async def visualizacao_duvida(id: str, email: str):
    return DuvidasController().updateVisualizacoesDuvidas(id, email)
