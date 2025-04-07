# {{ project_name }}

{{ project_description }}

## Features

- FastAPI with SQLModel for enhanced type safety
- JWT Authentication with fastapi-users
- SQLAdmin for automatic admin panel
- PostgreSQL database with async support
- Email verification
- Docker support with Traefik for secure HTTPS
- Alembic for database migrations

## Getting Started

### Prerequisites

- Python 3.12+
- Docker and Docker Compose (for containerized deployment)
- PostgreSQL (or use the provided Docker service)

### Development Setup

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -e .
   ```
4. Create a `.env` file with the required environment variables (see .env.example)
5. Run the development server:
   ```
   uvicorn app.main:app --reload
   ```

### Using Docker

For development with Docker:
```
cd docker/compose
docker-compose up -d
```

For production with Docker:
```
cd docker/compose
docker-compose -f docker-compose.prod.yml up -d
```

## API Documentation

Once running, access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Admin Panel

The admin panel is available at http://localhost:8000/admin

## Running Migrations

To run database migrations:

```bash
alembic upgrade head
```

To create a new migration:

```bash
alembic revision --autogenerate -m "Description of changes"
```
