from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class DuvidasUpdateModel(BaseModel):
    titulo: Optional[str] = None
    mensagem: Optional[str] = None
    autor: Optional[str] = None
    email: Optional[str] = None
    visualizacoes: Optional[List[str]] = None
    postado: Optional[bool] = None
    resposta: Optional[str] = None
    data_de_envio: Optional[datetime] = None
    data_de_postagem: Optional[datetime] = None
