from pydantic import BaseModel, EmailStr;
from typing import Optional;

class SignupSchema(BaseModel):
    email: EmailStr;
    password: str;
    fullname: str;

class SigninSchema(BaseModel):
    email: EmailStr;
    password: str;

class UpdateUserSchema(BaseModel):
    email: Optional[EmailStr] = None;
    password: Optional[str] = None;
    fullname: Optional[str] = None;