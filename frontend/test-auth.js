// Simple script to test the authentication flow
const axios = require('axios');

// Base URL for the API
const BASE_URL = 'http://localhost:8000/api/v1';

// Test user credentials
const TEST_USERNAME = 'testuser';
const TEST_PASSWORD = 'password123';

// Function to test the authentication flow
async function testAuth() {
  try {
    console.log('Testing authentication flow...');
    
    // Step 1: Login
    console.log('Step 1: Logging in...');
    const loginResponse = await axios.post(`${BASE_URL}/auth/login`, 
      `username=${TEST_USERNAME}&password=${TEST_PASSWORD}`,
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
    
    // Step 4: Get a specific resource
    if (resourcesResponse.data.items.length > 0) {
      // Find a public resource that the user should have access to
      const publicResource = resourcesResponse.data.items.find(item => item.is_public === true);
      
      if (publicResource) {
        const resourceId = publicResource.id;
        console.log('\nStep 4: Getting public resource with ID', resourceId);
        
        const resourceResponse = await axios.get(`${BASE_URL}/resources/${resourceId}/`, {
          headers: {
            'Authorization': `Bearer ${token}`
          },
          // Enable redirect following
          maxRedirects: 5,
          // Preserve headers during redirects
          withCredentials: true
        });
        
        if (resourceResponse.status !== 200) {
          console.error('Get resource failed:', resourceResponse.status, resourceResponse.statusText);
          return;
        }
        
        console.log('Get resource successful:', resourceResponse.status);
        console.log('Resource data:', resourceResponse.data);
      } else {
        console.log('\nNo public resources found to test individual resource access');
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
testAuth();
