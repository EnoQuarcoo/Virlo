#Supabase connection lives here
from supabase import create_client, Client 
from app.config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
