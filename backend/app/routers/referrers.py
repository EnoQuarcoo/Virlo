from fastapi import APIRouter, Header, HTTPException
from app.models.referrer import Referrer
import secrets
import string
from app.services.database import supabase
from app.services.auth import get_company_id_from_api_key

def generate_referral(length=6):
    # This alphabet deliberately omits visually ambiguous characters:
    # 0/O look alike, 1/I/l look alike. Referral codes may be typed manually
    # by end users, so ambiguity causes failed lookups and support tickets.
    # secrets.choice provides cryptographically secure randomness so codes
    # can't be predicted or brute-forced.
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return ''.join(secrets.choice(alphabet) for _ in range(length))



router = APIRouter()

@router.post("/campaigns/{campaign_id}/signup")
def create_referrer(campaign_id: str, data: Referrer, x_api_key:str=Header(None)):
    company_id = get_company_id_from_api_key(x_api_key)
    # Fetch the campaign's website_url to build the referral link server-side.
    # The client doesn't know the base URL, and building it server-side ensures
    # the link always points to the canonical URL stored at campaign creation.
    campaign_response = (
        supabase.table("campaigns")
        .select("website_url, company_id")
        .eq("id", campaign_id)
        .execute()
    )
    if not campaign_response.data:
        raise HTTPException(status_code=404, detail="Campaign not found")

    campaign = campaign_response.data[0]

    if campaign["company_id"] != company_id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    

    #Check if referrer already exists for this campaign
    existing_referrer_response = (
        supabase.table("referrers")
        .select("*")
        .eq("email", data.email)
        .eq("campaign_id", campaign_id)
        .execute()
    )

    if existing_referrer_response.data:
        return {"message": "Referrer already exists", "referral_link": existing_referrer_response.data[0]["referral_link"]}

    referral_code = generate_referral()
    website_link = campaign["website_url"]
    # Append the referral code as a query parameter so the campaign page can
    # detect it and trigger tracking via the /referrals/track endpoint.
    referral_link = website_link + "?ref=" + referral_code
    add_referrer_response = (
        supabase.table("referrers")
        .insert({
            "name": data.name,
            "email": data.email,
            "campaign_id": campaign_id,
            "referral_code": referral_code,
            "referral_link": referral_link,
            # Initialize count explicitly to 0 so the leaderboard query can
            # order by this column without needing NULL handling.
            "referral_count": 0
        })
        .execute()
    )
    return {"message": "Referrer created", "referral_link": referral_link}



