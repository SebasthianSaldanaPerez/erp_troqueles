# Troqueles ERP Backend

Backend API for the Troqueles ERP system.

## Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pytest
- JWT authentication
- Argon2 password hashing

## Requirements

- Python 3.12+
- Docker
- Docker Compose

## Environment


Create a `.env` file based on `.env.example`.

Required variables:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/troqueles
DATABASE_TEST_URL=postgresql+psycopg://postgres:postgres@localhost:5432/troqueles_test

JWT_SECRET_KEY=change-me
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

```

## Setup

Create virtual environment:

```bash
python -m venv .venv

```

# Activate

.venv\Scripts\Activate.ps1

# Install Dependecies

pip install -r requirements.txt

# Start PostgreSQL

From the project root:

docker compose -f docker/docker-compose.yml up -d postgres

# Run Migrations

From backend/:

alembic upgrade head

# Create First Admin User

python -m scripts.create_admin

# Run APPI

fastapi dev src/presentation/api/main.py

# Swagger

http://127.0.0.1:8000/docs

# Health

http://127.0.0.1:8000/health

## Run Tests

# All Tests

python -m pytest

# API Tests

python -m pytest tests/api -v