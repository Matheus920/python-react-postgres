# Resource Management System - Backend

This is the backend for the Resource Management System, a Python Full-Stack Assessment project. It provides a RESTful API for managing resources with secure authentication and efficient data retrieval.

## Features

- User authentication and authorization with JWT
- Role-based access control (RBAC)
  - Admin users can access all resources
  - Regular users can only access resources they own or have been shared with them
- Resource management with ownership and sharing
- Efficient data retrieval with pagination, filtering, and sorting
- Advanced caching strategies with cache invalidation
- Comprehensive error handling
- Database migrations with Alembic

## Tech Stack

- Python 3.11
- FastAPI 0.109
- SQLAlchemy 2.0 with async support
- Pydantic v2 for data validation
- PostgreSQL 15
- Alembic for migrations
- Pytest for testing
- Passlib for password hashing
- Python-jose for JWT token handling

## Project Structure

The project follows a clean, layered architecture:

- **API Layer**: FastAPI routes and controllers
- **Service Layer**: Business logic and coordination
- **Repository Layer**: Data access with caching
- **Model Layer**: Database models with relationships
- **Schema Layer**: Data validation and serialization
- **Utils Layer**: Utilities for caching, pagination, etc.

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
6. Create test users (optional):
   ```bash
   python create_test_user.py  # Creates an admin user
   python create_regular_user.py  # Creates a regular user
   ```
7. Start the development server:
   ```bash
   uvicorn app.main:app --reload
   # or
   python run.py
   ```

### API Documentation

Once the server is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Testing the API

You can use the provided test scripts to verify the API functionality:

```bash
# Test resource implementation
python test_resources.py

# Test filtering functionality
python test_filtering.py

# Test sorting functionality
python test_sorting.py

# Test RBAC implementation
python test_auth_resource.py
```

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

### Seeding the Database

The application includes a comprehensive seed data system for testing:

```python
from app.db.seed import seed_db

# Seed the database with test data
await seed_db(db, force=True)
```

## Key Features

### Role-Based Access Control (RBAC)

The system implements two types of users with different permission levels:

1. **Admin Users**: Can access, modify, and manage all resources in the system, regardless of ownership.
2. **Regular Users**: Can only access resources they own or resources that have been explicitly shared with them.

The RBAC implementation is primarily handled in the `resource_service.py` file:

- Admin users can see all resources with applied filters
- Regular users can only see resources they own or resources shared with them
- Admin users can update any resource, while regular users can only update resources they own
- Admin users can delete any resource, while regular users can only delete resources they own

### Caching System

The application implements an advanced caching system to improve performance:

- In-memory caching for frequently accessed data
- Cache invalidation on data updates
- Configurable cache expiration
- Cache key generation based on function name and arguments
- Cache statistics and monitoring

The caching implementation is in the `utils/caching.py` file and is used throughout the application, particularly in the repository layer.

### Filtering and Sorting

The resource API supports comprehensive filtering and sorting:

- Filter by owner
- Filter by public status
- Filter by search term (name or description)
- Sort by various fields (name, id, created_at, updated_at)
- Sort in ascending or descending order
- Combine filtering and sorting for advanced data retrieval

### Pagination

The API implements efficient pagination for large datasets:

- Skip and limit parameters for pagination
- Total count for accurate pagination
- Page information (current page, total pages, has_next, has_prev)

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

- `GET /api/v1/resources/`: Get resources with filtering, sorting, and pagination
- `GET /api/v1/resources/me`: Get current user's resources
- `POST /api/v1/resources/`: Create a new resource
- `GET /api/v1/resources/{id}`: Get resource by ID
- `PUT /api/v1/resources/{id}`: Update resource
- `DELETE /api/v1/resources/{id}`: Delete resource
- `POST /api/v1/resources/{id}/share`: Share resource with a user
- `DELETE /api/v1/resources/{id}/share/{user_id}`: Unshare resource from a user

### Cache Management

- `GET /api/v1/cache/stats`: Get cache statistics
- `DELETE /api/v1/cache/`: Clear all cache
- `DELETE /api/v1/cache/expired`: Clear expired cache
