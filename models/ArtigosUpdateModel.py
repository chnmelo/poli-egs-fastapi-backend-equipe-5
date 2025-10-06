from typing import List, Optional
from pydantic import BaseModel

class ArtigosUpdateModel(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    equipe: Optional[List[str]] = None
    tema: Optional[str] = None
    data: Optional[str] = None
    palavras_chave: Optional[List[str]] = None
    arquivo: Optional[str] = None
    revisado: Optional[str] = None
    resumo: Optional[str] = None
