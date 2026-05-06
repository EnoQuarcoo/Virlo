# Virlo

**Virlo** is a B2B referral marketing platform that lets companies launch and manage referral campaigns in minutes. Companies sign up, create a campaign, and each participant gets a unique referral link. Virlo tracks referrals in real time, ranks participants on a live leaderboard, and exposes an API so companies can integrate referral tracking directly into their own products.

---

## Features

- **Company accounts** — Secure signup and login with bcrypt-hashed passwords and JWT authentication
- **Campaign creation** — Create referral campaigns with a name, description, reward, and campaign URL
- **Unique referral links** — Every participant who joins a campaign receives a unique, shareable referral link built from the campaign URL
- **Referral tracking** — Referral conversions are tracked via a single API call, automatically incrementing the referrer's count and logging the referred email
- **Live leaderboard** — Each campaign has a public leaderboard ranked by referral count, updated in real time as referrals come in
- **API key** — Every company account is issued a `vrl_` prefixed API key at registration for use with the Virlo tracking endpoint

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| Database | PostgreSQL via Supabase |
| Auth | JWT (python-jose), bcrypt (passlib) |
| Frontend | React 19, React Router v7 |
| Build tool | Vite |
| Backend hosting | Render |
| Frontend hosting | Vercel |

---

## Project Structure

```
virlo/
├── backend/
│   ├── main.py                  # App entry point, CORS, router registration
│   ├── requirements.txt
│   └── app/
│       ├── config.py            # Loads environment variables
│       ├── models/              # Pydantic request/response schemas
│       │   ├── campaign.py
│       │   ├── company.py
│       │   ├── referral.py
│       │   └── referrer.py
│       ├── routers/             # Route handlers grouped by domain
│       │   ├── campaigns.py
│       │   ├── companies.py
│       │   ├── leaderboards.py
│       │   ├── referrals.py
│       │   └── referrers.py
│       └── services/
│           ├── auth.py          # JWT, bcrypt, API key helpers
│           └── database.py      # Supabase client singleton
└── frontend/
    └── src/
        ├── config.js            # API base URL
        ├── App.jsx              # Route definitions
        ├── components/
        │   ├── Navbar.jsx
        │   └── Footer.jsx
        └── pages/
            ├── LandingPage.jsx
            ├── SignupPage.jsx
            ├── LoginPage.jsx
            ├── Dashboard.jsx
            ├── CreateCampaign.jsx
            └── CampaignDetail.jsx
```

---

## API Endpoints

### Auth

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/auth/register` | None | Create a company account, returns JWT |
| `POST` | `/auth/login` | None | Login, returns JWT |
| `GET` | `/company/me` | JWT | Get the company's API key |

### Campaigns

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/campaigns` | JWT | Create a new campaign |
| `GET` | `/campaigns` | JWT | List all campaigns for the authenticated company |

### Referrers

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/campaigns/{campaign_id}/signup` | None | Register as a referrer, returns unique referral link |

### Referrals

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/referrals/track` | None | Track a referral conversion by referral code |

### Leaderboard

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/campaigns/{campaign_id}/leaderboard` | None | Get referrers ranked by referral count |

Referrer signup, referral tracking, and the leaderboard are intentionally public — they are called from your campaign page, not from the Virlo dashboard.

---

## Running Locally

### Prerequisites

- Python 3.11+
- Node.js 18+
- A [Supabase](https://supabase.com) project with the following tables: `companies`, `campaigns`, `referrers`, `referrals`

---

### Backend

```bash
cd backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create a .env file
cp .env.example .env            # or create it manually (see below)

# Start the server
uvicorn main:app --reload
```

**Required environment variables** (create a `backend/.env` file):

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-or-service-key
JWT_SECRET=a-long-random-secret-string
```

The API will be available at `http://127.0.0.1:8000`. FastAPI auto-generates interactive docs at `http://127.0.0.1:8000/docs`.

---

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Point the frontend at your local backend
# Edit src/config.js:
#   export const API_URL = "http://127.0.0.1:8000"

# Start the dev server
npm run dev
```

The frontend will be available at `http://localhost:5173`.

---

## Deployment Notes

### Backend — Render

The backend is deployed on Render's free tier. Free tier instances spin down after periods of inactivity, so **the first request after a period of inactivity may take 30–60 seconds** while the instance boots. Subsequent requests will respond at normal speed.

### Frontend — Vercel

The frontend is deployed on Vercel. `src/config.js` holds the backend base URL and is the only file that needs updating if the backend URL changes.

---

## Roadmap

The following features are planned for future development:

- **Email notifications** — Welcome emails to new referrers and conversion alerts to companies
- **Duplicate referral detection** — Prevent the same email from being counted more than once per campaign
- **Campaign analytics dashboard** — Charts showing referral volume over time, top referrers, and conversion trends
- **Campaign expiry enforcement** — Automatically close campaigns past their `expires_at` date
- **Custom reward tiers** — Different rewards at different referral count milestones
- **Embeddable signup widget** — Drop-in JavaScript widget so companies can add a referrer signup form to any page without building one
- **Webhook support** — Fire a webhook to the company's backend on each successful referral conversion
- **Multi-user company accounts** — Allow multiple team members to access the same company dashboard
- **API key rotation** — Let companies invalidate and regenerate their API key from the dashboard
- **White-label leaderboard page** — A hosted, public leaderboard page companies can link to directly

---

## License

This project is not currently open source. All rights reserved.
