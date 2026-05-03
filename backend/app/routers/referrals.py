from fastapi import APIRouter
from app.models.referral import referral
from app.services.database import supabase

router = APIRouter()

@router.post("/referrals/track")
def track_referral(data: referral):
    # Find the referrer by their referral code
    referrer = (
        supabase.table("referrers")
        .select("*")
        .eq("referral_code", data.referral_code)
        .execute()
    )
    
    if not referrer.data:
        return {"message": "Invalid referral code"}
    
    referrer_id = referrer.data[0]["id"]
    current_count = referrer.data[0]["referral_count"]
    
    # Increment the referral count by 1
    supabase.table("referrers").update(
        {"referral_count": current_count + 1}
    ).eq("id", referrer_id).execute()
    
    # Log the referral
    supabase.table("referrals").insert({
        "referrer_id": referrer_id,
        "referred_email": str(data.referred_email)
    }).execute()
    
    return {"message": "Referral tracked successfully"}