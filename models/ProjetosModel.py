from typing import List, Optional

from pydantic import BaseModel


class ProjetosModel(BaseModel):

    id : str
    titulo : str
    tema : str
    palavras_chave : List[str]
    descricao : str
    cliente : str
    semestre : str
    equipe : List
    link_repositorio : str
    tecnologias_utilizadas : List[str]
    video_tecnico : str
    pitch : str
    revisado: str = "Pendente"
    curtidas: int = 0
    user_curtidas_email: List[str] = []
    comentarios: List[str] = []
   
    
    def toMaps(self):
        return {
            "id" : self.id,
            "titulo" : self.titulo,
            "tema" : self.tema,
            "palavras_chave" : self.palavras_chave,
            "descricao" : self.descricao,
            "cliente" : self.cliente,
            "semestre" : self.semestre,
            "equipe" : self.equipe,
            "link_repositorio" : self.link_repositorio,
            "tecnologias_utilizadas" : self.tecnologias_utilizadas,
            "video_tecnico" : self.video_tecnico,
            "pitch" : self.pitch,
            "revisado": self.revisado,
            "curtidas": self.curtidas,
            "user_curtidas_email": self.user_curtidas_email,
            "comentarios": self.comentarios
            }
        
    def getKeyDoc(self):
        return self.id
    
    
    '''
{
    "id": "AUTO_INCREMENT",
    "titulo": "E-comp teste",
    "tema": "Engenharia de Software",
    "palavras_chave": "Engenharia;Mestrado;RESP API;FastApi",
    "descricao": "Esse em documento de teste",
    "cliente": "Denis",
    "semestre": "2024.1",
    "equipe": "Adjailson Ferreira;João Victor;Emerson Ferreira;Cynthia Oliveira;José Carlos;Arthur Xavier;Ana Karla",
    "link_repositorio": "https://github.com/adjailsonferreira/repository_egs_poli",
    "tecnologias_utilizadas": "Python;FastApi;React.js;Firebase;Firestore;MVC",
    "video_tecnico": "https://www.youtube.com/watch?v=wRca2IMJVVk",
    "pitch": "https://www.youtube.com/watch?v=wRca2IMJVVk"
}

    '''