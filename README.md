# Development Container for Python, FastAPI, React TypeScript, and PostgreSQL

This repository contains a development container configuration for a full-stack application using Python 3.11, FastAPI 0.109, React 18 with TypeScript, and PostgreSQL 15.

## Tech Stack

### Backend
- **Python 3.11**
- **FastAPI 0.109**
- **SQLAlchemy 2.0**
- **pytest 7.2**
- **PostgreSQL 15**

### Frontend
- **React 18**
- **TypeScript**
- **Node.js 18**

## Getting Started

### Prerequisites
- [Visual Studio Code](https://code.visualstudio.com/)
- [Docker](https://www.docker.com/products/docker-desktop)
- [VS Code Remote - Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Setup Instructions

1. Clone this repository
2. Open the repository in VS Code
3. When prompted, click "Reopen in Container" or run the "Remote-Containers: Reopen in Container" command from the command palette
4. Wait for the container to build and initialize (this may take a few minutes the first time)

## Development Environment

The development container includes:

- Python 3.11 with FastAPI and required packages
- PostgreSQL 15 database
- Node.js and npm for React development with TypeScript
- VS Code extensions for Python, TypeScript, React, and PostgreSQL development
- Pre-configured settings for linting, formatting, and testing

## Environment Variables

A sample `.env.example` file is provided with common environment variables. Copy this file to `.env` and modify as needed:

```bash
cp .env.example .env
```

## Port Forwarding

The following ports are forwarded from the container to your local machine:

- **8000**: FastAPI backend
- **5432**: PostgreSQL database
- **3000**: React development server

## Working with the Stack

### Backend (FastAPI)

The Python virtual environment is automatically activated in the container. You can start the FastAPI server with:

```bash
cd backend  # If you have a backend directory
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (React TypeScript)

To create a new React TypeScript project:

```bash
npx create-react-app frontend --template typescript
cd frontend
npm start
```

### Database (PostgreSQL)

The PostgreSQL database is available at:

- **Host**: db
- **Port**: 5432
- **Username**: postgres
- **Password**: postgres
- **Database**: postgres

You can connect to the database using the VS Code PostgreSQL extension or with psql:

```bash
psql -h db -U postgres
```

## Additional Information

- The container includes common development tools and extensions
- Code formatting and linting are configured to run on save
- The PostgreSQL data is persisted in a Docker volume
