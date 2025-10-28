from fastapi import APIRouter, Depends
from controllers.UserController import UserController
from models.UserModel import UserModel
from models.ForgotPasswordModel import ForgotPasswordModel
from utils.checkAdminUser import check_if_admin
router = APIRouter()
user_controller = UserController()


@router.post("/register")
def register(user: UserModel):
    return user_controller.register(user.username, user.email, user.password, user.is_admin)

@router.post("/login")
def login(email: str, password: str):
    return user_controller.login(email, password)

@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordModel):
    return user_controller.forgot_password(request.email)

@router.get("/user-info/{user_id}", dependencies=[Depends(check_if_admin)])
def get_user_info(user_id: str):
    return user_controller.get_user_info(user_id)

@router.get("/users", dependencies=[Depends(check_if_admin)])
def list_users():
    return user_controller.list_users()

@router.put("/users/{user_id}", dependencies=[Depends(check_if_admin)])
def update_user(user_id: str, username: str, is_admin: bool):
    return user_controller.update_user(
        user_id=user_id,
        username=username,
        is_admin=is_admin
    )

@router.delete("/users/{user_id}", dependencies=[Depends(check_if_admin)])
def delete_user(user_id: str):
    return user_controller.delete_user(user_id)