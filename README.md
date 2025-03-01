# Resource Management System

A full-stack application for managing resources with secure authentication and efficient data retrieval.

## Project Overview

This project is a Python Full-Stack Assessment that demonstrates proficiency in Python development, database optimization, and secure authentication. It implements a Resource Management System that allows users to create, manage, and access resources with proper authentication and authorization.

## Features

- User authentication and authorization with JWT
- Role-based access control (RBAC)
- Resource management with ownership and sharing
- Efficient data retrieval with pagination and filtering
- Caching for improved performance
- Comprehensive error handling

## Tech Stack

### Backend
- Python 3.11
- FastAPI 0.109
- SQLAlchemy 2.0
- PostgreSQL 15
- Alembic for migrations
- Pytest for testing

### Frontend (Coming Soon)
- React 18
- TypeScript
- React Router
- React Query
- Formik & Yup
- Tailwind CSS

## Project Structure

The project follows a clean, layered architecture:

```
project/
├── backend/             # Backend application
│   ├── app/             # Application code
│   │   ├── api/         # API routes and controllers
│   │   ├── core/        # Core functionality
│   │   ├── db/          # Database configuration
│   │   ├── models/      # Database models
│   │   ├── repositories/# Data access layer
│   │   ├── schemas/     # Data validation and serialization
│   │   ├── services/    # Business logic
│   │   ├── tests/       # Tests
│   │   └── utils/       # Utilities
│   ├── alembic/         # Database migrations
│   ├── requirements.txt # Dependencies
│   └── README.md        # Backend documentation
└── frontend/            # Frontend application (Coming Soon)
```

## Getting Started

### Backend

See the [backend README](backend/README.md) for detailed instructions on setting up and running the backend.

### Frontend

Coming soon.

## User Stories

1. **Efficient Data Retrieval**
   - Retrieve large datasets with pagination and filtering
   - Optimize database queries for performance
   - Implement caching strategies for frequently accessed data

2. **Secure Authentication**
   - Implement user registration and authentication
   - Ensure secure password storage and handling
   - Implement role-based access control (RBAC)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
