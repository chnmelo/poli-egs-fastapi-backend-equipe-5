from controllers.ConexaoFirestore import ConexaoFirestore
from models.ProdutosModel import ProdutosModel
from utils.MD5 import MD5
import os
from fastapi.responses import FileResponse
from fastapi import HTTPException


class ProdutosController(ConexaoFirestore):

    def __init__(self):
        self.db = ConexaoFirestore.conect(self)
        self.upload_directory = "uploads/produtos"
        os.makedirs(self.upload_directory, exist_ok=True)

    def setProduto(self, dados: ProdutosModel):
        try:
            key_doc = MD5(dados=dados.titulo).encrypt()  # título é chave única
            dados.id = key_doc
            dados.status = 'Pendente'
            docs = self.db.collection('produtos').document(key_doc)

            if docs.get().exists:
                raise HTTPException(status_code=400, detail="Título já cadastrado, informe outro título")
            
            write_result = docs.set(dados.toMaps())
            produto = self.db.collection('produtos').document(key_doc).get().to_dict()
            return {'msg': 'Produto criado com sucesso!', 'produto': produto}
        except Exception as e:
            raise e

    def updateProduto(self, dados: ProdutosModel):
        try:
            # Certifique-se de que há campos para atualizar
            if not dados:
                return {'msg': 'Nenhum campo para atualizar.', 'projeto': None}

            doc_ref = self.db.collection('produtos').document(dados.get("id"))
            write_result = doc_ref.set(dados, merge=True)
            produto = doc_ref.get().to_dict()
            return {
                'msg': f'Sucesso! Documento atualizado em {write_result.update_time}',
                'produto': produto
            }
        except Exception as e:
            return {'msg': f'Houve um erro! {e}'}

    def deleteProduto(self, id: str):
        try:
            produto = self.db.collection('produtos').document(id).get().to_dict()
            self.db.collection("produtos").document(id).delete()
            return {'msg': 'Sucesso ao deletar!', 'produto': produto}
        except Exception as e:
            return {'msg': f'Houve um erro! {e}'}

    def getProdutos(self):
        try:
            docs = self.db.collection('produtos').stream()
            produtos = []
            for produto in docs:
                produtos.append(produto.to_dict())
            if produtos:
                return {'msg': 'Sucesso ao listar!', 'total de produtos': len(produtos), 'produtos': produtos}
            else:
                return {"msg": "Sem produtos!"}
        except Exception as e:
            return {'msg': f'Houve um erro! {e}'}

    def getProdutoId(self, id: str):
        try:
            produto = self.db.collection('produtos').document(id).get()
            if produto.exists:
                return {'produto': produto.to_dict()}
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

    def getProdutosAprovados(self):
        try:
            query = self.db.collection('produtos').where("status", "==", "Aprovado")
            docs = query.stream()
            produtos_aprovados = [doc.to_dict() for doc in docs]
            return {"produtos_aprovados": produtos_aprovados}

        except Exception as e:
            print(f"Erro ao buscar produtos aprovados: {e}")
            return {"msg": f"Erro ao buscar produtos aprovados: {e}"}

    def getProdutosReprovados(self):
        try:
            query = self.db.collection('produtos').where("status", "==", "Reprovado")
            docs = query.stream()
            produtos_reprovados = [doc.to_dict() for doc in docs]
            return {"produtos_reprovados": produtos_reprovados}

        except Exception as e:
            print(f"Erro ao buscar produtos reprovados: {e}")
            return {"msg": f"Erro ao buscar produtos reprovados: {e}"}

    def getProdutosPendentes(self):
        try:
            query = self.db.collection('produtos').where("status", "==", "Pendente")
            docs = query.stream()
            produtos_pendentes = [doc.to_dict() for doc in docs]
            return {"produtos pendentes": produtos_pendentes}

        except Exception as e:
            print(f"Erro ao buscar produtos pendentes: {e}")
            return {"msg": f"Erro ao buscar produtos pendentes: {e}"}

    def updateStatusProduto(self, id: str, novo_status: str):
        status_validos = {"Pendente", "Aprovado", "Reprovado"}
        if novo_status not in status_validos:
            return {"msg": f"Status inválido: {novo_status}. Status permitido: {status_validos}"}
        try:
            produto_ref = self.db.collection('produtos').document(id)
            old_status = produto_ref.get().get('status')
            produto_ref.update({"status": novo_status})
            return {"msg": f"Status '{old_status}' atualizado para '{novo_status}' no produto {id}"}
        except Exception as e:
            print(f"Erro ao atualizar o status revisado: {e}")
            return {"msg": f"Erro ao atualizar o status revisado: {e}"}

    def getProdutoFiltroMultiplos(self, filtros: dict):
        try:
            query = self.db.collection('produtos')

            for campo, valor in filtros.items():
                if valor:
                    if campo == 'titulo' or campo == 'tipo':
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
            produtos_filtrados = [doc.to_dict() for doc in docs]

            print(f"Produtos encontrados: {len(produtos_filtrados)}")
            if produtos_filtrados:
                return {"produtos": produtos_filtrados}
            else:
                return {"msg": "Nenhum produto encontrado com os filtros fornecidos."}

        except Exception as e:
            print(f"Erro ao buscar produtos: {e}")
            return {"msg": f"Erro ao buscar produtos com filtros múltiplos: {e}"}