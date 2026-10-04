# SalonFlow MVP

A small local MVP for a salon appointment/WhatsApp automation SaaS.

## What it does

- Customer management
- Service management
- Appointment creation
- Appointment conflict checking
- Appointment status updates
- Basic availability API
- JSON API endpoints ready for future WhatsApp integration
- SQLite database
- Simple responsive dashboard

## Requirements

Python 3.10+ recommended.

## Run on Windows

Open PowerShell in this folder:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs

Health check:

http://127.0.0.1:8000/health

## Run on Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Important

This is an MVP, not a production SaaS.

Before accepting real customers, add:

- User/business authentication
- Tenant isolation
- HTTPS
- Production database
- Backups
- Rate limiting
- Payment/subscription handling
- WhatsApp Business Cloud API integration
- Webhook signature verification
- Message usage limits
- Proper logging/monitoring
- Privacy policy and terms
- Secure secrets management

## Planned production architecture

Frontend:
S3 + CloudFront

Backend:
API Gateway + Lambda

Database:
DynamoDB

AI:
Amazon Bedrock

Messaging:
WhatsApp Business Cloud API

Files:
S3

Monitoring:
CloudWatch

Do not put AWS credentials or WhatsApp access tokens into source code.
