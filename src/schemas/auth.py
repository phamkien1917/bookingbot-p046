from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class TokenData(BaseModel):
    user_id: UUID | None = None
    role: str | None = None

class UserRegister(BaseModel):
    full_name: str = Field(..., json_schema_extra={"example": "Nguyen Van A"}, min_length=2)
    email: EmailStr = Field(..., json_schema_extra={"example": "nguyenvana@gmail.com"})
    password: str = Field(..., json_schema_extra={"example": "matkhau123"}, min_length=6)
    phone: str = Field(..., json_schema_extra={"example": "0912345678"}, pattern=r'^\+?[0-9]{8,15}$')

class UserResponse(BaseModel):
    id: UUID
    full_name: str
    email: str
    phone: str | None
    role: str
    status: str

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2)
    phone: str | None = Field(default=None, pattern=r'^\+?[0-9]{8,15}$')

class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=6)
