from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional


class CompanySignup(BaseModel):
    name: Optional[str] = None 
    email: EmailStr
    password: str
    website_url: Optional[str] = None 
    company_information: Optional[str] = None
    company_vibe:  Optional[str] = None


class CompanyLogin(BaseModel):
    email: EmailStr
    password: str
