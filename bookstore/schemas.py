from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    """Schema for user registration"""
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """Schema for user response (without password)"""
    id: int
    email: EmailStr

    class Config:
        orm_mode = True  # Enables compatibility with SQLAlchemy ORM objects
