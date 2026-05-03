from fastapi import APIRouter 
from app.models.campaign import CreateCampaign 
from app.services.database import supabase 

router = APIRouter()


@router.post("/campaigns")
def create_campaign(data: CreateCampaign, company_id: str):
    response = (supabase.table("campaigns")
                .insert({
                    "company_id": company_id,
                    "campaign_name" : data.campaign_name,
                    "campaign_description" : data.campaign_description,
                    "website_url" : str(data.website_url),
                    "vibe" : data.vibe, 
                    "reward_description" : data.reward_description,
                    "is_demo" : data.is_demo,
                    "expires_at" : data.expires_at.isoformat() if data.expires_at else None,
                    "send_welcome_email" : data.send_welcome_email
                })
                .execute()
                )
    return {"message": "Campaign created", "campaign": response.data[0]}
    
