from controllers.ConexaoFirestore import ConexaoFirestore
from models.ArtigosModel import ArtigosModel
from utils.MD5 import MD5
import os
from fastapi.responses import FileResponse
from fastapi import HTTPException

class ArtigosController(ConexaoFirestore):

    def __init__(self):
        self.db = ConexaoFirestore.conect(self)
        self.upload_directory = "uploads/artigos"  
        os.makedirs(self.upload_directory, exist_ok=True)
        
    def setArtigo(self, dados: ArtigosModel):
        try:
            key_doc = MD5(dados=dados.titulo).encrypt() # título é chave única
            dados.id = key_doc
            dados.revisado = 'Pendente'
            docs = self.db.collection('artigos').document(key_doc)

            if docs.get().exists:
                raise HTTPException(status_code=400, detail="Título já cadastrado, informe outro título")

            write_result = docs.set(dados.toMaps())
            artigo = self.db.collection('artigos').document(key_doc).get().to_dict()
            return {'msg': 'Artigo criado com sucesso!', 'artigo': artigo }
        except Exception as e:
            raise e
        
    """ def updateArtigo(self, dados: ArtigosModel):
        try:
            docs = self.db.collection('artigos').document(dados.id)
            write_result = docs.set(dados.toMaps(), merge=True)
            artigo = self.db.collection('artigos').document(dados.id).get().to_dict()
            return {'msg': f'Sucesso!\n{write_result.update_time}', 'artigo': artigo }
        except Exception as e:
            return {'msg': f'Houve um erro! {e}'} """
    def updateArtigo(self, dados: ArtigosModel):
        try:
            # Certifique-se de que há campos para atualizar
            if not dados:
                return {'msg': 'Nenhum campo para atualizar.', 'projeto': None}
            
            doc_ref = self.db.collection('artigos').document(dados.get("id"))
            write_result = doc_ref.set(dados, merge=True)
            artigo = doc_ref.get().to_dict()
            return {
                'msg': f'Sucesso! Documento atualizado em {write_result.update_time}',
                'artigo': artigo
            }
        except Exception as e:
            return {'msg': f'Houve um erro! {e}'}

    def deleteArtigo(self, id: str):
        try:
            artigo = self.db.collection('artigos').document(id).get().to_dict()
            self.db.collection("artigos").document(id).delete()
            return {'msg': 'Sucesso ao deletar!', 'artigo': artigo }
        except Exception as e:
            return {'msg': f'Houve um erro! {e}'}

    def getArtigos(self):
        try:
            docs = self.db.collection('artigos').stream()
            artigos = []
            for artigo in docs:
                artigos.append(artigo.to_dict())
            if artigos:
                return {'msg': 'Sucesso ao listar!','total de artigos': len(artigos) , 'artigos': artigos }
            else:
                return {"msg": "Sem artigos!"}
        except Exception as e:
            return {'msg': f'Houve um erro! {e}'}
        
    def getArtigoId(self, id: str):
        try:
            artigo = self.db.collection('artigos').document(id).get()
            if artigo.exists:
                return {'artigo': artigo.to_dict()}
            else:
                return {"msg": "Não encontrado!"}
        except Exception as e:
            return {'msg': f'Houve um erro! {e}'}
        
    def upload_pdf(self, id: str, file):
        try:
            file_location = os.path.join(self.upload_directory, f"{id}.pdf")
            with open(file_location, "wb") as f:
                f.write(file.file.read())
            return {"msg": f"Arquivo '{file.filename}' salvo em '{file_location}'"}
        except Exception as e:
            return {'msg': f'Houve um erro ao salvar o arquivo! {e}'}

    def get_pdf(self, id: str):
        file_location = os.path.join(self.upload_directory, f"{id}.pdf")
        if os.path.isfile(file_location):
            return FileResponse(path=file_location, filename=f"{id}.pdf")
        else:
            return {"msg": "Arquivo não encontrado"}

    def getArtigosAprovados(self):
        try:
            query = self.db.collection('artigos').where("revisado", "==", "Aprovado")
            docs = query.stream()
            artigos_aprovados = [doc.to_dict() for doc in docs]
            return {"artigos_aprovados": artigos_aprovados}

        except Exception as e:
            print(f"Erro ao buscar artigos aprovados: {e}")
            return {"msg": f"Erro ao buscar artigos aprovados: {e}"}

    def getArtigosReprovados(self):
        try:
            query = self.db.collection('artigos').where("revisado", "==", "Reprovado")
            docs = query.stream()
            artigos_reprovados = [doc.to_dict() for doc in docs]
            return {"artigos_reprovados": artigos_reprovados}

        except Exception as e:
            print(f"Erro ao buscar artigos reprovados: {e}")
            return {"msg": f"Erro ao buscar artigos reprovados: {e}"}

    def getArtigosPendentes(self):
        try:
            query = self.db.collection('artigos').where("revisado", "==", "Pendente")
            docs = query.stream()
            artigos_pendentes = [doc.to_dict() for doc in docs]
            return {"artigos pendentes": artigos_pendentes}

        except Exception as e:
            print(f"Erro ao buscar artigos pendentes: {e}")
            return {"msg": f"Erro ao buscar artigos pendentes: {e}"}

    def updateRevisadoArtigo(self, id: str, novo_status: str):
        status_validos = {"Pendente", "Aprovado", "Reprovado"}
        if novo_status not in status_validos:
            return {"msg": f"Status inválido: {novo_status}. Status permitido: {status_validos}"}
        try:
            artigo_ref = self.db.collection('artigos').document(id)
            old_status = artigo_ref.get().get('revisado')
            artigo_ref.update({"revisado": novo_status})
            return {"msg": f"Status '{old_status}' atualizado para '{novo_status}' no artigo {id}"}
        except Exception as e:
            print(f"Erro ao atualizar o status revisado: {e}")
            return {"msg": f"Erro ao atualizar o status revisado: {e}"}

    def getArtigoFiltroMultiplos(self, filtros: dict):
        try:
            query = self.db.collection('artigos')

            for campo, valor in filtros.items():
                if valor:
                    if campo == 'palavras_chave' or campo == 'equipe':
                        if isinstance(valor, list):
                            print(f"Aplicando filtro: {campo} contém algum dos valores {valor}")
                            query = query.where(campo, 'array_contains_any', valor)
                        else:
                            print(f"Aplicando filtro: {campo} contém {valor}")
                            query = query.where(campo, 'array_contains', valor)
                    else:
                        print(f"Aplicando filtro: {campo} == {valor}")
                        query = query.where(campo, '==', valor)

            docs = query.stream()
            artigos_filtrados = [doc.to_dict() for doc in docs]

            print(f"Artigos encontrados: {len(artigos_filtrados)}")
            if artigos_filtrados:
                return {"artigos": artigos_filtrados}
            else:
                return {"msg": "Nenhum artigo encontrado com os filtros fornecidos."}

        except Exception as e:
            print(f"Erro ao buscar artigos: {e}")
            return {"msg": f"Erro ao buscar artigos com filtros múltiplos: {e}"}