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


@router.get("/campaigns")
def fetch_campaigns(authorization: str = Header(None)):
    # Filtering by company_id extracted from the JWT means each company only
    # ever sees its own campaigns — no additional ownership check needed on
    # each row.
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = authorization.replace("Bearer ", "")
    decoded_access_token = decode_access_token(token)

    if decoded_access_token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    company_id = decoded_access_token["company_id"]

    response = (
        supabase.table("campaigns")
        .select("*")
        .eq("company_id", company_id)
        .execute()
    )

    return {"message": "Campaigns retrieved", "campaigns": response.data}
  