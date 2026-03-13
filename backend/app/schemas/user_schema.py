from pydantic import BaseModel, EmailStr, Field
from uuid import UUID #It is a unique ID used to identify records like users, vehicles, bookings, etc.
from enum import Enum
from typing import Optional
from datetime import datetime


class UserRole(str, Enum):
    USER = "user"
    PROVIDER = "provider"
    ADMIN = "admin"


class Msg(BaseModel):
    message: str


class UserBase(BaseModel):

    name: str
    email: EmailStr
    contact: str
    profile_pic: str
    address: str
    role: UserRole = UserRole.USER


class UserCreate(UserBase):

    password: str = Field(..., min_length=8, max_length=72)


class UserUpdate(BaseModel):

    name: Optional[str] = None
    contact: Optional[str] = None
    profile_pic: Optional[str] = None
    address: Optional[str] = None


class UserResponse(UserBase):

    id: int
    uuid: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True