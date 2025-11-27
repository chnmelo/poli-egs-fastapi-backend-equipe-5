from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from controllers.UserController import UserController

router = APIRouter()
user_controller = UserController()

class AdminClaimPayload(BaseModel):
    email: EmailStr

@router.post("/set-admin/", summary="Conceder permissão de administrador a um usuário")
def set_admin_claim(payload: AdminClaimPayload):
    """
    Endpoint para atribuir permissões de administrador a um usuário existente.
    **Atenção:** Este é um endpoint sensível e deve ser protegido em produção.
    """
    try:
        result = user_controller.set_admin_claim(payload.email)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor: {e}")
