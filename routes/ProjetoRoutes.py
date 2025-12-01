from fastapi import APIRouter, Form, HTTPException, UploadFile, File, Path, Body, Depends, Request, Query
from controllers.ProjetosController import ProjetosController
from controllers.StorageController import StorageController
from models.ProjetosModel import ProjetosModel
from models.ProjetosUpdateModel import ProjetosUpdateModel
import os
from utils.checkAdminUser import check_if_admin, check_if_login
from typing import Optional, List
from pydantic import BaseModel

router = APIRouter()

###PROJETOS
@router.post("/projeto_add/", dependencies=[Depends(check_if_login)])
def inserir_Projeto(dados:ProjetosModel):
    return ProjetosController().setProjeto(dados)

@router.post("/upload_logo_projeto/{id_projeto}/", dependencies=[Depends(check_if_login)])
async def upload_logo_projeto(id_projeto: str, file: UploadFile = File(...)):
    # Garante que o diretório existe
    os.makedirs('uploads/projetos', exist_ok=True)
    
    # CORREÇÃO: Removida a barra '/' do final do caminho
    temp_file_path = f'uploads/projetos/{file.filename}'
    
    try:
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(await file.read())

        saida = StorageController().upload_logo_projeto(id_projeto, temp_file_path)
        return saida
    except Exception as e:
        return {"erro": f"Erro no upload: {str(e)}"}
    finally:
        # Remove o arquivo temporário se ele foi criado
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


### ========= ADD IMAGENS AO PROJETO ==================
@router.post("/projetos/{id}/imagens/", dependencies=[Depends(check_if_login)])
def adicionar_imagens_ao_projeto(
    id: str = Path(..., description="ID do projeto"),
    files: List[UploadFile] = File(..., description="Uma ou mais imagens para upload")
):
    """
    CRIAÇÃO: Adiciona uma ou mais imagens a um projeto.
    """
    if not files or all(not f.filename for f in files):
        raise HTTPException(status_code=400, detail="Nenhum arquivo enviado.")
        
    # Chama o novo método no seu controller
    return ProjetosController().adicionar_imagens_projeto(projeto_id=id, files=files)

class ImagemUrlModel(BaseModel):
    imagem_url: str

@router.delete("/projetos/{id}/imagem/", dependencies=[Depends(check_if_login)])
def remover_imagem_do_projeto(
    id: str = Path(..., description="ID do projeto"),
    dados: ImagemUrlModel = Body(..., description="JSON contendo a URL da imagem a ser removida")
):
    """
    EDIÇÃO: Remove uma imagem específica da lista do projeto.
    """
    if not dados.imagem_url:
        raise HTTPException(status_code=400, detail="URL da imagem é obrigatória.")
        
    # Chama o novo método no seu controller
    return ProjetosController().remover_imagem_projeto(
        projeto_id=id, 
        imagem_url=dados.imagem_url
    )

### ========= ADD IMAGENS AO PROJETO ==================


@router.post("/upload_fotos_integrantes/", dependencies=[Depends(check_if_login)])
async def upload_fotos_integrantes(files: List[UploadFile] = File(...), file_ids: List[str] = Form(...)):
    os.makedirs('uploads/projetos', exist_ok=True)
    
    saidas = []
    
    # Itera sobre os arquivos e seus IDs correspondentes
    for index, file in enumerate(files):
        # Proteção caso a lista de IDs seja menor que a de arquivos
        if index >= len(file_ids):
            break
            
        file_id = file_ids[index]
        
        temp_file_path = f'uploads/projetos/{file.filename}'
        
        try:
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(await file.read())
            
            saida = StorageController().upload_fotos_integrantes(temp_file_path, file_id)
            if saida:
                saidas.append(saida)
        except Exception as e:
            print(f"Erro ao subir foto {file.filename}: {e}")
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    if len(saidas) > 0:
        return saidas
    else:
        return {"erro": "Nenhuma foto foi salva."}
    
@router.get("/view_fotos_integrantes/{id_foto}/")
async def view_fotos_integrantes(id_foto: str):
    if id_foto == 'null': return {'url':None}
    return StorageController().view_fotos_integrantes(id_foto)

@router.put("/projetos/{id}/", dependencies=[Depends(check_if_admin)])
def atualizar_projeto(id: str, dados: ProjetosUpdateModel):
    # Converte os dados para um dicionário, ignorando campos não enviados
    dados_dict = dados.dict(exclude_unset=True)
    # Adiciona o ID ao dicionário de dados
    if dados_dict:
        dados_dict["id"] = id
    else:
        raise HTTPException(status_code=400, detail="Nenhum dado fornecido para atualização.")
    return ProjetosController().updateProjeto(dados_dict)

