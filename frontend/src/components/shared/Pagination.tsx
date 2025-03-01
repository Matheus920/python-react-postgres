import React from 'react';
import { PageInfo } from '../../types/common';

interface PaginationProps {
  pageInfo: PageInfo;
  onPageChange: (page: number) => void;
  onLimitChange?: (limit: number) => void;
}

const Pagination: React.FC<PaginationProps> = ({
  pageInfo,
  onPageChange,
  onLimitChange,
}) => {
  const { total, page, pages, has_next, has_prev } = pageInfo;
  
  // Calculate the range of items being displayed
  const itemsPerPage = Math.ceil(total / pages);
  const startItem = (page - 1) * itemsPerPage + 1;
  const endItem = Math.min(page * itemsPerPage, total);
  
  // Generate page numbers to display
  const getPageNumbers = () => {
    const pageNumbers = [];
    const maxPagesToShow = 5;
    
    if (pages <= maxPagesToShow) {
      // Show all pages if there are few
      for (let i = 1; i <= pages; i++) {
        pageNumbers.push(i);
      }
    } else {
      // Show a subset of pages with current page in the middle
      let startPage = Math.max(1, page - Math.floor(maxPagesToShow / 2));
      let endPage = Math.min(pages, startPage + maxPagesToShow - 1);
      
      // Adjust if we're near the end
      if (endPage - startPage + 1 < maxPagesToShow) {
        startPage = Math.max(1, endPage - maxPagesToShow + 1);
      }
      
      // Add first page
      if (startPage > 1) {
        pageNumbers.push(1);
        if (startPage > 2) pageNumbers.push('...');
      }
      
      // Add middle pages
      for (let i = startPage; i <= endPage; i++) {
        pageNumbers.push(i);
      }
      
      // Add last page
      if (endPage < pages) {
        if (endPage < pages - 1) pageNumbers.push('...');
        pageNumbers.push(pages);
      }
    }
    
    return pageNumbers;
  };

  return (
    <div className="pagination">
      <div className="pagination-info">
        Showing {startItem} to {endItem} of {total} items
      </div>
      
      <div className="pagination-controls">
        <button
          onClick={() => onPageChange(page - 1)}
          disabled={!has_prev}
          className="pagination-button"
        >
          Previous
        </button>
        
        {getPageNumbers().map((pageNum, index) => (
          <button
            key={index}
            onClick={() => typeof pageNum === 'number' && onPageChange(pageNum)}
            className={`pagination-button ${
              pageNum === page ? 'active' : ''
            } ${typeof pageNum !== 'number' ? 'ellipsis' : ''}`}
            disabled={typeof pageNum !== 'number'}
          >
            {pageNum}
          </button>
        ))}
        
        <button
          onClick={() => onPageChange(page + 1)}
          disabled={!has_next}
          className="pagination-button"
        >
          Next
        </button>
      </div>
      
      {onLimitChange && (
        <div className="pagination-limit">
          <select
            value={itemsPerPage}
            onChange={(e) => onLimitChange(Number(e.target.value))}
            className="pagination-select"
          >
            <option value={10}>10 per page</option>
            <option value={25}>25 per page</option>
            <option value={50}>50 per page</option>
            <option value={100}>100 per page</option>
          </select>
        </div>
      )}
    </div>
  );
};

export default Pagination;
