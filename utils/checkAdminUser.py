from firebase_admin import auth as admin_auth
from fastapi import HTTPException
import time

def check_if_admin(id_token: str):
    try:
        # Tenta verificar e decodificar o token
        decoded_token = admin_auth.verify_id_token(id_token)
        
        # Verifica se o usuário tem a permissão de admin
        if not decoded_token.get('admin', False):
            raise HTTPException(status_code=403, detail="Access forbidden: Admins only.")
        
        return decoded_token
    
    except admin_auth.InvalidIdTokenError as e:
        error_message = str(e)
        
        # Se o erro for "Token used too early"
        if "Token used too early" in error_message:
            print("Relógio dessincronizado (atrasado). Aguardando 10s para tentar de novo...")
            
            # ESPERA 10 SEGUNDOS (A "GAMBIARRA")
            time.sleep(10) 
            
            try:
                # Tenta de novo
                decoded_token = admin_auth.verify_id_token(id_token)
                return decoded_token
            except Exception as retry_e:
                # Se falhar de novo, desiste
                raise HTTPException(status_code=401, detail=f"token error after retry: {retry_e}")

        # Se for outro erro de token (expirado, assinatura, etc.)
        raise HTTPException(status_code=401, detail=f"token error: {e}")
    
    except Exception as e:
        # Qualquer erro relacionado ao token é tratado aqui
        raise HTTPException(status_code=403, detail=f"token error: {e}")


def check_if_login(id_token: str):
    try:
        decoded_token = admin_auth.verify_id_token(id_token)
        if not decoded_token:
            raise HTTPException(status_code=403, detail="Access forbidden: User not logged in.")
        return decoded_token
    except admin_auth.InvalidIdTokenError as e:
        error_message = str(e)
        
        # Se o erro for "Token used too early"
        if "Token used too early" in error_message:
            print("Relógio dessincronizado (atrasado). Aguardando 10s para tentar de novo...")
            
            # ESPERA 10 SEGUNDOS (A "GAMBIARRA")
            time.sleep(10) 
            
            try:
                # Tenta de novo
                decoded_token = admin_auth.verify_id_token(id_token)
                return decoded_token
            except Exception as retry_e:
                # Se falhar de novo, desiste
                raise HTTPException(status_code=401, detail=f"token error after retry: {retry_e}")

        # Se for outro erro de token (expirado, assinatura, etc.)
        raise HTTPException(status_code=401, detail=f"token error: {e}")
    
    except Exception as e:
        # Qualquer erro relacionado ao token é tratado aqui
        raise HTTPException(status_code=403, detail=f"token error: {e}")