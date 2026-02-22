from pydantic import BaseModel, EmailStr
from typing import Optional

class StandardResponse(BaseModel):
    status: bool
    message: str
    data: Optional[dict | list] = None


class UserSignup(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TodoCreate(BaseModel):
    title: str
    description: str


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None