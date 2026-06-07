import os
import resend
import anthropic
from app.services.database import supabase
from app.config import CLAUDE_API_KEY, RESEND_API_KEY
import json


# Set up Claude Client
client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

# Set up Resend
resend.api_key = RESEND_API_KEY


# Query supabase and return all campaigns with their referrer counts
def fetch_campaign_data():
    
    """
    Fetches all campaigns from Supabase with referrer counts and company emails.
    Strips emails from campaign data before returning to protect privacy.
    Returns campaign data (list) and email_dict (dict mapping campaign_id to email).
    """
    email_dict = {}
    response = (supabase.table("campaigns")
                .select("id,campaign_name, reward_description, campaign_description, referrers(id), companies(email)")
                .execute()
                )

    for campaign in response.data:
        # replace individual referral ids with a referral count
        referrer_count = len(campaign["referrers"])
        campaign["referrer_count"] = referrer_count
        del campaign["referrers"]

        # Store emails in the dict and del it from the data
        campaign_id = campaign["id"]
        campaign_email = campaign["companies"]["email"]
        del campaign["companies"]
        email_dict[campaign_id] = campaign_email

    return response.data, email_dict

# Call claude to analyze the campagins and return emails for the companies. 
def analyze_campaigns(campaign_data):
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=6000,
        messages=[{"role": "user", "content": json.dumps(campaign_data)}],
        system="""These are campaigns created using an app called Virlo. 
        Virlo is a B2B2C marketing platform that allows companies to increase customer engagement through a referral system. 
        Companies create campaigns through Virlo's dashboard, set a reward, and embed the campaign into their website.
        For example, a prelaunch company might give early access to users who refer 3 or more people. 
        A retail company might offer discount tiers based on referral count. You will receive a list of campaigns with their details.
        For each campaign, analyze the data available and assess its health — is it thriving or stalling? Make specific recommendations to improve performance. 
        Pay close attention to referrer count as a key health signal. For each campaign, your analysis and suggestions should come in the form of a professional, advisory email
        Respond only with a JSON array. Each object in the array should have these four fields: campaign_id, campaign_name, email_subject, email_body. 
        No extra text. Do not wrap the response in markdown code blocks or backticks. 
        The email body should be formatted in HTML. The email you generate will be sent as is, obeying the html,  to the customer. 
        Ensure that it is written to traditional email standards. 
        """

    )
    text = message.content[0].text
    clean = text.strip().removeprefix("```json").removeprefix(
        "```").removesuffix("```").strip()
    return json.loads(clean)


def send_email(claude_analysis, email_dict):
    for assessment in claude_analysis: 
        campaign_id = assessment["campaign_id"]
        campaign_email = email_dict[campaign_id]
        try:
            result = resend.Emails.send({
                "from": os.environ.get("EMAIL_FROM", "Virlo <onboarding@resend.dev>"),
                "to": ["delivered@resend.dev"],  # TODO: replace with campaign_email when domain is verified
                "subject": assessment["email_subject"],
                "html": assessment["email_body"],
            })
            print({"message":"Email sent successfully!", "result":result }) 
        except Exception as e:
            print(f"Error sending email: {e}")
            continue 

def run_agent():
    campaigns_data, email_dict = fetch_campaign_data()
    claude_analysis = analyze_campaigns(campaigns_data)
    send_email(claude_analysis, email_dict)

