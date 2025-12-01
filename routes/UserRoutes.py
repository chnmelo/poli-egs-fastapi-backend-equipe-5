from fastapi import APIRouter, Depends
from controllers.UserController import UserController
from pydantic import BaseModel 
from typing import Optional
from models.UserModel import UserModel
from models.UserLoginModel import UserLoginModel
from models.ForgotPasswordModel import ForgotPasswordModel
from utils.checkAdminUser import check_if_admin, check_if_login

router = APIRouter()
user_controller = UserController()

class UserProfileUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None


@router.post("/register/")
def register(user: UserModel):
    return user_controller.register(user.username, user.email, user.password, user.is_admin)

@router.post("/login/")
def login(dados: UserLoginModel):
    return user_controller.login(dados.email, dados.password)

@router.post("/forgot-password/")
def forgot_password(request: ForgotPasswordModel):
    return user_controller.forgot_password(request.email)

@router.get("/user-info/{user_id}/", dependencies=[Depends(check_if_admin)])
def get_user_info(user_id: str):
    return user_controller.get_user_info(user_id)

@router.get("/users/", dependencies=[Depends(check_if_admin)])
def list_users():
    return user_controller.list_users()

@router.put("/users/{user_id}/", dependencies=[Depends(check_if_admin)])
def update_user(user_id: str, username: str, is_admin: bool):
    return user_controller.update_user(
        user_id=user_id,
        username=username,
        is_admin=is_admin
    )

@router.delete("/users/{user_id}/", dependencies=[Depends(check_if_admin)])
def delete_user(user_id: str):
    return user_controller.delete_user(user_id)

@router.get("/users/me/", dependencies=[Depends(check_if_login)])
def get_my_profile(decoded_token=Depends(check_if_login)):
    user_id = decoded_token['uid']
    return user_controller.get_my_profile(user_id)

@router.put("/users/me/", dependencies=[Depends(check_if_login)])
def update_my_profile(dados: UserProfileUpdate, decoded_token=Depends(check_if_login)):
    user_id = decoded_token['uid']
    return user_controller.update_profile(user_id, dados.username, dados.password)