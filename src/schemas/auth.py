from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
import re

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: UUID | None = None
    role: str | None = None

class UserRegister(BaseModel):
    full_name: str = Field(..., example="Nguyen Van A", min_length=2)
    email: EmailStr = Field(..., example="nguyenvana@gmail.com")
    password: str = Field(..., example="matkhau123", min_length=6)
    phone: str = Field(..., example="0912345678", pattern=r'^\+?[0-9]{8,15}$')

class UserResponse(BaseModel):
    id: UUID
    full_name: str
    email: str
    phone: str
    role: str
