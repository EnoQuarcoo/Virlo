from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class CreateCampaign(BaseModel):
    campaign_name : str
    campaign_description : Optional[str] = None
    website_url : HttpUrl
    vibe : Optional[str] = None
    reward_description : str 
    is_demo : bool = False 
    expires_at : Optional[datetime] = None 
    send_welcome_email : bool = True 


     