""" @router.delete("/delete_projeto/{titulo}", dependencies=[Depends(check_if_login)])
def delete_Projeto(titulo:str):
    projeto = ProjetosController()
    return projeto.deleteProjeto(titulo) """

@router.delete("/projetos/{id}/", dependencies=[Depends(check_if_admin)])
def deletar_projeto(id: str):
    return ProjetosController().deleteProjeto(id)

@router.get("/projetos/")
def listar_projetos():
    return ProjetosController().getProjetos()

@router.get("/projetos/{id}/")
def obter_projeto(id: str):
    projeto = ProjetosController().getProjetoId(id)
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    return projeto

@router.get("/view_logo_projeto/{id_projeto}/")
async def view_logo_projeto(id_projeto: str):
    return StorageController().view_logo_projeto(id_projeto)

@router.get("/filtrar_projetos/")
def filtrar_projetos(
    semestre: Optional[str] = None,
    titulo: Optional[str] = None,
    tecnologias_utilizadas: Optional[List[str]] = Query(None),
    tema: Optional[str] = None,
    palavras_chave: Optional[List[str]] = Query(None),
    equipe: Optional[List[str]] = Query(None),
    id: Optional[str] = None
):

    controller = ProjetosController()
    filtros = {}

    if semestre:
        filtros["semestre"] = semestre
    if titulo:
        filtros["titulo"] = titulo
    if tecnologias_utilizadas:
        filtros["tecnologias_utilizadas"] = tecnologias_utilizadas
    if tema:
        filtros["tema"] = tema
    if palavras_chave:
        filtros["palavras_chave"] = palavras_chave
    if equipe:
        filtros["equipe"] = equipe
    if id:
        filtros["id"] = id
    if filtros:
        return controller.getProjetoFiltroMultiplos(filtros)
    else:
        return {"msg": "Nenhum filtro foi fornecido."}



@router.get("/projetos_pendentes/", dependencies=[Depends(check_if_admin)])
def pendentes():
    projeto = ProjetosController()
    return projeto.getProjetosPendentes()

@router.get("/projetos_aprovados/", dependencies=[Depends(check_if_admin)])
def aprovados():
    projeto = ProjetosController()
    return projeto.getProjetosAprovados()

@router.get("/projetos_reprovados/", dependencies=[Depends(check_if_admin)])
def reprovados():
    projeto = ProjetosController()
    return projeto.getProjetosReprovados()

@router.put("/projeto_revisado/{id}/", dependencies=[Depends(check_if_admin)])
async def atualizar_projetos_revisados(id: str, novo_revisado: str):
    projeto = ProjetosController()
    return projeto.updateRevisadoProjetos(id, novo_revisado)

@router.get("/projetos/{id}/status/")
def ver_status_projeto(id: str):
    projeto_controller = ProjetosController()
    status = projeto_controller.getStatusProjeto(id)
    if not status:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    return status


@router.post("/projetos/{id}/curtir/", dependencies=[Depends(check_if_login)])
def curtir_projeto(id: str, decoded_token=Depends(check_if_login)):
    email_usuario = decoded_token.get("email")
    projeto_controller = ProjetosController()
    resultado = projeto_controller.curtir_projeto(id, email_usuario)

    if resultado.get("msg") == "Projeto não encontrado!":
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    return resultado

@router.post("/projetos/{id}/comentar/", dependencies=[Depends(check_if_login)])
def comentar_projeto(id: str, usuario: str, comentario: str):
    projeto_controller = ProjetosController()
    resultado = projeto_controller.comentar_projeto(id, usuario, comentario)

    if resultado.get("msg") == "Projeto não encontrado!":
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    return resultado

class ComentarioDeleteModel(BaseModel):
    username: str
    comentario: str
    data: str

@router.post("/projetos/{id}/comentar/", dependencies=[Depends(check_if_login)])
def comentar_projeto(id: str, usuario: str, comentario: str):
    projeto_controller = ProjetosController()
    resultado = projeto_controller.comentar_projeto(id, usuario, comentario)

    if resultado.get("msg") == "Projeto não encontrado!":
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    return resultado

@router.delete("/projetos/{id}/comentar/", dependencies=[Depends(check_if_login)])
def deletar_comentario(
    id: str, 
    dados: ComentarioDeleteModel, 
    # O id_token é pego automaticamente pelo Depends(check_if_login) via query param
):
    # Converte o modelo Pydantic para dicionário simples
    comentario_dict = dados.dict()
    return ProjetosController().deletar_comentario_projeto(id, comentario_dict)
