from fastapi import APIRouter, HTTPException 
from app.models.company import CompanySignup, CompanyLogin
from app.services.auth import hash_password, verify_password, create_access_token
from app.services.database import supabase


router = APIRouter()


@router.post("/auth/register")
def signup_company(data: CompanySignup):
    hashed = hash_password(data.password)
    response = (supabase.table("companies")
                .insert({
                    "name": data.name,
                    "email": data.email,
                    "password": hashed,
                    "website_url": str(data.website_url),
                    "company_information": data.company_information,
                    "company_vibe": data.company_vibe
                })
                .execute()
                )
    company = response.data[0]
    token = create_access_token({"company_id": company["id"]})
    return {"message": "Account creation successful. Logging you in", "token": token}



@router.post("/auth/login")
def login_company(data: CompanyLogin):
    try:
        # Query the database for a company with the provided email
        response = (
            supabase.table("companies")
            .select("*")
            .eq("email", str(data.email))
            .execute()
        )

        # If no company found, return generic error
        if not response.data:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        company = response.data[0]

        # Verify the plain password against the stored hash
        if not verify_password(data.password, company["password"]):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Password is correct - return a JWT token 
        token = create_access_token({"company_id": company["id"]})
        return {"message": "Login successful", "token": token}
    except HTTPException:
        raise
    except Exception as e:
        # Catch unexpected errors and return a clean message
        return {"message": f"Something went wrong: {str(e)}"}
