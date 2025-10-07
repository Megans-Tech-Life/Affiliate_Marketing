# Affiliate Marketing Accounts API – Part 1

## Overview

Backend service for an Affiliate Marketing page that manages B2B accounts and their progression through sales pipeline.

### Authentication

- User registration (`/auth/register`)
- User login (`/auth/login`)
- Retrieve current user info (`/auth/me`) using JWT token

### Leads Management (CRUD)

- **Create** a new lead: `POST /leads/`
- **Retrieve** all leads: `GET /leads/`
- **Retrieve** a specific lead by UUID: `GET /leads/{lead_id}`
- **Update** a lead by UUID: `PUT /leads/{lead_id}`
- **Delete** a lead by UUID: `DELETE /leads/{lead_id}`

## Technology Stack

- **Python 3.11+**
- **FastAPI** for building the API
- **SQLAlchemy** for ORM
- **PostgreSQL** as the database
- **Passlib + bcrypt** for password hashing
- **JWT** for authentication

## Getting Started

1. Clone the repository
2. Set up a virtual environment
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure your database connection in .env (PostgreSQL)
5. Run the API:

```bash
uvicorn main:app --reload
```

6. Test endpoints using Postman or any API client
