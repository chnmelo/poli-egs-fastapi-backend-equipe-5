from pydantic import BaseModel, EmailStr
from typing import Optional

class UserModel(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None
