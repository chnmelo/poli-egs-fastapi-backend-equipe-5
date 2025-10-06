from typing import List
from pydantic import BaseModel
from datetime import datetime

class DuvidasModel(BaseModel):
    id: str
    titulo: str
    mensagem: str
    autor: str
    email: str
    visualizacoes: List[str]
    postado: bool
    resposta: str
    data_de_envio: datetime
    data_de_postagem: datetime


    def toMaps(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "mensagem": self.mensagem,
            "autor": self.autor,
            "email": self.email,
            "visualizacoes": self.visualizacoes,
            "postado": self.postado,
            "resposta": self.resposta,
            "data_de_envio": self.data_de_envio,
            "data_de_postagem": self.data_de_postagem
        }

    def getKeyDoc(self):
        return self.id