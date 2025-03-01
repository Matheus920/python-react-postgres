# Resource Management System - Frontend

This is the frontend application for the Resource Management System, built with React, TypeScript, and React Query.

## Features

- User authentication (login, register)
- Resource management (create, read, update, delete)
- Efficient data retrieval with pagination, filtering, and sorting
- Caching for improved performance
- Role-based access control

## Project Structure

```
frontend/
├── public/              # Static files
├── src/                 # Source code
│   ├── api/             # API integration
│   │   ├── authApi.ts   # Authentication API
│   │   └── resourcesApi.ts # Resources API
│   ├── components/      # React components
│   │   ├── auth/        # Authentication components
│   │   ├── resources/   # Resource-related components
│   │   └── shared/      # Shared components
│   ├── contexts/        # React contexts
│   │   └── AuthContext.tsx # Authentication context
│   ├── pages/           # Page components
│   │   ├── LoginPage.tsx
│   │   ├── RegisterPage.tsx
│   │   ├── ResourceListPage.tsx
│   │   ├── ResourceDetailPage.tsx
│   │   └── ResourceCreateEditPage.tsx
│   ├── types/           # TypeScript type definitions
│   │   ├── auth.ts      # Authentication types
│   │   ├── common.ts    # Common types
│   │   └── resource.ts  # Resource types
│   ├── utils/           # Utility functions
│   │   └── axios.ts     # Axios instance with interceptors
│   ├── App.tsx          # Main App component
│   ├── App.css          # App-specific styles
│   ├── index.tsx        # Entry point
│   └── index.css        # Global styles
├── package.json         # Dependencies and scripts
└── tsconfig.json        # TypeScript configuration
```

## Key Components

### Authentication

- **AuthContext**: Provides authentication state and functions to the entire application
- **LoginPage**: User login form
- **RegisterPage**: User registration form
- **ProtectedRoute**: Route wrapper that requires authentication

### Resource Management

- **ResourceListPage**: Main page for viewing resources with pagination, filtering, and sorting
- **ResourceDetailPage**: Page for viewing a single resource
- **ResourceCreateEditPage**: Page for creating and editing resources
- **ResourceTable**: Table component for displaying resources
- **FilterControls**: Component for filtering resources
- **SortControls**: Component for sorting resources
- **Pagination**: Component for paginating through resources

## User Story #1: Efficient Data Retrieval

The frontend implementation for User Story #1 focuses on efficient data retrieval with pagination, filtering, and sorting. Key features include:

1. **Pagination**: The `Pagination` component allows users to navigate through large datasets with ease.
2. **Filtering**: The `FilterControls` component provides options for filtering resources by various criteria.
3. **Sorting**: The `SortControls` component allows users to sort resources by different fields.
4. **Caching**: React Query is used for data fetching and caching, improving performance for frequently accessed data.

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

1. Clone the repository
2. Navigate to the frontend directory
3. Install dependencies:

```bash
npm install
# or
yarn install
```

### Running the Application

```bash
npm start
# or
yarn start
```

The application will be available at http://localhost:3000.

### Running Tests

The project includes comprehensive tests for components and pages. To run the tests:

```bash
# Run tests in watch mode
npm test
# or
yarn test

# Run tests with coverage report
npm run test:coverage
# or
yarn test:coverage
```

The test suite includes:
- Unit tests for individual components
- Integration tests for pages
- Mock API tests using MSW (Mock Service Worker)

### Building for Production

```bash
npm run build
# or
yarn build
```

## API Integration

The frontend communicates with the backend API using Axios. The API integration is organized into separate modules:

- `authApi.ts`: Authentication-related API calls
- `resourcesApi.ts`: Resource-related API calls

The Axios instance is configured with interceptors for adding authentication tokens and handling errors.

## State Management

- **Authentication State**: Managed by the `AuthContext` using React Context API
- **Resource State**: Managed by React Query for efficient data fetching and caching

## Styling

The application uses CSS for styling, with a focus on responsive design and usability. The styles are organized into:

- `index.css`: Global styles
- `App.css`: App-specific styles
