import React, { useState, useEffect } from 'react';
import { ResourceSort } from '../../types/resource';

interface SortControlsProps {
  sort: ResourceSort;
  onChange: (sort: ResourceSort) => void;
  onApply?: () => void;
}

const SortControls: React.FC<SortControlsProps> = ({ 
  sort, 
  onChange, 
  onApply 
}: SortControlsProps) => {
  const [localSort, setLocalSort] = useState<ResourceSort>(sort);
  const [isApplying, setIsApplying] = useState(false);
  
  // Update local sort when props change
  useEffect(() => {
    setLocalSort(sort);
  }, [sort]);
  
  // Handle sort field change
  const handleSortByChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newSort = {
      ...localSort,
      sort_by: e.target.value,
    };
    setLocalSort(newSort);
    onChange(newSort);
  };
  
  // Handle sort order change
  const handleSortOrderChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newSort = {
      ...localSort,
      sort_order: e.target.value as 'asc' | 'desc',
    };
    setLocalSort(newSort);
    onChange(newSort);
  };
  
  // Apply sorting
  const handleApplySorting = () => {
    // Show loading state
    setIsApplying(true);
    
    try {
      console.log('Applying sorting:', localSort);
      
      // First update the parent component's state with the local sort
      onChange(localSort);
      
      // Then trigger the onApply callback to force a refetch
      if (onApply) {
        // Use setTimeout to ensure the state update has been processed
        setTimeout(() => {
          onApply();
          // Hide loading state after a short delay to ensure the user sees the feedback
          setTimeout(() => {
            setIsApplying(false);
          }, 300);
        }, 100);
      } else {
        // If no onApply callback, just hide the loading state
        setIsApplying(false);
      }
    } catch (error) {
      console.error('Error applying sorting:', error);
      setIsApplying(false);
    }
  };
  
  return (
    <div className="sort-controls">
      <div className="sort-control">
        <label htmlFor="sort_by">Sort By</label>
        <select
          id="sort_by"
          name="sort_by"
          value={localSort.sort_by || 'name'}
          onChange={handleSortByChange}
        >
          <option value="name">Name</option>
          <option value="id">ID</option>
          <option value="created_at">Created Date</option>
          <option value="updated_at">Updated Date</option>
        </select>
      </div>
      
      <div className="sort-control">
        <label htmlFor="sort_order">Sort Order</label>
        <select
          id="sort_order"
          name="sort_order"
          value={localSort.sort_order || 'asc'}
          onChange={handleSortOrderChange}
        >
          <option value="asc">Ascending</option>
          <option value="desc">Descending</option>
        </select>
      </div>
      
      <div className="sort-actions">
        <button 
          onClick={handleApplySorting} 
          className="button"
          aria-label="Apply sorting"
          disabled={isApplying}
        >
          {isApplying ? (
            <>
              <span className="button-spinner"></span>
              Applying...
            </>
          ) : (
            'Apply Sorting'
          )}
        </button>
      </div>
    </div>
  );
};

export default SortControls;
