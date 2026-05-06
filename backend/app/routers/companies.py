from fastapi import APIRouter, HTTPException, Header
from app.models.company import CompanySignup, CompanyLogin
from app.services.auth import hash_password, verify_password, create_access_token, generate_api_key, get_company_id_from_token
from app.services.database import supabase


router = APIRouter()


@router.post("/auth/register")
def signup_company(data: CompanySignup):
    hashed = hash_password(data.password)

    # Generate the API key at registration so every company has one immediately.
    # We don't wait for them to request it because it's needed to integrate the
    # Virlo SDK and requiring an extra step would create friction.
    api_key = generate_api_key()

    response = (supabase.table("companies")
                .insert({
                    "name": data.name,
                    "email": data.email,
                    "password": hashed,
                    "website_url": str(data.website_url),
                    "company_information": data.company_information,
                    "company_vibe": data.company_vibe,
                    "api_key": api_key
                })
                .execute()
                )
    company = response.data[0]
    # Return a JWT immediately after registration so the frontend can auto-login
    # the user without requiring a separate login step.
    token = create_access_token({"company_id": company["id"]})
    return {"message": "Account creation successful. Logging you in", "token": token}


@router.post("/auth/login")
def login_company(data: CompanyLogin):
    try:
        response = (
            supabase.table("companies")
            .select("*")
            .eq("email", str(data.email))
            .execute()
        )

        # Use the same error message whether the email doesn't exist or the
        # password is wrong. Distinct messages would let an attacker enumerate
        # which emails are registered.
        if not response.data:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        company = response.data[0]

        if not verify_password(data.password, company["password"]):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        token = create_access_token({"company_id": company["id"]})
        return {"message": "Login successful", "token": token}
    except HTTPException:
        # Re-raise auth errors so FastAPI returns the correct 401 status.
        # Without this, the outer `except Exception` would swallow them and
        # return a 200 with an error message body instead.
        raise
    except Exception as e:
        return {"message": f"Something went wrong: {str(e)}"}


@router.get("/company/me")
def get_api_key(authorization: str = Header(None)):
    # company_id is extracted from the JWT rather than accepted as a query
    # parameter. This ensures a company can only retrieve their own API key.
    company_id = get_company_id_from_token(authorization)

    response = (
        supabase.table("companies")
        .select("api_key")
        .eq("id", company_id)
        .execute()
    )

    return {"api_key": response.data[0]["api_key"]}
    