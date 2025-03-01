import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import Pagination from '../../../components/shared/Pagination';
import { PageInfo } from '../../../types/common';

describe('Pagination Component', () => {
  const mockPageInfo: PageInfo = {
    total: 100,
    page: 2,
    pages: 10,
    has_next: true,
    has_prev: true,
  };
  
  const mockOnPageChange = jest.fn();
  const mockOnLimitChange = jest.fn();
  
  beforeEach(() => {
    jest.clearAllMocks();
  });
  
  test('renders pagination info correctly', () => {
    render(
      <Pagination
        pageInfo={mockPageInfo}
        onPageChange={mockOnPageChange}
        onLimitChange={mockOnLimitChange}
      />
    );
    
    // Check if pagination info is displayed correctly
    expect(screen.getByText(/Showing 11 to 20 of 100 items/i)).toBeInTheDocument();
  });
  
  test('renders correct number of page buttons', () => {
    render(
      <Pagination
        pageInfo={mockPageInfo}
        onPageChange={mockOnPageChange}
        onLimitChange={mockOnLimitChange}
      />
    );
    
    // Should show: 1, ..., 1, 2, 3, ..., 10
    expect(screen.getAllByRole('button').length).toBe(7); // 5 page buttons + prev + next
  });
  
  test('disables previous button on first page', () => {
    const firstPageInfo: PageInfo = {
      ...mockPageInfo,
      page: 1,
      has_prev: false,
    };
    
    render(
      <Pagination
        pageInfo={firstPageInfo}
        onPageChange={mockOnPageChange}
        onLimitChange={mockOnLimitChange}
      />
    );
    
    const prevButton = screen.getByText('Previous');
    expect(prevButton).toBeDisabled();
  });
  
  test('disables next button on last page', () => {
    const lastPageInfo: PageInfo = {
      ...mockPageInfo,
      page: 10,
      has_next: false,
    };
    
    render(
      <Pagination
        pageInfo={lastPageInfo}
        onPageChange={mockOnPageChange}
        onLimitChange={mockOnLimitChange}
      />
    );
    
    const nextButton = screen.getByText('Next');
    expect(nextButton).toBeDisabled();
  });
  
  test('calls onPageChange when page button is clicked', () => {
    render(
      <Pagination
        pageInfo={mockPageInfo}
        onPageChange={mockOnPageChange}
        onLimitChange={mockOnLimitChange}
      />
    );
    
    // Click on page 3
    fireEvent.click(screen.getByText('3'));
    expect(mockOnPageChange).toHaveBeenCalledWith(3);
  });
  
  test('calls onPageChange when previous button is clicked', () => {
    render(
      <Pagination
        pageInfo={mockPageInfo}
        onPageChange={mockOnPageChange}
        onLimitChange={mockOnLimitChange}
      />
    );
    
    fireEvent.click(screen.getByText('Previous'));
    expect(mockOnPageChange).toHaveBeenCalledWith(1);
  });
  
  test('calls onPageChange when next button is clicked', () => {
    render(
      <Pagination
        pageInfo={mockPageInfo}
        onPageChange={mockOnPageChange}
        onLimitChange={mockOnLimitChange}
      />
    );
    
    fireEvent.click(screen.getByText('Next'));
    expect(mockOnPageChange).toHaveBeenCalledWith(3);
  });
  
  test('calls onLimitChange when limit is changed', () => {
    render(
      <Pagination
        pageInfo={mockPageInfo}
        onPageChange={mockOnPageChange}
        onLimitChange={mockOnLimitChange}
      />
    );
    
    fireEvent.change(screen.getByRole('combobox'), { target: { value: '25' } });
    expect(mockOnLimitChange).toHaveBeenCalledWith(25);
  });
  
  test('does not render limit selector when onLimitChange is not provided', () => {
    render(
      <Pagination
        pageInfo={mockPageInfo}
        onPageChange={mockOnPageChange}
      />
    );
    
    expect(screen.queryByRole('combobox')).not.toBeInTheDocument();
  });
});
