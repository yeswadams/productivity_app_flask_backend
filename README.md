# Productivity App API

A Flask REST API for a personal expense tracker. It uses JWT bearer tokens for authentication and enforces ownership at every expense endpoint, so one user cannot read, change, or delete another user's data. The backend follows a feature-first structure: each feature owns its routes, schemas, services, and models.

## Features

- Secure registration and login with bcrypt password hashing
- JWT access and refresh tokens, token revocation on logout, and a current-user endpoint
- Expense CRUD: title, amount, optional description, date, and owning user
- Server-side pagination on the expense collection
- Input validation through Marshmallow and database constraints
- Development seed script, Flask-Migrate migration, and pytest coverage for the auth flow, pagination, and ownership protection
- Compatibility routes for the provided React JWT client, alongside a versioned API for future clients

## Project layout

```text
backend/
  app/
    core/                 # environment configuration and health check
    extensions/           # SQLAlchemy, JWT, bcrypt, and migrations
    features/
      auth/               # authentication models, schemas, service, routes
      expenses/           # expense models, schemas, service, routes
  migrations/             # Flask-Migrate/Alembic revision history
  tests/                  # API integration tests
  run.py                  # Flask entry point
  seed.py                 # development data
```

## Prerequisites

- Python 3.10 or newer
- pip and a virtual environment

## Installation

From the repository root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Set secure values in `backend/.env` before using a shared or production environment:

```env
FLASK_ENV=development
SECRET_KEY=replace-with-a-long-random-value
JWT_SECRET_KEY=replace-with-a-different-long-random-value
```

## Database setup and seed data

Run the existing migration to create the SQLite database, then add sample records:

```powershell
flask --app run.py db upgrade
python seed.py
```

`seed.py` recreates the development database and adds two users (`ada` and `sam`), both with password `password123`, plus three expenses. Do not run it against production data.

## Run the API

```powershell
cd backend
python run.py
```

The development server listens at `http://localhost:5555`. Check it with `GET /api/v1/health`.

## Authentication

Send the access token in every protected request:

```http
Authorization: Bearer <access_token>
```

The supplied React client calls the unversioned routes below. They are intentionally retained for compatibility.

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/signup` | Create a user and return `{ token, user }`. Requires `username`, `password`, and `password_confirmation`. |
| POST | `/login` | Authenticate and return `{ token, user }`. |
| GET | `/me` | Return the authenticated user. |

## Versioned API

### Auth endpoints

| Method | Path | Authentication | Description |
| --- | --- | --- | --- |
| POST | `/api/v1/auth/register` | No | Register a user. |
| POST | `/api/v1/auth/login` | No | Return an access token, refresh token, and user. |
| POST | `/api/v1/auth/refresh` | Refresh token | Exchange a refresh token for a new access token. |
| POST | `/api/v1/auth/logout` | Access token | Revoke the current access token. |
| GET | `/api/v1/auth/me` | Access token | Return the authenticated user in a `user` envelope. |

### Expense endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | `/api/v1/expenses?page=1&per_page=10` | Return only the caller's expenses and pagination metadata. `per_page` is 1–100. |
| POST | `/api/v1/expenses` | Create an expense for the caller. |
| GET | `/api/v1/expenses/<id>` | Return one of the caller's expenses. |
| PATCH | `/api/v1/expenses/<id>` | Partially update one of the caller's expenses. |
| DELETE | `/api/v1/expenses/<id>` | Delete one of the caller's expenses. |

`POST` accepts `title` (1–120 characters), positive `amount`, and optional `description` and ISO 8601 `date`. Updates accept any subset of those fields. An expense outside the caller's ownership is treated as not found (404), avoiding disclosure of another user's records.

## Example request

```powershell
$login = Invoke-RestMethod -Method Post -Uri http://localhost:5555/login `
  -ContentType 'application/json' `
  -Body '{"username":"ada","password":"password123"}'

Invoke-RestMethod -Method Post -Uri http://localhost:5555/api/v1/expenses `
  -Headers @{ Authorization = "Bearer $($login.token)" } `
  -ContentType 'application/json' `
  -Body '{"title":"Coffee","amount":3.50,"description":"Morning coffee"}'
```

## Tests

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest -q
```

The suite exercises React-client authentication compatibility, protected expense CRUD, pagination, and cross-user access denial.
