# Resource Management System - Backend

This is the backend for the Resource Management System, a Python Full-Stack Assessment project. It provides a RESTful API for managing resources with secure authentication and efficient data retrieval.

## Features

- User authentication and authorization with JWT
- Role-based access control (RBAC)
- Resource management with ownership and sharing
- Efficient data retrieval with pagination and filtering
- Caching for improved performance
- Comprehensive error handling
- Database migrations with Alembic

## Tech Stack

- Python 3.11
- FastAPI 0.109
- SQLAlchemy 2.0
- PostgreSQL 15
- Alembic for migrations
- Pytest for testing

## Project Structure

The project follows a clean, layered architecture:

- **API Layer**: FastAPI routes and controllers
- **Service Layer**: Business logic
- **Repository Layer**: Data access
- **Model Layer**: Database models
- **Schema Layer**: Data validation and serialization

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL 15+

### Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file based on `.env.example`
5. Run database migrations:
   ```bash
   alembic upgrade head
   ```
6. Start the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

### API Documentation

Once the server is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

### Creating Migrations

To create a new migration:

```bash
alembic revision --autogenerate -m "Description of changes"
```

To apply migrations:

```bash
alembic upgrade head
```

### Running Tests

```bash
pytest
```

## API Endpoints

### Authentication

- `POST /api/v1/auth/register`: Register a new user
- `POST /api/v1/auth/login`: Login and get access token

### Users

- `GET /api/v1/users/`: Get all users (admin only)
- `POST /api/v1/users/`: Create a new user (admin only)
- `GET /api/v1/users/me`: Get current user
- `PUT /api/v1/users/me`: Update current user
- `GET /api/v1/users/{user_id}`: Get user by ID
- `PUT /api/v1/users/{user_id}`: Update user
- `DELETE /api/v1/users/{user_id}`: Delete user

### Resources

- `GET /api/v1/resources/`: Get resources with filtering
- `GET /api/v1/resources/me`: Get current user's resources
- `POST /api/v1/resources/`: Create a new resource
- `GET /api/v1/resources/{id}`: Get resource by ID
- `PUT /api/v1/resources/{id}`: Update resource
- `DELETE /api/v1/resources/{id}`: Delete resource
- `POST /api/v1/resources/{id}/share`: Share resource with a user
- `DELETE /api/v1/resources/{id}/share/{user_id}`: Unshare resource from a user
