# Productivity App API - (Feature-First Architecture)

A Flask backend for a personal expense-tracking productivity app. Users register and authenticate with JWT bearer tokens, then create and manage their own expenses. Every expense query is scoped to the authenticated user's ID, so a user cannot list, retrieve, edit, or delete another user's data.

The repository also contains a supplied React JWT client. The backend is the assessed component; the client can be used to verify the login flow visually.

## What the API provides

- Bcrypt password hashing; password hashes are never returned in API responses.
- JWT signup, login, refresh, logout, and current-user endpoints.
- Full expense CRUD with `title`, `amount`, `description`, `date`, and `user_id` ownership.
- Paginated expense listing.
- Input validation using Marshmallow and database-level constraints.
- Token revocation after logout.
- Seed data, Alembic migrations, and automated integration tests.

## Security and ownership model

The client sends `Authorization: Bearer <access_token>` with every expense request. The server reads the user ID from that verified token; it never accepts a `user_id` from a client payload.

| Operation | Ownership protection |
| --- | --- |
| `GET /api/v1/expenses` | Filters the collection by the JWT user's ID. |
| `POST /api/v1/expenses` | Assigns the JWT user's ID to the new expense. |
| `GET/PATCH/DELETE /api/v1/expenses/<id>` | Looks up the expense using both its ID **and** the JWT user's ID. |

An expense that belongs to somebody else returns `404 Not Found`; this also prevents leaking whether another user's expense ID exists.

## Repository structure

```text
summative_productivity_app/
├── backend/                              # Flask API and database tooling
│   ├── app/
│   │   ├── __init__.py                    # Application factory; registers extensions and blueprints
│   │   ├── core/
│   │   │   ├── config/
│   │   │   │   ├── base.py                # Shared Flask/JWT/SQLAlchemy settings
│   │   │   │   ├── development.py         # Local SQLite configuration
│   │   │   │   ├── testing.py             # In-memory SQLite configuration for pytest
│   │   │   │   └── production.py          # Production database configuration
│   │   │   └── health/routes.py           # GET /api/v1/health
│   │   ├── extensions/
│   │   │   ├── database.py                # SQLAlchemy instance
│   │   │   ├── bcrypt.py                  # Bcrypt instance
│   │   │   ├── jwt.py                     # JWT manager, blocklist, token error responses
│   │   │   └── migrate.py                 # Flask-Migrate instance
│   │   └── features/                      # Feature-first application code
│   │       ├── auth/
│   │       │   ├── models/                # User, reset-token, and token-blocklist models
│   │       │   ├── schemas/               # Registration/login payload validation and serialization
│   │       │   ├── services.py            # User creation, authentication, token creation/revocation
│   │       │   └── routes.py              # Auth API and supplied-client compatibility routes
│   │       └── expenses/
│   │           ├── models/expense.py      # Expense database model and constraints
│   │           ├── schemas/expense_schema.py # Expense validation and response serialization
│   │           ├── services.py            # Owner-scoped expense business logic
│   │           └── routes.py              # Protected expense CRUD endpoints
│   ├── instance/app.db                    # Local SQLite database (ignored by Git)
│   ├── migrations/                        # Alembic migration environment and revisions
│   ├── tests/
│   │   ├── conftest.py                    # Isolated in-memory test application fixtures
│   │   └── test_productivity_api.py       # Auth, pagination, CRUD, and ownership tests
│   ├── .env.example                       # Environment-variable template
│   ├── requirements.txt                   # Python dependencies
│   ├── run.py                             # Local Flask entry point (port 5555)
│   └── seed.py                            # Rebuilds local data with sample users/expenses
├── client-with-jwt/                       # Supplied React client; not required for API testing
└── README.md                              # This guide
```

## Prerequisites

- Git
- Python 3.10 or newer
- pip
- Postman or cURL (optional, for manual API verification)

## Clone and install

```bash
git clone https://github.com/yeswadams/productivity_app_flask_backend.git
cd productivity_app_flask_backend/backend
```

Create and activate a virtual environment.

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process Bypass` and activate again.

**macOS/Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies and create your local environment file:

```bash
pip install -r requirements.txt
```

```powershell
Copy-Item .env.example .env
```

Use this minimum local `.env` configuration. Replace both secrets with long, different random values outside local development.

```env
FLASK_ENV=development
SECRET_KEY=replace-with-a-long-random-value
JWT_SECRET_KEY=replace-with-a-different-long-random-value
```

## Create the database and sample data

Apply migrations first:

```powershell
.\.venv\Scripts\python.exe -m flask --app run.py db upgrade
```

To create deterministic sample data, run:

```powershell
.\.venv\Scripts\python.exe seed.py
```

`seed.py` intentionally recreates the local development database. It creates `ada` and `sam` (both password `password123`) and three expenses. Do not run it against production or a database containing data you want to keep.

## Run the API

From `backend/`, with the virtual environment active:

```powershell
python run.py
```

The server starts at `http://localhost:5555`. Confirm it is live:

```bash
curl http://localhost:5555/api/v1/health
```

Expected response:

```json
{"status":"ok"}
```

## Endpoint reference

### React-client compatibility auth routes

| Method | Path | Request body | Success response |
| --- | --- | --- | --- |
| POST | `/signup` | `username`, `password`, `password_confirmation` | `201`, `{ "token", "user" }` |
| POST | `/login` | `username`, `password` | `200`, `{ "token", "user" }` |
| GET | `/me` | None; bearer token required | `200`, user object |

### Versioned auth routes

