from typing import List, Optional

from pydantic import BaseModel

class ArtigosModel(BaseModel):
     
    id: str
    titulo: str
    descricao: str
    equipe: List[str]
    tema: str
    data: str
    palavras_chave: List[str]
    arquivo: str
    revisado: str = "Pendente"
    resumo: str
    
    def toMaps(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "equipe": self.equipe,
            "tema": self.tema,
            "data": self.data,
            "palavras_chave": self.palavras_chave,
            "arquivo": self.arquivo,
            "revisado": self.revisado,
            "resumo": self.resumo
        }

    def getKeyDoc(self):
        return self.id
    
    