from fastapi import APIRouter, HTTPException, Header
from app.models.campaign import CreateCampaign
from app.services.database import supabase
from app.services.auth import decode_access_token, get_company_id_from_token

router = APIRouter()


@router.post("/campaigns")
def create_campaign(data: CreateCampaign, authorization: str = Header(None)):
    # company_id comes from the verified JWT, not from the request body.
    # Accepting it as a body parameter would let any authenticated company
    # create campaigns under a different company's account.
    company_id = get_company_id_from_token(authorization)

    # expires_at must be serialized to ISO 8601 string because Supabase's
    # Python client doesn't accept Python datetime objects directly.
    response = (supabase.table("campaigns")
                .insert({
                    "company_id": company_id,
                    "campaign_name": data.campaign_name,
                    "campaign_description": data.campaign_description,
                    "website_url": str(data.website_url),
                    "vibe": data.vibe,
                    "reward_description": data.reward_description,
                    "is_demo": data.is_demo,
                    "expires_at": data.expires_at.isoformat() if data.expires_at else None,
                    "send_welcome_email": data.send_welcome_email
                })
                .execute()
                )
    return {"message": "Campaign created", "campaign": response.data[0]}



@router.get("/campaigns/{campaign_id}")
def campaign_details(campaign_id: str, authorization: str = Header(None)):
    company_id = get_company_id_from_token(authorization)
    response = (
        supabase.table("campaigns")
        .select("*")
        .eq("id", campaign_id)
        .execute()
    )
    if not response.data:
        raise HTTPException(status_code=404, detail="Campaign not found")
    campaign = response.data[0]
    # Ownership check: any authenticated company can hit this endpoint with an
    # arbitrary campaign_id, so we verify the campaign belongs to the requester.
    if campaign["company_id"] != company_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return {"message": "Campaign data retrieved", "campaign": campaign}



# Returns all campaigns owned by the authenticated company.
@router.get("/campaigns")
def fetch_campaigns(authorization: str = Header(None)):
    company_id = get_company_id_from_token(authorization)
    response = (
        supabase.table("campaigns")
        .select("*")
        .eq("company_id", company_id)
        .execute()
    )
    return {"message": "Campaigns retrieved", "campaigns": response.data}

