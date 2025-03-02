# Resource Management System

A full-stack application for managing resources with secure authentication and efficient data retrieval.

## Project Overview

This project is a Python Full-Stack Assessment that demonstrates proficiency in Python development, database optimization, and secure authentication. It implements a Resource Management System that allows users to create, manage, and access resources with proper authentication and authorization.

## Features

- User authentication and authorization with JWT
- Role-based access control (RBAC)
  - Admin users can access all resources
  - Regular users can only access their own resources or shared resources
- Resource management with ownership and sharing
- Efficient data retrieval with pagination, filtering, and sorting
- Advanced caching strategies for improved performance
- Comprehensive error handling
- Responsive UI with modern design

## Tech Stack

### Backend
- Python 3.11
- FastAPI 0.109
- SQLAlchemy 2.0
- PostgreSQL 15
- Alembic for migrations
- Pytest for testing
- Pydantic for data validation

### Frontend
- React 18
- TypeScript
- React Router for navigation
- React Query for data fetching and caching
- Axios for API integration
- CSS for styling

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
├── frontend/            # Frontend application
│   ├── public/          # Static files
│   ├── src/             # Source code
│   │   ├── api/         # API integration
│   │   ├── components/  # React components
│   │   ├── contexts/    # React contexts
│   │   ├── pages/       # Page components
│   │   ├── types/       # TypeScript type definitions
│   │   └── utils/       # Utility functions
│   ├── package.json     # Dependencies and scripts
│   └── README.md        # Frontend documentation
└── RBAC_DEMO.md         # RBAC demonstration guide
```

## Getting Started

### Backend

See the [backend README](backend/README.md) for detailed instructions on setting up and running the backend.

### Frontend

See the [frontend README](frontend/README.md) for detailed instructions on setting up and running the frontend.

### RBAC Demo

See the [RBAC Demo](RBAC_DEMO.md) for instructions on demonstrating the role-based access control features.

## User Stories

1. **Efficient Data Retrieval**
   - Retrieve large datasets with pagination, filtering, and sorting
   - Optimize database queries for performance
   - Implement caching strategies for frequently accessed data
   - Provide a responsive UI for data exploration

2. **Secure Authentication**
   - Implement user registration and authentication
   - Ensure secure password storage and handling
   - Implement role-based access control (RBAC)
   - Provide different access levels for admin and regular users

## License

This project is licensed under the MIT License - see the LICENSE file for details.
