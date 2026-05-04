from fastapi import APIRouter, HTTPException, Header 
from app.models.campaign import CreateCampaign
from app.services.database import supabase 
from app.services.auth import decode_access_token

router = APIRouter()


@router.post("/campaigns")
def create_campaign(data: CreateCampaign, authorization: str= Header(None)):
    # Reject request immediately if no Authorization header was sent
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Strip "Bearer " prefix to get the raw JWT token
    token = authorization.replace("Bearer ", "")

    # Decode and validate the token — returns None if invalid or expired
    decoded_access_token = decode_access_token(token)

    # If token is invalid or expired, reject the request
    if decoded_access_token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Extract company_id from the decoded token payload
    company_id = decoded_access_token["company_id"]

    # Insert the new campaign into the database
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
    
