from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.database import supabase 

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