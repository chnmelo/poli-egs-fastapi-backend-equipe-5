from typing import List, Optional
from pydantic import BaseModel

class ProjetosUpdateModel(BaseModel):
    titulo: Optional[str] = None
    tema: Optional[str] = None
    palavras_chave: Optional[List[str]] = None
    descricao: Optional[str] = None
    cliente: Optional[str] = None
    semestre: Optional[str] = None
    equipe: Optional[List] = None
    link_repositorio: Optional[str] = None
    tecnologias_utilizadas: Optional[List[str]] = None
    video_tecnico: Optional[str] = None
    pitch: Optional[str] = None
    revisado: Optional[str] = None
    curtidas: Optional[int] = None
    user_curtidas_email: Optional[List[str]] = None
    comentarios: Optional[List] = None
