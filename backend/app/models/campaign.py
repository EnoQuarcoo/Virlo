from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class CreateCampaign(BaseModel):
    campaign_name: str
    campaign_description: Optional[str] = None
    # HttpUrl validates that website_url is a properly formed URL with a scheme
    # (https://...). This matters because we append referral codes to this URL
    # when generating referral links — a malformed base URL would produce
    # broken links that silently fail to track referrals.
    website_url: HttpUrl
    vibe: Optional[str] = None
    reward_description: str
    is_demo: bool = False
    expires_at: Optional[datetime] = None
    send_welcome_email: bool = True


     