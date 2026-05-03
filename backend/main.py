from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.services.database import supabase 
from app.routers.companies import router as companies_router
from app.routers.campaigns import router as campaigns_router
from app.routers.referrers import router as referrer_router
from app.routers.referrals import router as referral_router
from app.routers.leaderboards import router as leaderboard_router 


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Virlo API is running"}

@app.get("/testsupabase")
def get_company_name():
    response = (
        supabase.table("companies")
        .select("*")
        .execute()
    )
    return response.data

app.include_router(companies_router)
app.include_router(campaigns_router)
app.include_router(referrer_router)
app.include_router(referral_router)
app.include_router(leaderboard_router)
