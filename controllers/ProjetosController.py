from typing import List

from controllers.ConexaoFirestore import ConexaoFirestore
from models.ProjetosModel import ProjetosModel
from utils.MD5 import MD5
from fastapi import HTTPException
import datetime, os
#from google.cloud import storage

class ProjetosController(ConexaoFirestore):

    def __init__(self):
        self.db = ConexaoFirestore.conect(self)
        self.upload_directory = "uploads/projetos"  
        os.makedirs(self.upload_directory, exist_ok=True)

    def setProjeto(self, dados:ProjetosModel):
        try:
            key_doc = MD5(dados=dados.titulo).encrypt() # título é chave única
            dados.id = key_doc
            dados.revisado = 'Pendente'
            dados.curtidas = 0
            docs = self.db.collection('projetos').document(key_doc)

            if docs.get().exists:
                raise HTTPException(status_code=400, detail="Título já cadastrado, informe outro título")
                            
            write_result = docs.set(dados.toMaps())
            projeto = self.db.collection('projetos').document(key_doc).get().to_dict()
            return {'msg': f'Sucesso!\n{write_result.update_time}, key={key_doc}', 'projeto': projeto }
        except Exception as e:
            raise e
            #return {'msg': f'Houve um erro! {e}'}
        
    """     def updateProjeto(self, dados:ProjetosModel):
        try:
            docs = self.db.collection('projetos').document(dados.id)
            write_result = docs.set(dados.toMaps(),merge=True)
            projeto = self.db.collection('projetos').document(dados.id).get().to_dict()
            return {'msg':f'Sucesso!\n{write_result.update_time}', 'projeto': projeto }
        except Exception as e:
            return {'msg': f'Houve um erro! {str(e)}', 'erro': str(e)} """

    """     def updateProjeto(self, dados: dict):
        try:
            # Certifique-se de que há campos para atualizar
            if not dados:
                return {'msg': 'Nenhum campo para atualizar.', 'projeto': None}
            
            doc_ref = self.db.collection('projetos').document(dados.get("id"))
            write_result = doc_ref.set(dados, merge=True)
            projeto = doc_ref.get().to_dict()
            return {'msg': f'Sucesso! Documento atualizado em {write_result.update_time}', 'projeto': projeto}
        except Exception as e:
            return {'msg': f'Houve um erro! {str(e)}', 'erro': str(e)} """

    def updateProjeto(self, dados: ProjetosModel):
        try:
            # Certifique-se de que há campos para atualizar
            if not dados:
                return {'msg': 'Nenhum campo para atualizar.', 'projeto': None}
            
            doc_ref = self.db.collection('projetos').document(dados.get("id"))
            write_result = doc_ref.set(dados, merge=True)
            projeto = doc_ref.get().to_dict()
            return {
                'msg': f'Sucesso! Documento atualizado em {write_result.update_time}', 
                'projeto': projeto
            }
        except Exception as e:
            return {'msg': f'Houve um erro! {str(e)}', 'erro': str(e)}
    def deleteProjeto(self, id:str):
        try:
            projeto = self.db.collection('projetos').document(id).get().to_dict()
            self.db.collection("projetos").document(id).delete()
            return {'msg':f'Sucesso ao deletar!', 'projeto': projeto }
        except Exception as e:
            return {'msg':f'Houve um erro! Verifique se o nome do título tá correto.{e}'}

    def getProjetoId(self, id: str):
        try:
            doc = self.db.collection('projetos').document(id).get()
            if doc.exists:
                return doc.to_dict()  # Retorna apenas o projeto (sem chave extra 'projeto')
            else:
                raise HTTPException(status_code=404, detail="Projeto não encontrado")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao buscar projeto: {str(e)}")

    def getProjetos(self):
        try:
            docs = self.db.collection('projetos').stream()
            projetos = []
            for projeto in docs:
                projetos.append(projeto.to_dict())
            if len(projetos)>0:
                return {'msg': 'Sucesso ao listar!', 'total de projetos': len(projetos), 'projetos': projetos}
            else:
                return {"msg":"Sem projetos!"}
        except Exception as e:
            return {'msg': f'Houve um erro! {e}'}

    def getProjetoFiltroMultiplos(self, filtros: dict):
        try:
            query = self.db.collection('projetos')

            for campo, valor in filtros.items():
                if valor:
                    if campo == 'palavras_chave' or campo == 'tecnologias_utilizadas' or campo == 'equipe':
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
            projetos_filtrados = [doc.to_dict() for doc in docs]

            print(f"Projetos encontrados: {len(projetos_filtrados)}")
            if projetos_filtrados:
                return {"projetos": projetos_filtrados}
            else:
                return {"msg": "Nenhum projeto encontrado com os filtros fornecidos."}

        except Exception as e:
            print(f"Erro ao buscar projetos: {e}")
            return {"msg": f"Erro ao buscar projetos com filtros múltiplos: {e}"}

    def getProjetosPendentes(self):
        try:
            query = self.db.collection('projetos').where("revisado", "==", "Pendente")
            docs = query.stream()
            projetos_nao_revisados = [doc.to_dict() for doc in docs]
            return {"projetos_nao_revisados": projetos_nao_revisados}

        except Exception as e:
            print(f"Erro ao buscar projetos pendentes: {e}")
            return {"msg": f"Erro ao buscar projetos pendentes: {e}"}

    def getProjetosAprovados(self):
        try:
            query = self.db.collection('projetos').where("revisado", "==", "Aprovado")
            docs = query.stream()
            projetos_aprovados = [doc.to_dict() for doc in docs]
            return {"projetos_aprovados": projetos_aprovados}

        except Exception as e:
            print(f"Erro ao buscar projetos aprovados: {e}")
            return {"msg": f"Erro ao buscar projetos aprovados: {e}"}

    def getProjetosReprovados(self):
        try:
            query = self.db.collection('projetos').where("revisado", "==", "Reprovado")
            docs = query.stream()
            projetos_reprovados = [doc.to_dict() for doc in docs]
            return {"projetos_reprovados": projetos_reprovados}

        except Exception as e:
            print(f"Erro ao buscar projetos reprovados: {e}")
            return {"msg": f"Erro ao buscar projetos reprovados: {e}"}

    def updateRevisadoProjetos(self, id: str, novo_status: str):
        status_validos = {"Pendente", "Aprovado", "Reprovado"}
        if novo_status not in status_validos:
            return {"msg": f"Status inválido: {novo_status}. Status permitido: {status_validos}"}
        try:
            projetos_ref = self.db.collection('projetos').document(id)
            old_status = projetos_ref.get().get('revisado')
            projetos_ref.update({"revisado": novo_status})
            return {"msg": f"Status '{old_status}' atualizado para '{novo_status}' no projeto {id}"}
        except Exception as e:
            print(f"Erro ao atualizar o status revisado: {e}")
            return {"msg": f"Erro ao atualizar o status revisado: {e}"}

    def getStatusProjeto(self, id: str):
        try:
            doc = self.db.collection('projetos').document(id).get()
            if doc.exists:
                projeto_data = doc.to_dict()
                status = projeto_data.get("revisado", "Status não definido")
                return {"status": status}
            else:
                return {"msg": "Projeto não encontrado!"}
        except Exception as e:
            return {'msg': f'Houve um erro! {e}'}

    def curtir_projeto(self, id: str, email: str):
        try:
            doc_ref = self.db.collection('projetos').document(id)
            doc = doc_ref.get()
            msg = "Projeto não encontrado!"

            if doc.exists:
                projeto_data = doc.to_dict()
                curtidas = projeto_data.get("curtidas", 0)
                user_curtidas_email = projeto_data.get("user_curtidas_email", [])

                if email in user_curtidas_email:
                    user_curtidas_email.remove(email)
                    curtidas -= 1
                    msg = "Projeto descurtido com sucesso!"
                else:
                    user_curtidas_email.append(email)
                    curtidas += 1
                    msg = "Projeto curtido com sucesso!"

                doc_ref.update({"user_curtidas_email": user_curtidas_email})
                doc_ref.update({"curtidas": curtidas})
                return {"msg": msg, "curtidas": curtidas}
            else:
                return {"msg": msg}

        except Exception as e:
            return {'msg': f'Houve um erro! {e}'}

    def comentar_projeto(self, id: str, email: str, comentario: str):
        try:
            doc_ref = self.db.collection('projetos').document(id)
            doc = doc_ref.get()

            if doc.exists:
                projeto_data = doc.to_dict()
                comentarios = projeto_data.get("comentarios", [])
                data = datetime.datetime.now(tz=datetime.timezone.utc).strftime('%d/%m/%Y')
                comentarios.append({"username": email, "comentario": comentario, "data": data})
                doc_ref.update({"comentarios": comentarios})
                return {"msg": "Comentario adicionado com sucesso!", "comentarios": comentarios}
            else:
                return {"msg": "Projeto nao encontrado!"}

        except Exception as e:
            return {'msg': f'Houve um erro! {e}'}





