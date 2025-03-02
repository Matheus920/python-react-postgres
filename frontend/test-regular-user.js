// Simple script to test the regular user authentication flow
const axios = require('axios');

// Base URL for the API
const BASE_URL = 'http://localhost:8000/api/v1';

// Regular user credentials
const REGULAR_USERNAME = 'regularuser';
const REGULAR_PASSWORD = 'password123';

// Function to test the authentication flow for a regular user
async function testRegularUserAuth() {
  try {
    console.log('Testing regular user authentication flow...');
    
    // Step 1: Login
    console.log('Step 1: Logging in as regular user...');
    const loginResponse = await axios.post(`${BASE_URL}/auth/login`, 
      `username=${REGULAR_USERNAME}&password=${REGULAR_PASSWORD}`,
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }
    );
    
    if (loginResponse.status !== 200) {
      console.error('Login failed:', loginResponse.status, loginResponse.statusText);
      return;
    }
    
    console.log('Login successful:', loginResponse.status);
    const token = loginResponse.data.access_token;
    console.log('Token:', token);
    
    // Step 2: Get current user
    console.log('\nStep 2: Getting current user...');
    const userResponse = await axios.get(`${BASE_URL}/users/me`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (userResponse.status !== 200) {
      console.error('Get current user failed:', userResponse.status, userResponse.statusText);
      return;
    }
    
    console.log('Get current user successful:', userResponse.status);
    console.log('User data:', userResponse.data);
    
    // Verify that the user is not an admin
    if (userResponse.data.is_admin) {
      console.error('Test failed: User is an admin, but should be a regular user');
      return;
    }
    
    console.log('Verified: User is a regular user (not an admin)');
    
    // Step 3: Get resources
    console.log('\nStep 3: Getting resources...');
    const resourcesResponse = await axios.get(`${BASE_URL}/resources/`, {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      params: {
        skip: 0,
        limit: 10,
        sort_by: 'name',
        sort_order: 'asc'
      },
      // Enable redirect following
      maxRedirects: 5,
      // Preserve headers during redirects
      withCredentials: true
    });
    
    if (resourcesResponse.status !== 200) {
      console.error('Get resources failed:', resourcesResponse.status, resourcesResponse.statusText);
      return;
    }
    
    console.log('Get resources successful:', resourcesResponse.status);
    console.log('Resources count:', resourcesResponse.data.items.length);
    console.log('Page info:', resourcesResponse.data.page_info);
    
    // Step 4: Get a specific public resource
    if (resourcesResponse.data.items.length > 0) {
      // Find a public resource that the user should have access to
      const publicResource = resourcesResponse.data.items.find(item => item.is_public === true);
      
      if (publicResource) {
        const resourceId = publicResource.id;
        console.log('\nStep 4: Getting public resource with ID', resourceId);
        
        const resourceResponse = await axios.get(`${BASE_URL}/resources/${resourceId}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          },
          // Enable redirect following
          maxRedirects: 5,
          // Preserve headers during redirects
          withCredentials: true
        });
        
        if (resourceResponse.status !== 200) {
          console.error('Get public resource failed:', resourceResponse.status, resourceResponse.statusText);
          return;
        }
        
        console.log('Get resource successful:', resourceResponse.status);
        console.log('Resource data:', resourceResponse.data);
      } else {
        console.log('\nNo public resources found to test individual resource access');
      }
    }
    
    // Step 5: Try to get a private resource that the user doesn't own (should fail)
    // We'll use a known resource ID that the regular user doesn't own
    const privateResourceId = 831; // This is a private resource owned by another user
    console.log('\nStep 5: Trying to get private resource with ID', privateResourceId, '(should fail)');
    
    try {
      const privateResourceResponse = await axios.get(`${BASE_URL}/resources/${privateResourceId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        },
        // Enable redirect following
        maxRedirects: 5,
        // Preserve headers during redirects
        withCredentials: true
      });
      
      console.error('Test failed: Regular user was able to access a private resource owned by another user');
      console.error('Response status:', privateResourceResponse.status);
      console.error('Response data:', privateResourceResponse.data);
      return;
    } catch (error) {
      if (error.response && error.response.status === 403) {
        console.log('Access denied as expected:', error.response.status);
        console.log('Error message:', error.response.data.detail);
        console.log('Permission test passed: Regular user cannot access private resources owned by other users');
      } else {
        console.error('Unexpected error:', error.message);
        if (error.response) {
          console.error('Response status:', error.response.status);
          console.error('Response data:', error.response.data);
        }
        return;
      }
    }
    
    console.log('\nAll tests passed successfully!');
  } catch (error) {
    console.error('Error during test:', error.message);
    if (error.response) {
      console.error('Response status:', error.response.status);
      console.error('Response data:', error.response.data);
    }
  }
}

// Run the test
testRegularUserAuth();
