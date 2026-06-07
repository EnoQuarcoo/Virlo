import os 
import resend 
import anthropic 
from app.services.database import supabase
from app.config import CLAUDE_API_KEY, RESEND_API_KEY


#Set up Claude Client 
client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

#Set up Resend 
resend.api_key = RESEND_API_KEY


#Querry supabse and return all campaigns with their referrer counts
def fetch_campaign_data():
    response= (supabase.table("campaigns")
    .select("id,campaign_name, referrers(id)")
    .execute()
    )

    for campaign in response.data:
        referrer_count = len(campaign["referrers"])
        campaign["referrer_count"] = referrer_count 
        del campaign["referrers"]

    return  response.data

#Claude API call, prompt engineering
def analyze_campaigns(campaign_data):
    ... 