# Resource Management System - Frontend

This is the frontend application for the Resource Management System, built with React, TypeScript, and React Query.

## Features

- User authentication (login, register)
- Resource management (create, read, update, delete)
- Efficient data retrieval with pagination, filtering, and sorting
- Caching for improved performance
- Role-based access control (RBAC)
  - Admin users can access all resources
  - Regular users can only access their own resources or shared resources
- Enhanced UI with responsive design
- Proper error handling and loading states
- Consistent URL handling with trailing slashes

## Project Structure

```
frontend/
├── public/              # Static files
│   ├── index.html       # HTML template
│   ├── manifest.json    # Web app manifest
│   ├── favicon.ico      # Favicon
│   └── robots.txt       # Robots file
├── src/                 # Source code
│   ├── api/             # API integration
│   │   ├── authApi.ts   # Authentication API
│   │   └── resourcesApi.ts # Resources API
│   ├── components/      # React components
│   │   ├── auth/        # Authentication components
│   │   │   └── ProtectedRoute.tsx # Route protection component
│   │   ├── resources/   # Resource-related components
│   │   │   ├── FilterControls.tsx # Filtering component
│   │   │   ├── SortControls.tsx   # Sorting component
│   │   │   └── ResourceTable.tsx  # Resource display component
│   │   └── shared/      # Shared components
│   │       ├── Layout.tsx         # Layout component
│   │       └── Pagination.tsx     # Pagination component
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
- **LoginPage**: User login form with error handling
- **RegisterPage**: User registration form with validation
- **ProtectedRoute**: Route wrapper that requires authentication and handles redirects

### Resource Management

- **ResourceListPage**: Main page for viewing resources with pagination, filtering, and sorting
  - Adapts UI based on user role (admin vs. regular user)
  - Handles loading states and error handling
  - Implements efficient data fetching with React Query
- **ResourceDetailPage**: Page for viewing a single resource
  - Displays resource details including metadata
  - Provides actions for editing and deleting resources
- **ResourceCreateEditPage**: Page for creating and editing resources
  - Form validation and error handling
  - Metadata editing support
- **ResourceTable**: Table component for displaying resources
  - Expandable metadata view
  - Action buttons for view, edit, delete
  - Visual indicators for resource visibility
- **FilterControls**: Component for filtering resources
  - Search by name or description
  - Filter by owner (with special options for admin users)
  - Filter by visibility (public/private)
  - Loading states during filter application
- **SortControls**: Component for sorting resources
  - Sort by different fields (name, ID, created date, updated date)
  - Sort in ascending or descending order
  - Loading states during sort application
- **Pagination**: Component for paginating through resources
  - Page navigation controls
  - Items per page selection
  - Page information display

## Key Features

### Role-Based Access Control (RBAC)

The frontend implements role-based access control that works in conjunction with the backend:

- **Admin Users**: Can see all resources in the system
  - FilterControls component shows additional options for admin users
  - ResourceListPage adapts to show all resources for admin users
  - Admin users can access any resource detail page

- **Regular Users**: Can only see resources they own or have been shared with them
  - FilterControls component shows limited options for regular users
  - ResourceListPage only displays resources the user has access to
  - Attempting to access unauthorized resources results in access denied errors

### URL Handling and Redirects

The application implements proper URL handling to ensure consistent behavior:

- **Consistent URL Formats**: 
  - Collection routes use trailing slashes (e.g., `/resources/`)
  - ID-based routes don't use trailing slashes (e.g., `/resources/123`)

- **Enhanced Axios Configuration**:
  - Custom Axios instance with interceptors for authentication
  - Manual handling of redirects to preserve authentication headers
  - Proper error handling for 401 Unauthorized errors
  - Detailed logging for debugging

### Efficient Data Retrieval

The frontend implementation for User Story #1 focuses on efficient data retrieval with pagination, filtering, and sorting. Key features include:

1. **Pagination**: The `Pagination` component allows users to navigate through large datasets with ease.
2. **Filtering**: The `FilterControls` component provides options for filtering resources by various criteria.
3. **Sorting**: The `SortControls` component allows users to sort resources by different fields.
4. **Caching**: React Query is used for data fetching and caching, improving performance for frequently accessed data.
5. **Loading States**: Components display loading indicators during data fetching operations.
6. **Error Handling**: Comprehensive error handling with user-friendly error messages.

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Backend server running (see backend README)

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

### Testing RBAC Implementation

You can use the provided test scripts to verify the RBAC implementation:

```bash
# Test admin user access
node test-auth.js

# Test regular user access
node test-regular-user.js
```

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

The Axios instance is configured with interceptors for:
- Adding authentication tokens to requests
- Handling redirects properly to preserve authentication headers
- Handling errors with consistent error formatting
- Logging for debugging purposes

### URL Handling

The application uses consistent URL formats:
- Collection routes use trailing slashes (e.g., `/resources/`)
- ID-based routes don't use trailing slashes (e.g., `/resources/123`)

This is important for proper redirect handling and authentication header preservation.

## State Management

- **Authentication State**: Managed by the `AuthContext` using React Context API
  - Stores user information and authentication status
  - Provides login, logout, and token management functions
  - Persists authentication tokens in localStorage

- **Resource State**: Managed by React Query for efficient data fetching and caching
  - Automatic refetching on window focus
  - Caching for improved performance
  - Loading and error states

## Styling

The application uses CSS for styling, with a focus on responsive design and usability. The styles are organized into:

- `index.css`: Global styles
- `App.css`: App-specific styles

UI enhancements include:
- Enhanced button styling with visual feedback
- Better spacing between elements
- Improved form controls with focus and hover states
- Transitions and animations for smoother interactions
- Responsive design for better mobile experience
- Proper formatting for JSON metadata
