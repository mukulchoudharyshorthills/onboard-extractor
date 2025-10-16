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

class DocumentSchema(BaseModel):
    user_id: str
    path: str
    title: str
    tag: str
    data: dict
    edited_data: dict
    status: Optional[str]

class UpdateDocumentSchema(BaseModel):
    user_id: str
    path: Optional[str]
    title: Optional[str]
    tag: Optional[str]
    data: Optional[dict]
    edited_data: Optional[dict]
    status: Optional[str]