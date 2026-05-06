from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional


class CompanySignup(BaseModel):
    # EmailStr triggers Pydantic's email format validation before the handler
    # runs, so we never receive a malformed email address in the database.
    # Most signup fields are Optional because the onboarding flow can be
    # completed in stages — only email and password are required to create an account.
    name: Optional[str] = None
    email: EmailStr
    password: str
    website_url: Optional[str] = None
    company_information: Optional[str] = None
    company_vibe: Optional[str] = None


class CompanyLogin(BaseModel):
    email: EmailStr
    password: str
