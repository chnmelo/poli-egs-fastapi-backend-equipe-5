from typing import List, Optional
from pydantic import BaseModel

class ProdutosUpdateModel(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    equipe: Optional[List[str]] = None
    tipo: Optional[str] = None
    arquivo: Optional[str] = None
    status: Optional[str] = None
    semestre: Optional[str] = None
