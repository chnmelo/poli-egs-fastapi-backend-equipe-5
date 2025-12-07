from firebase_admin import auth as admin_auth
from fastapi import HTTPException, Request
import time
# Importar a inicialização para garantir conexão
from controllers.keyAdmin import initialize_firebase 
import logging

logger = logging.getLogger(__name__)

# Garante a inicialização
try:
    initialize_firebase()
except Exception:
    pass

def get_token_from_request(request: Request):
    # 1. Tenta pegar do Header
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        return auth_header.split(' ')[1]
    
    # 2. Fallback para URL
    return request.query_params.get('id_token')

def check_if_admin(request: Request):
    id_token = get_token_from_request(request)
    
    if not id_token:
        raise HTTPException(status_code=401, detail="Token não fornecido.")

    try:
        # Adiciona 5 segundos de tolerância de relógio (clock skew)
        decoded_token = admin_auth.verify_id_token(id_token, clock_skew_seconds=60)
        
        if not decoded_token.get('admin', False):
            raise HTTPException(status_code=403, detail="Acesso proibido: Apenas administradores.")
        
        return decoded_token
    
    except Exception as e:
        logger.info(f"!!! ERRO ADMIN VERIFY: {e}") # OLHE NO TERMINAL
        raise HTTPException(status_code=401, detail=f"Sessão inválida: {str(e)}")


def check_if_login(request: Request):
    id_token = get_token_from_request(request)

    if not id_token:
        logger.info("!!! ERRO: Token não encontrado no request.")
        raise HTTPException(status_code=401, detail="Token não fornecido.")

    try:
        # Adiciona 5 segundos de tolerância de relógio
        decoded_token = admin_auth.verify_id_token(id_token, clock_skew_seconds=60)
        return decoded_token
        
    except ValueError as e:
        logger.info(f"!!! ERRO CONFIG FIREBASE: {e}")
        try:
            initialize_firebase()
            return admin_auth.verify_id_token(id_token, clock_skew_seconds=60)
        except Exception as e2:
             logger.info(f"!!! ERRO RE-INIT: {e2}")
             raise HTTPException(status_code=500, detail=f"Erro interno de autenticação: {str(e2)}")

    except Exception as e:
        logger.info(f"!!! ERRO LOGIN VERIFY: {e}") # OLHE NO TERMINAL, O ERRO ESTARÁ AQUI
        raise HTTPException(status_code=401, detail=f"Token inválido: {str(e)}")