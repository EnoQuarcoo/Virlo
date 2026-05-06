from fastapi import APIRouter
from app.models.referral import referral
from app.services.database import supabase

router = APIRouter()

@router.post("/referrals/track")
def track_referral(data: referral):
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

    # We read the count and write count+1 in two separate calls because the
    # Supabase Python client doesn't expose atomic increment operations without
    # using a raw RPC call. This means there's a small race condition window
    # under very high concurrency, but it's acceptable for typical campaign volumes.
    supabase.table("referrers").update(
        {"referral_count": current_count + 1}
    ).eq("id", referrer_id).execute()

    # Write a referral log row separately from updating the count. The log
    # serves as an audit trail — if counts ever drift, the log can be replayed
    # to reconstruct accurate totals. It also lets us detect duplicate referrals
    # (same email referred more than once) in the future.
    supabase.table("referrals").insert({
        "referrer_id": referrer_id,
        "referred_email": str(data.referred_email)
    }).execute()

    return {"message": "Referral tracked successfully"}