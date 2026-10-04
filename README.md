# SalonFlow MVP

**WhatsApp-based appointment booking assistant for salons — FastAPI + SQLite MVP.**

## The problem

Salons lose bookings when customers can't reach the front desk — missed calls, no-shows, and manual scheduling eat up staff time. SalonFlow is an MVP backend exploring automated appointment booking through WhatsApp-style conversational flows.

## Key features

- Customer and service management
- Appointment creation with conflict checking
- Appointment status updates (e.g. confirmed, cancelled)
- Availability and booking JSON APIs, structured for future WhatsApp integration
- Simple responsive web dashboard
- Interactive API docs via FastAPI/Swagger

## Tech stack

- Python 3.10+, FastAPI
- SQLite
- Uvicorn
- Plain HTML/CSS dashboard

## Run locally

Requirements: Python 3.10+ recommended.

**Windows** (PowerShell, from this folder):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open:

- Dashboard: http://127.0.0.1:8000
- API docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## Project status

This is an **MVP/demo**, not a production SaaS. It runs locally with a SQLite database and has no authentication, multi-tenant isolation, payments, or production hardening.

WhatsApp integration is **planned but not live** — the API is structured to support a WhatsApp Business Cloud API webhook later (webhook signature verification, message usage limits, and secrets handling would need to be added first).

⚠️ Do not put AWS credentials or WhatsApp access tokens into source code.
