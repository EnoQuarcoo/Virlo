from pydantic import BaseModel, EmailStr, HttpUrl

class CompanySignup(BaseModel):
    name : str
    email : EmailStr 
    password: str
    website_url : HttpUrl
    company_information: str 
    company_vibe :  str


class CompanyLogin(BaseModel):
    email : EmailStr 
    password: str
