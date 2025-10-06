from controllers.ConexaoFirestore import ConexaoFirestore
from models.DuvidasModel import DuvidasModel
from utils.MD5 import MD5
import datetime, os
from fastapi import HTTPException

class DuvidasController(ConexaoFirestore):

    def __init__(self):
        self.db = ConexaoFirestore.conect(self)
        #self.upload_directory = "uploads/duvidas"  
        #os.makedirs(self.upload_directory, exist_ok=True)

    def setDuvida(self, dados: DuvidasModel):
        try:
            key_doc = MD5(dados=dados.titulo).encrypt() # título é chave única
            dados.id = key_doc
            docs = self.db.collection('duvidas').document(key_doc)

            if docs.get().exists:
                raise HTTPException(status_code=400, detail="Tema já registrado, informe outro tema")
            
            write_result = docs.set(dados.toMaps())
            duvida = self.db.collection('duvidas').document(key_doc).get().to_dict()
            return {'msg': f'Sucesso!\n{write_result.update_time}, key={key_doc}', 'duvida': duvida }
        except Exception as e:
            raise e
            #return {'msg': f'Houve um erro! {e}'}
        
    def updatePostadoDuvidas(self, id: str):
        try:
            duvidas_ref = self.db.collection('duvidas').document(id)
            postado_status = duvidas_ref.get().get('postado')
            duvidas_ref.update({"postado": not postado_status, "data_de_postagem": datetime.datetime.now(tz=datetime.timezone.utc)})
            return {"msg": f"Postado '{postado_status}' atualizado para '{not postado_status}' na dúvida {id}"}
        except Exception as e:
            print(f"Erro ao atualizar o status: {e}")
            return {"msg": f"Erro ao atualizar o status: {e}"}
    
    def updateVisualizacoesDuvidas(self, id: str, email: str):
        try:
            duvidas_ref = self.db.collection('duvidas').document(id)
            visualizacoes = duvidas_ref.get().get('visualizacoes')
            visualizacoes.append(email)
            duvidas_ref.update({"visualizacoes": visualizacoes})
            return {"msg": f"Visualizacoes atualizado para '{visualizacoes}' na dúvida {id}"}
        except Exception as e:
            print(f"Erro ao atualizar o status: {e}")
            return {"msg": f"Erro ao atualizar o status: {e}"}

    def getDuvidas(self):
        try:
            docs = self.db.collection('duvidas').stream()
            duvidas = []
            for duvida in docs:
                duvidas.append(duvida.to_dict())
            if duvidas:
                return {'msg': 'Sucesso ao listar!','total de duvidas': len(duvidas) , 'duvidas': duvidas }
            else:
                return {"msg": "Sem duvidas!"}
        except Exception as e:
            return {"msg": f"Erro ao atualizar o status postado: {e}"}

    def updateDuvida(self, dados: DuvidasModel):
        try:
            if not dados:
                return {'msg': 'Nenhum campo para atualizar.', 'projeto': None}

            doc_ref = self.db.collection('duvidas').document(dados.get("id"))
            write_result = doc_ref.set(dados, merge=True)
            duvida = doc_ref.get().to_dict()
            return {
                'msg': f'Sucesso! Documento atualizado em {write_result.update_time}',
                'duvida': duvida
            }
        except Exception as e:
            return {'msg': f'Houve um erro! {e}'}

    def deleteDuvida(self, id: str):
        try:
            duvida = self.db.collection('duvidas').document(id).get().to_dict()
            self.db.collection("duvidas").document(id).delete()
            return {'msg': 'Sucesso ao deletar!', 'duvida': duvida }
        except Exception as e:
            return {'msg': f'Houve um erro! {e}'}