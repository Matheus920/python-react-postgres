import '@testing-library/jest-dom';
import { rest } from 'msw';
import { setupServer } from 'msw/node';

// Make sure jest-dom matchers are available
import '@testing-library/jest-dom/extend-expect';

// Mock data
export const mockResources = [
  {
    id: 1,
    name: 'Resource 1',
    description: 'Description for resource 1',
    content: 'Content for resource 1',
    meta_data: '{"key": "value"}',
    is_public: true,
    owner_id: 1,
  },
  {
    id: 2,
    name: 'Resource 2',
    description: 'Description for resource 2',
    content: 'Content for resource 2',
    meta_data: '{"key": "value2"}',
    is_public: false,
    owner_id: 1,
  },
  {
    id: 3,
    name: 'Resource 3',
    description: 'Description for resource 3',
    content: 'Content for resource 3',
    meta_data: '{"key": "value3"}',
    is_public: true,
    owner_id: 2,
  },
];

export const mockPageInfo = {
  total: 3,
  page: 1,
  pages: 1,
  has_next: false,
  has_prev: false,
};

export const mockResourcesResponse = {
  items: mockResources,
  page_info: mockPageInfo,
};

// Mock server
export const server = setupServer(
  // Mock resources endpoint
  rest.get('/api/resources', (req, res, ctx) => {
    return res(ctx.json(mockResourcesResponse));
  }),
  
  // Mock single resource endpoint
  rest.get('/api/resources/:id', (req, res, ctx) => {
    const { id } = req.params;
    const resource = mockResources.find(r => r.id === parseInt(id as string, 10));
    
    if (resource) {
      return res(ctx.json(resource));
    }
    
    return res(ctx.status(404), ctx.json({ detail: 'Resource not found' }));
  }),
  
  // Mock create resource endpoint
  rest.post('/api/resources', (req, res, ctx) => {
    return res(ctx.status(201), ctx.json({
      ...req.body,
      id: 4,
      owner_id: 1,
    }));
  }),
  
  // Mock update resource endpoint
  rest.put('/api/resources/:id', (req, res, ctx) => {
    const { id } = req.params;
    const resourceIndex = mockResources.findIndex(r => r.id === parseInt(id as string, 10));
    
    if (resourceIndex !== -1) {
      return res(ctx.json({
        ...mockResources[resourceIndex],
        ...req.body,
      }));
    }
    
    return res(ctx.status(404), ctx.json({ detail: 'Resource not found' }));
  }),
  
  // Mock delete resource endpoint
  rest.delete('/api/resources/:id', (req, res, ctx) => {
    const { id } = req.params;
    const resource = mockResources.find(r => r.id === parseInt(id as string, 10));
    
    if (resource) {
      return res(ctx.json(resource));
    }
    
    return res(ctx.status(404), ctx.json({ detail: 'Resource not found' }));
  }),
  
  // Mock login endpoint
  rest.post('/api/auth/login', (req, res, ctx) => {
    return res(ctx.json({
      access_token: 'mock-token',
      token_type: 'bearer',
    }));
  }),
  
  // Mock register endpoint
  rest.post('/api/auth/register', (req, res, ctx) => {
    return res(ctx.status(201), ctx.json({
      id: 3,
      email: req.body.email,
      username: req.body.username,
      is_active: true,
      is_admin: false,
    }));
  }),
  
  // Mock current user endpoint
  rest.get('/api/users/me', (req, res, ctx) => {
    return res(ctx.json({
      id: 1,
      email: 'user@example.com',
      username: 'testuser',
      is_active: true,
      is_admin: false,
    }));
  }),
);

// Export the server so it can be imported in tests
export { rest, setupServer };

// Start server before all tests
beforeAll(() => server.listen({ onUnhandledRequest: 'bypass' }));

// Reset handlers after each test
afterEach(() => server.resetHandlers());

// Close server after all tests
afterAll(() => server.close());

// Add a test to make the file a valid test suite
test('Setup file is loaded', () => {
  expect(true).toBe(true);
});
