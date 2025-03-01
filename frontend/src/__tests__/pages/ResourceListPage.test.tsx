import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import ResourceListPage from '../../pages/ResourceListPage';
import { AuthProvider } from '../../contexts/AuthContext';
import { mockResourcesResponse, server } from '../setup';
import { rest } from 'msw';

// Create a wrapper with all required providers
const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });
  
  return ({ children }: { children: React.ReactNode }) => (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          {children}
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  );
};

describe('ResourceListPage Component', () => {
  beforeEach(() => {
    // Reset handlers to default before each test
    server.resetHandlers();
  });
  
  test('renders loading state initially', async () => {
    render(<ResourceListPage />, { wrapper: createWrapper() });
    
    // Check if loading spinner is displayed
    expect(screen.getByText(/Resources/i)).toBeInTheDocument();
    expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();
  });
  
  test('renders resources after loading', async () => {
    render(<ResourceListPage />, { wrapper: createWrapper() });
    
    // Wait for resources to load
    await waitFor(() => {
      expect(screen.queryByTestId('loading-spinner')).not.toBeInTheDocument();
    });
    
    // Check if resources are displayed
    expect(screen.getByText('Resource 1')).toBeInTheDocument();
    expect(screen.getByText('Resource 2')).toBeInTheDocument();
    expect(screen.getByText('Resource 3')).toBeInTheDocument();
    
    // Check if pagination is displayed
    expect(screen.getByText(/Showing 1 to 3 of 3 items/i)).toBeInTheDocument();
  });
  
  test('renders error state when API fails', async () => {
    // Override the default handler to return an error
    server.use(
      rest.get('/api/resources', (req, res, ctx) => {
        return res(ctx.status(500), ctx.json({ detail: 'Server error' }));
      })
    );
    
    render(<ResourceListPage />, { wrapper: createWrapper() });
    
    // Wait for error message to appear
    await waitFor(() => {
      expect(screen.getByText(/Error loading resources/i)).toBeInTheDocument();
    });
    
    // Check if retry button is displayed
    expect(screen.getByText(/Retry/i)).toBeInTheDocument();
  });
  
  test('applies filters when filter controls are used', async () => {
    // Create a spy to track API calls
    const getSpy = jest.fn();
    server.use(
      rest.get('/api/resources', (req, res, ctx) => {
        getSpy(req.url.searchParams.toString());
        return res(ctx.json(mockResourcesResponse));
      })
    );
    
    render(<ResourceListPage />, { wrapper: createWrapper() });
    
    // Wait for resources to load
    await waitFor(() => {
      expect(screen.queryByTestId('loading-spinner')).not.toBeInTheDocument();
    });
    
    // Change search filter
    fireEvent.change(screen.getByLabelText(/Search/i), { target: { value: 'test search' } });
    
    // Change visibility filter
    fireEvent.change(screen.getByLabelText(/Visibility/i), { target: { value: 'true' } });
    
    // Click Apply Filters button
    fireEvent.click(screen.getByText(/Apply Filters/i));
    
    // Wait for refetch to happen
    await waitFor(() => {
      // Check if API was called with correct parameters
      expect(getSpy).toHaveBeenCalledWith(expect.stringContaining('search=test+search'));
      expect(getSpy).toHaveBeenCalledWith(expect.stringContaining('is_public=true'));
    });
  });
  
  test('applies sorting when sort controls are used', async () => {
    // Create a spy to track API calls
    const getSpy = jest.fn();
    server.use(
      rest.get('/api/resources', (req, res, ctx) => {
        getSpy(req.url.searchParams.toString());
        return res(ctx.json(mockResourcesResponse));
      })
    );
    
    render(<ResourceListPage />, { wrapper: createWrapper() });
    
    // Wait for resources to load
    await waitFor(() => {
      expect(screen.queryByTestId('loading-spinner')).not.toBeInTheDocument();
    });
    
    // Change sort by
    fireEvent.change(screen.getByLabelText(/Sort By/i), { target: { value: 'id' } });
    
    // Wait for refetch to happen
    await waitFor(() => {
      // Check if API was called with correct parameters
      expect(getSpy).toHaveBeenCalledWith(expect.stringContaining('sort_by=id'));
    });
    
    // Change sort order
    fireEvent.change(screen.getByLabelText(/Sort Order/i), { target: { value: 'desc' } });
    
    // Wait for refetch to happen
    await waitFor(() => {
      // Check if API was called with correct parameters
      expect(getSpy).toHaveBeenCalledWith(expect.stringContaining('sort_order=desc'));
    });
  });
  
  test('changes page when pagination controls are used', async () => {
    // Create a mock response with multiple pages
    const multiPageResponse = {
      items: mockResourcesResponse.items,
      page_info: {
        total: 30,
        page: 1,
        pages: 3,
        has_next: true,
        has_prev: false,
      },
    };
    
    // Create a spy to track API calls
    const getSpy = jest.fn();
    server.use(
      rest.get('/api/resources', (req, res, ctx) => {
        getSpy(req.url.searchParams.toString());
        return res(ctx.json(multiPageResponse));
      })
    );
    
    render(<ResourceListPage />, { wrapper: createWrapper() });
    
    // Wait for resources to load
    await waitFor(() => {
      expect(screen.queryByTestId('loading-spinner')).not.toBeInTheDocument();
    });
    
    // Click on page 2
    fireEvent.click(screen.getByText('2'));
    
    // Wait for refetch to happen
    await waitFor(() => {
      // Check if API was called with correct parameters
      expect(getSpy).toHaveBeenCalledWith(expect.stringContaining('skip=10'));
    });
    
    // Change items per page
    fireEvent.change(screen.getByRole('combobox', { name: /items per page/i }), { target: { value: '25' } });
    
    // Wait for refetch to happen
    await waitFor(() => {
      // Check if API was called with correct parameters
      expect(getSpy).toHaveBeenCalledWith(expect.stringContaining('limit=25'));
    });
  });
  
  test('navigates to create resource page when create button is clicked', async () => {
    render(<ResourceListPage />, { wrapper: createWrapper() });
    
    // Wait for resources to load
    await waitFor(() => {
      expect(screen.queryByTestId('loading-spinner')).not.toBeInTheDocument();
    });
    
    // Click create resource button
    fireEvent.click(screen.getByText(/Create Resource/i));
    
    // Check if navigation happened (we can't directly test this in JSDOM, but we can check if the button has the correct onClick handler)
    expect(window.location.pathname).toBe('/resources/create');
  });
});
