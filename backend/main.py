from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.services.database import supabase
from app.routers.companies import router as companies_router
from app.routers.campaigns import router as campaigns_router
from app.routers.referrers import router as referrer_router
from app.routers.referrals import router as referral_router
from app.routers.leaderboards import router as leaderboard_router
from app.services.scheduler import scheduler
from contextlib import asynccontextmanager

def get_allowed_origins():
    response = ( supabase.table("companies")
                .select("website_url")
                .execute()
                )
    allowed_origins = []
    for company in response.data:
        #filter out null values
        url = company["website_url"]
        if url and url != "None":
            allowed_origins.append(company["website_url"])
    # Vite's dev server may bind to different ports on each start, so we allow
    # the common range (5173–5175) to avoid broken requests during local dev.
    allowed_origins += [
        "http://localhost:5173",
        "http://localhost:5174", 
        "http://localhost:5175",
        "https://virlo-eta.vercel.app"
    ]
    return allowed_origins 

    



@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)
# get_allowed_origins() is called once at startup. New company domains
# won't be allowed until the server restarts. A production fix would be
# middleware that queries allowed origins dynamically on each request.
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Virlo API is running"}


app.include_router(companies_router)
app.include_router(campaigns_router)
app.include_router(referrer_router)
app.include_router(referral_router)
app.include_router(leaderboard_router)
