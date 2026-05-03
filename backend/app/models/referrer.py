from pydantic import BaseModel, EmailStr
from typing import Optional 


class Referrer(BaseModel):
    name : Optional[str] = None
    email : EmailStr 
   