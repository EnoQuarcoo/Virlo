from pydantic import BaseModel, EmailStr

class referral(BaseModel):
    referral_code : str 
    referred_email : EmailStr  
    