| Method | Path | Auth required | Purpose |
| --- | --- | --- | --- |
| POST | `/api/v1/auth/register` | No | Register a user. |
| POST | `/api/v1/auth/login` | No | Return access and refresh tokens. |
| POST | `/api/v1/auth/refresh` | Refresh token | Issue a new access token. |
| POST | `/api/v1/auth/logout` | Access token | Revoke the access token. |
| GET | `/api/v1/auth/me` | Access token | Return the current user. |

### Required expense CRUD routes

All expense routes require an access token.

| Method | Path | Purpose | Success status |
| --- | --- | --- | --- |
| GET | `/api/v1/expenses?page=1&per_page=10` | Paginated list of only the current user's expenses. `page >= 1`, `1 <= per_page <= 100`. | 200 |
| POST | `/api/v1/expenses` | Create an expense owned by the current user. | 201 |
| GET | `/api/v1/expenses/<id>` | Retrieve one expense owned by the current user. | 200 |
| PATCH | `/api/v1/expenses/<id>` | Update fields on one expense owned by the current user. | 200 |
| DELETE | `/api/v1/expenses/<id>` | Delete one expense owned by the current user. | 200 |

`title` is required on creation (1-120 characters) and `amount` must be greater than zero. `description` and ISO 8601 `date` are optional. PATCH accepts any subset of those fields.

## Validate the API with cURL

The following commands use two separate users to prove that access control works. Run them in a Bash-compatible terminal. On Windows, Git Bash or WSL works best for these examples.

```bash
BASE_URL=http://localhost:5555

# 1. Create Alice and save her access token.
ALICE_TOKEN=$(curl -s -X POST "$BASE_URL/signup" \
  -H 'Content-Type: application/json' \
  -d '{"username":"alice_demo","password":"secure-password","password_confirmation":"secure-password"}' \
  | python -c "import json,sys; print(json.load(sys.stdin)['token'])")

# 2. Alice creates an expense. Record the returned expense ID.
curl -X POST "$BASE_URL/api/v1/expenses" \
  -H "Authorization: Bearer $ALICE_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"title":"Groceries","amount":42.50,"description":"Weekly food shop"}'

# 3. Alice lists only her expenses, with pagination.
curl "$BASE_URL/api/v1/expenses?page=1&per_page=10" \
  -H "Authorization: Bearer $ALICE_TOKEN"

# 4. Replace EXPENSE_ID with an ID returned in steps 2 or 3.
EXPENSE_ID=1
curl -X PATCH "$BASE_URL/api/v1/expenses/$EXPENSE_ID" \
  -H "Authorization: Bearer $ALICE_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"amount":45.00,"description":"Updated grocery total"}'

# 5. Create Bob and prove he cannot access Alice's expense.
BOB_TOKEN=$(curl -s -X POST "$BASE_URL/signup" \
  -H 'Content-Type: application/json' \
  -d '{"username":"bob_demo","password":"secure-password","password_confirmation":"secure-password"}' \
  | python -c "import json,sys; print(json.load(sys.stdin)['token'])")

curl -i "$BASE_URL/api/v1/expenses/$EXPENSE_ID" \
  -H "Authorization: Bearer $BOB_TOKEN"
# Expected: HTTP/1.1 404 NOT FOUND

# 6. Alice may delete her own expense.
curl -X DELETE "$BASE_URL/api/v1/expenses/$EXPENSE_ID" \
  -H "Authorization: Bearer $ALICE_TOKEN"
```

For Windows PowerShell, use `Invoke-RestMethod` with `-Headers @{ Authorization = "Bearer $token" }`; the endpoint paths and JSON bodies are otherwise identical.

## Validate with Postman

1. Create an environment named `Productivity App` with `base_url` set to `http://localhost:5555` and blank variables `alice_token`, `bob_token`, and `expense_id`.
2. Send `POST {{base_url}}/signup` with raw JSON body:

   ```json
   {"username":"alice_postman","password":"secure-password","password_confirmation":"secure-password"}
   ```

3. Copy the `token` in the response into `alice_token`.
4. Send `POST {{base_url}}/api/v1/expenses`. Set Authorization to **Bearer Token** and use `{{alice_token}}`. Use this body:

   ```json
   {"title":"Postman expense","amount":20.5,"description":"Created in Postman"}
   ```

5. Copy `expense.id` from the `201` response into `expense_id`.
6. Send `GET {{base_url}}/api/v1/expenses?page=1&per_page=10` with the same bearer token. The response contains the collection and a `pagination` object.
7. Send `PATCH {{base_url}}/api/v1/expenses/{{expense_id}}` with Alice's token and a partial JSON body such as `{ "amount": 25.0 }`.
8. Create and log in a second user, save their token as `bob_token`, then use it to call `GET`, `PATCH`, or `DELETE {{base_url}}/api/v1/expenses/{{expense_id}}`. Each must return `404`.
9. Repeat DELETE with `alice_token`; it must return `200`.

## Automated tests

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest -q
```

The test suite verifies signup/login compatibility, unauthenticated request rejection, pagination, expense CRUD, and cross-user read/delete denial.

## Common issues

- **`401 Missing Authorization Header`**: add `Authorization: Bearer <token>` to protected requests.
- **`422` validation response**: check required fields, password length (at least 8), positive amount, and ISO 8601 date format.
- **`404 Expense not found or access denied`**: the ID does not exist or belongs to another user; use the owning user's token.
- **Port 5555 is busy**: stop the existing Flask process before starting `python run.py` again.


