from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional


class CompanySignup(BaseModel):
    name: str
    email: EmailStr
    password: str
    website_url: HttpUrl
    company_information: Optional[str] = None
    company_vibe:  Optional[str] = None


class CompanyLogin(BaseModel):
    email: EmailStr
    password: str
