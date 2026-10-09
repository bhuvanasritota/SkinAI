from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ProfileCreate(BaseModel):
    skin_type: str
    concerns: list[str]

    age_range: Optional[str] = None

    product_preferences: Optional[str] = None

    budget: Optional[int] = None

    ingredients_to_avoid: Optional[str] = None


class ProfileResponse(BaseModel):
    skin_type: str
    concerns: list[str]

    age_range: Optional[str] = None

    product_preferences: Optional[str] = None

    budget: Optional[int] = None

    ingredients_to_avoid: Optional[str] = None