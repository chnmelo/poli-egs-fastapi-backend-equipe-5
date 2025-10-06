from typing import List, Optional

from pydantic import BaseModel


class ProdutosModel(BaseModel):
    id: str
    titulo: str
    descricao: str
    equipe: List[str]
    tipo: str
    arquivo: str
    status: str = "Pendente"
    semestre: str

    def toMaps(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "equipe": self.equipe,
            "tipo": self.tipo, #
            "semestre": self.semestre, #
            "arquivo": self.arquivo,
            "status": self.status
        }

    def getKeyDoc(self):
        return self.id

