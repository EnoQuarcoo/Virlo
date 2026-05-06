# Supabase client is created once at module import time and shared across all
# routers. Creating a new client per request would be wasteful — the client
# manages connection pooling internally, so a single instance is the right model.
from supabase import create_client, Client
from app.config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
