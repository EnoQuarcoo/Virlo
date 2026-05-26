from fastapi import APIRouter
from app.services.database import supabase

router = APIRouter()


@router.get("/campaigns/{campaign_id}/leaderboard")
def get_leaderboard(campaign_id):
    # This endpoint is intentionally unauthenticated. The leaderboard is part
    # of the public campaign experience — referrers share their link and can
    # see where they rank without needing a company account.
    # Sorting is done in the database query rather than in Python so Supabase
    # only returns already-ranked data; sorting in Python would require loading
    # all referrers into memory first.
    response = (
        supabase.table("referrers")
        .select("*")
        .eq("campaign_id", campaign_id)
        .order("referral_count", desc=True)
        .execute()
    )
    return {
        "leaderboard": response.data
        }

