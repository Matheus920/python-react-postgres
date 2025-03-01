import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import ResourceTable from '../../../components/resources/ResourceTable';
import { mockResources } from '../../setup';

// Wrap component with BrowserRouter for Link components
const renderWithRouter = (ui: React.ReactElement) => {
  return render(<BrowserRouter>{ui}</BrowserRouter>);
};

describe('ResourceTable Component', () => {
  const mockOnDelete = jest.fn();
  const mockOnRefresh = jest.fn();
  
  beforeEach(() => {
    jest.clearAllMocks();
  });
  
  test('renders resource table with data', () => {
    renderWithRouter(
      <ResourceTable
        resources={mockResources}
        onDelete={mockOnDelete}
        onRefresh={mockOnRefresh}
      />
    );
    
    // Check if table headers are rendered
    expect(screen.getByText('ID')).toBeInTheDocument();
    expect(screen.getByText('Name')).toBeInTheDocument();
    expect(screen.getByText('Description')).toBeInTheDocument();
    expect(screen.getByText('Visibility')).toBeInTheDocument();
    expect(screen.getByText('Owner ID')).toBeInTheDocument();
    expect(screen.getByText('Actions')).toBeInTheDocument();
    
    // Check if resource data is rendered
    expect(screen.getByText('Resource 1')).toBeInTheDocument();
    expect(screen.getByText('Resource 2')).toBeInTheDocument();
    expect(screen.getByText('Resource 3')).toBeInTheDocument();
    
    // Check if description is rendered
    expect(screen.getByText('Description for resource 1')).toBeInTheDocument();
    
    // Check if visibility badges are rendered
    const publicBadges = screen.getAllByText('Public');
    const privateBadges = screen.getAllByText('Private');
    expect(publicBadges.length).toBe(2); // Resource 1 and 3 are public
    expect(privateBadges.length).toBe(1); // Resource 2 is private
    
    // Check if action buttons are rendered
    const viewButtons = screen.getAllByText('View');
    const editButtons = screen.getAllByText('Edit');
    const deleteButtons = screen.getAllByText('Delete');
    expect(viewButtons.length).toBe(3);
    expect(editButtons.length).toBe(3);
    expect(deleteButtons.length).toBe(3);
  });
  
  test('renders empty state when no resources', () => {
    renderWithRouter(
      <ResourceTable
        resources={[]}
        onDelete={mockOnDelete}
        onRefresh={mockOnRefresh}
      />
    );
    
    // Check if empty state is rendered
    expect(screen.getByText('No resources found.')).toBeInTheDocument();
    expect(screen.getByText('Refresh')).toBeInTheDocument();
  });
  
  test('calls onRefresh when refresh button is clicked', () => {
    renderWithRouter(
      <ResourceTable
        resources={[]}
        onDelete={mockOnDelete}
        onRefresh={mockOnRefresh}
      />
    );
    
    // Click refresh button
    fireEvent.click(screen.getByText('Refresh'));
    expect(mockOnRefresh).toHaveBeenCalled();
  });
  
  test('calls onDelete when delete button is clicked and confirmed', () => {
    // Mock window.confirm to return true
    const originalConfirm = window.confirm;
    window.confirm = jest.fn(() => true);
    
    renderWithRouter(
      <ResourceTable
        resources={mockResources}
        onDelete={mockOnDelete}
        onRefresh={mockOnRefresh}
      />
    );
    
    // Click delete button for first resource
    const deleteButtons = screen.getAllByText('Delete');
    fireEvent.click(deleteButtons[0]);
    
    // Check if onDelete was called with correct resource id
    expect(mockOnDelete).toHaveBeenCalledWith(mockResources[0].id);
    
    // Restore original window.confirm
    window.confirm = originalConfirm;
  });
  
  test('does not call onDelete when delete is canceled', () => {
    // Mock window.confirm to return false
    const originalConfirm = window.confirm;
    window.confirm = jest.fn().mockReturnValue(false);
    
    renderWithRouter(
      <ResourceTable
        resources={mockResources}
        onDelete={mockOnDelete}
        onRefresh={mockOnRefresh}
      />
    );
    
    // Click delete button for first resource
    const deleteButtons = screen.getAllByText('Delete');
    fireEvent.click(deleteButtons[0]);
    
    // Check if onDelete was not called
    expect(mockOnDelete).not.toHaveBeenCalled();
    
    // Restore original window.confirm
    window.confirm = originalConfirm;
  });
  
  test('renders table without delete buttons when onDelete is not provided', () => {
    renderWithRouter(
      <ResourceTable
        resources={mockResources}
        onRefresh={mockOnRefresh}
      />
    );
    
    // Check if delete buttons are not rendered
    expect(screen.queryAllByText('Delete').length).toBe(0);
  });
  
  test('renders links to resource detail and edit pages', () => {
    renderWithRouter(
      <ResourceTable
        resources={mockResources}
        onDelete={mockOnDelete}
        onRefresh={mockOnRefresh}
      />
    );
    
    // Check if links are rendered with correct hrefs
    const resourceLinks = screen.getAllByText('Resource 1');
    expect(resourceLinks[0].closest('a')).toHaveAttribute('href', '/resources/1');
    
    const viewButtons = screen.getAllByText('View');
    expect(viewButtons[0].closest('a')).toHaveAttribute('href', '/resources/1');
    
    const editButtons = screen.getAllByText('Edit');
    expect(editButtons[0].closest('a')).toHaveAttribute('href', '/resources/1/edit');
  });
});
