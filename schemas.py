from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserSchema(BaseModel):
    username: str = Field(..., min_length=8)
    password: str = Field(..., min_length=8)
    status: Optional[str]


class UpdateUserSchema(BaseModel):
    username: Optional[str]
    password: Optional[str]
    status: Optional[str]


class LoginLogSchema(BaseModel):
    user_id: str
    login_time: str
    action: str