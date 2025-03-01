import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import SortControls from '../../../components/resources/SortControls';
import { ResourceSort } from '../../../types/resource';

describe('SortControls Component', () => {
  const initialSort: ResourceSort = {
    sort_by: 'name',
    sort_order: 'asc',
  };
  
  const mockOnChange = jest.fn();
  
  beforeEach(() => {
    jest.clearAllMocks();
  });
  
  test('renders sort controls with default values', () => {
    render(
      <SortControls
        sort={initialSort}
        onChange={mockOnChange}
      />
    );
    
    // Check if sort controls are rendered with default values
    const sortBySelect = screen.getByLabelText(/Sort By/i);
    const sortOrderSelect = screen.getByLabelText(/Sort Order/i);
    
    expect(sortBySelect).toBeInTheDocument();
    expect(sortOrderSelect).toBeInTheDocument();
    expect(sortBySelect).toHaveValue('name');
    expect(sortOrderSelect).toHaveValue('asc');
  });
  
  test('renders sort controls with custom values', () => {
    const customSort: ResourceSort = {
      sort_by: 'id',
      sort_order: 'desc',
    };
    
    render(
      <SortControls
        sort={customSort}
        onChange={mockOnChange}
      />
    );
    
    // Check if sort controls are rendered with custom values
    const sortBySelect = screen.getByLabelText(/Sort By/i);
    const sortOrderSelect = screen.getByLabelText(/Sort Order/i);
    
    expect(sortBySelect).toHaveValue('id');
    expect(sortOrderSelect).toHaveValue('desc');
  });
  
  test('calls onChange when sort by is changed', () => {
    render(
      <SortControls
        sort={initialSort}
        onChange={mockOnChange}
      />
    );
    
    // Change sort by select
    const sortBySelect = screen.getByLabelText(/Sort By/i);
    fireEvent.change(sortBySelect, { target: { value: 'id' } });
    
    // Check if onChange was called with updated sort
    expect(mockOnChange).toHaveBeenCalledWith({
      ...initialSort,
      sort_by: 'id',
    });
  });
  
  test('calls onChange when sort order is changed', () => {
    render(
      <SortControls
        sort={initialSort}
        onChange={mockOnChange}
      />
    );
    
    // Change sort order select
    const sortOrderSelect = screen.getByLabelText(/Sort Order/i);
    fireEvent.change(sortOrderSelect, { target: { value: 'desc' } });
    
    // Check if onChange was called with updated sort
    expect(mockOnChange).toHaveBeenCalledWith({
      ...initialSort,
      sort_order: 'desc',
    });
  });
  
  test('renders all available sort by options', () => {
    render(
      <SortControls
        sort={initialSort}
        onChange={mockOnChange}
      />
    );
    
    // Get all options in the sort by select
    const sortBySelect = screen.getByLabelText(/Sort By/i);
    const options = Array.from(sortBySelect.querySelectorAll('option')).map(
      option => option.textContent
    );
    
    // Check if all expected options are present
    expect(options).toContain('Name');
    expect(options).toContain('ID');
    expect(options).toContain('Created Date');
    expect(options).toContain('Updated Date');
  });
  
  test('renders all available sort order options', () => {
    render(
      <SortControls
        sort={initialSort}
        onChange={mockOnChange}
      />
    );
    
    // Get all options in the sort order select
    const sortOrderSelect = screen.getByLabelText(/Sort Order/i);
    const options = Array.from(sortOrderSelect.querySelectorAll('option')).map(
      option => option.textContent
    );
    
    // Check if all expected options are present
    expect(options).toContain('Ascending');
    expect(options).toContain('Descending');
  });
});
