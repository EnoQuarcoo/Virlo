from fastapi import APIRouter
from app.models.referrer import Referrer
import secrets
import string 
from app.services.database import supabase

def generate_referral(length=6):
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return ''.join(secrets.choice(alphabet) for _ in range(length))





router = APIRouter()

@router.post("/campaigns/{campaign_id}/signup")
def create_referrer(campaign_id: str, data: Referrer):
    #Retrive the company's website link 
    response = (
        supabase.table("campaigns")
        .select("website_url")
        .eq("id",campaign_id)
        .execute()
    )
    referral_code = generate_referral()
    website_link = response.data[0]["website_url"]
    referral_link = website_link +"?ref=" + referral_code 
    response = (
        supabase.table("referrers")
        .insert({
            "name" : data.name,
            "email" : data.email,
            "campaign_id" : campaign_id,
            "referral_code" : referral_code,
            "referral_link" : referral_link,
            "referral_count" : 0 
        })
        .execute()
    )
    return {"message":"Referrer created", "referral_link" : referral_link} 
    ...