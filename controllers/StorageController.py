import firebase_admin
from firebase_admin import credentials, storage,datetime
from controllers.keyAdmin import initialize_firebase  # Import initialization function
import tempfile, shutil, os
from fastapi import UploadFile, HTTPException


class StorageController:

    """ def __init__(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate("controllers/keyAdmin.py")
            firebase_admin.initialize_app(cred,{
                'storageBucket': 'ecomp-observatorio.appspot.com'
            }) """
    def __init__(self):
        # Ensure Firebase is initialized using environment variables
        initialize_firebase()

        # Set up the Firebase Storage bucket
        self.bucket = storage.bucket("ecomp-observatorio.appspot.com")

    
    #PARTE ARMAZENAR AS IMAGENS OU LOGO DO SPROJETOS
    def upload_logo_projeto(self, id, file):
        bucket = storage.bucket()
        nome_imagem = id+".png"
        blob = bucket.blob("logo_projetos/"+nome_imagem)

        if blob.exists():
            blob.delete()

        blob.upload_from_filename(file)
        #caso precisamos de uma url temporária
        #url = blob.generate_signed_url(expiration=datetime.timedelta(minutes=500),method='GET')
        blob.make_public()
        # Obtenha a URL pública do arquivo
        url = blob.public_url
        return {"url": url}
    
    def view_logo_projeto(self, id):
        bucket = storage.bucket()
        nome_imagem = id+".png"
        blob = bucket.blob("logo_projetos/"+nome_imagem)
        #blob.download_to_filename(id)
        if not blob.exists():
            raise HTTPException(status_code=404, detail="Logo não encontrada no Firebase.")
        #Url temporária
        #url = blob.generate_signed_url(expiration=datetime.timedelta(minutes=500),method='GET')
        url = blob.public_url
        return {'url':url}
    
    def upload_fotos_integrantes(self,file,file_id):
        bucket = storage.bucket()
        nome_imagem = f"{file_id}.png"
        blob = bucket.blob("fotos_integrantes/"+nome_imagem)

        if blob.exists():
            blob.delete()

        blob.upload_from_filename(file)
        blob.make_public()
        url = blob.public_url
        return {"url": url}
    
    def view_fotos_integrantes(self, id):
        bucket = storage.bucket()
        blob = bucket.blob("fotos_integrantes/"+id+".png")
        url = blob.public_url
        return {'url':url}
    
    #PARTE ARMAZENAR OS PDF OU ARTIGOS DO PROJETO
    def upload_pdf_artigo(self, id: str, file: UploadFile):
        try:
            #cria um nome para o arquivo pdf e cria um diretorio no Firebase
            nome_pdf = f"{id}.pdf"
            blob = self.bucket.blob(f"pdf_artigos/{nome_pdf}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao subir pdf para o firebase: {str(e)}")
        
        # Salvar o arquivo temporariamente
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
        
        # Fazer o upload pro Firebase
        blob.upload_from_filename(tmp_path)
        blob.make_public()
        os.remove(tmp_path)
        
        # Obtenha a URL pública do arquivo
        return {"url": blob.public_url}
    
    def view_pdf_artigo(self, id):
        try:
            bucket = storage.bucket()
            nome_pdf = id + ".pdf"
            blob = bucket.blob("pdf_artigos/" + nome_pdf)

            if not blob.exists():
                raise HTTPException(status_code=404, detail="PDF não encontrado no Firebase.")

            blob.make_public()
            return {'url':blob.public_url}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao recuperar PDF: {str(e)}")
