from firebase_admin import auth as admin_auth
from fastapi import HTTPException

def check_if_admin(id_token: str):
    try:
        # Tenta verificar e decodificar o token
        decoded_token = admin_auth.verify_id_token(id_token)
        
        # Verifica se o usuário tem a permissão de admin
        if not decoded_token.get('admin', False):
            raise HTTPException(status_code=403, detail="Access forbidden: Admins only.")
        
        return decoded_token
    
    except Exception:
        # Qualquer erro relacionado ao token é tratado aqui
        raise HTTPException(status_code=403, detail="token error")


def check_if_login(id_token: str):
    try:
        decoded_token = admin_auth.verify_id_token(id_token)
        if not decoded_token:
            raise HTTPException(status_code=403, detail="Access forbidden: User not logged in.")
        return decoded_token
    except Exception:
        # Qualquer erro relacionado ao token é tratado aqui
        raise HTTPException(status_code=403, detail="token error")