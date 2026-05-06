from fastapi import APIRouter
from app.models.referrer import Referrer
import secrets
import string
from app.services.database import supabase

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
def create_referrer(campaign_id: str, data: Referrer):
    # Fetch the campaign's website_url to build the referral link server-side.
    # The client doesn't know the base URL, and building it server-side ensures
    # the link always points to the canonical URL stored at campaign creation.
    response = (
        supabase.table("campaigns")
        .select("website_url")
        .eq("id", campaign_id)
        .execute()
    )
    referral_code = generate_referral()
    website_link = response.data[0]["website_url"]
    # Append the referral code as a query parameter so the campaign page can
    # detect it and trigger tracking via the /referrals/track endpoint.
    referral_link = website_link + "?ref=" + referral_code
    response = (
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