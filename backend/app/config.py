import os 
from dotenv import load_dotenv 

load_dotenv() #loads veraibles from .env 

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
JWT_SECRET = os.getenv("JWT_SECRET")
