from fastapi import APIRouter 
from app.services.database import supabase

router = APIRouter()


@router.get("/campaigns/{campaign_id}/leaderboard")
def get_leaderboard(campaign_id):
    response = (
        supabase.table("referrers")
        .select("*")
        .eq("campaign_id", campaign_id)
        .order("referral_count", desc=True)
        .execute()
    )
    return {"leaderboard": response.data}

