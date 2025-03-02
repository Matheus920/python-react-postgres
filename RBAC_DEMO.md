# Role-Based Access Control (RBAC) Demo

This document explains how to demonstrate the role-based access control (RBAC) features of the Resource Management System.

## Overview

The system implements two types of users with different permission levels:

1. **Admin Users**: Can access, modify, and manage all resources in the system, regardless of ownership.
2. **Regular Users**: Can only access resources they own or resources that have been explicitly shared with them.

## Test Users

The system includes two test users for demonstration purposes:

### Admin User
- Username: `testuser`
- Password: `password123`
- Role: Admin
- Capabilities: Can view, edit, delete, share, and unshare any resource in the system

### Regular User
- Username: `regularuser`
- Password: `password123`
- Role: Regular User
- Capabilities: Can only view, edit, delete, share, and unshare resources they own or resources shared with them

## Testing the RBAC Implementation

### Backend Testing

You can use the provided test scripts to verify the RBAC implementation:

1. **Test Admin Access**:
   ```bash
   cd backend
   python test_auth_resource.py 831
   ```
   This script logs in as the admin user and attempts to access a resource with ID 831, which is owned by another user. The test should pass, demonstrating that admin users can access any resource.

2. **Test Regular User Access**:
   ```bash
   cd frontend
   node test-regular-user.js
   ```
   This script logs in as the regular user and attempts to access a resource with ID 831, which is owned by another user. The test should fail with a 403 Forbidden error, demonstrating that regular users cannot access resources they don't own.

### Frontend Testing

You can also test the RBAC implementation through the frontend:

1. **Login as Admin User**:
   - Navigate to the login page
   - Enter username: `testuser` and password: `password123`
   - After logging in, you should be able to see all resources in the system
   - You should be able to view, edit, and delete any resource

2. **Login as Regular User**:
   - Navigate to the login page
   - Enter username: `regularuser` and password: `password123`
   - After logging in, you should only see resources owned by the regular user or shared with them
   - If you try to access a resource not owned by or shared with the regular user (e.g., by manually entering the URL), you should get an access denied error

## Implementation Details

The RBAC implementation is primarily handled in the `resource_service.py` file:

1. **Resource Listing**:
   - Admin users can see all resources with applied filters
   - Regular users can only see resources they own or resources shared with them

2. **Resource Access**:
   - Admin users can access any resource
   - Regular users can only access resources they own, public resources, or resources shared with them

3. **Resource Modification**:
   - Admin users can update any resource
   - Regular users can only update resources they own

4. **Resource Deletion**:
   - Admin users can delete any resource
   - Regular users can only delete resources they own

5. **Resource Sharing**:
   - Admin users can share any resource
   - Regular users can only share resources they own

## Troubleshooting

If you encounter issues with the RBAC implementation:

1. **Check User Roles**: Verify that the user has the correct role (admin or regular user)
2. **Check Resource Ownership**: Verify that the resource is owned by the correct user
3. **Check Resource Sharing**: Verify that the resource has been shared with the user if applicable
4. **Check Authentication**: Verify that the user is properly authenticated
5. **Check Authorization Headers**: Verify that the authorization headers are being properly sent and preserved during redirects
