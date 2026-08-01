# Productivity App  Flask Backend

## Project Description
This repository contains a production-style flask backend  
 for a productivity app. The project demonstrates  a proffesional backend architecture using flask, SQLAlchemy, Marshmallow, and pytest.

 ## Features
 - 
 - 
 - 

## Project Structure

```text
Summative_Productivity_App/
├── app/
│   ├── __init__.py
│   ├── core/
|   |   ├── config
|   │   ├── errors
|   │   ├── health
|   │   └── security
│   ├── extensions/
|   |   ├── __init__.py
|   │   ├── database.py
|   │   ├── marshmallow.py
|   │   └── migrate.py
│   └── features/
├── instance/
│   └── app.db
├── tests/
│   ├── conftest.py
│   ├── test_constraints.py
│   ├── test_validations.py
│   └── test_workout_api.py
├── config.py
├── pytest.ini
├── README.md
├── requirements.txt
├── run.py
└── seed.py
```

## Prerequisites
- Python 3.10+
- Git
- pip, pipenv / virtualenvironment

### 1. Clone the Repository
```bash
git clone  git@github.com:yeswadams/productivity_app_flask_backend.git
```

### 2. Create and Activate a Virtual Environment
- **Windows (PowerShell)**:
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```
- **macOS / Linux**:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
