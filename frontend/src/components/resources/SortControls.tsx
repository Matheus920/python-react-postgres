import React, { useState, useEffect } from 'react';
import { ResourceSort } from '../../types/resource';

interface SortControlsProps {
  sort: ResourceSort;
  onChange: (sort: ResourceSort) => void;
}

const SortControls: React.FC<SortControlsProps> = ({ sort, onChange }) => {
  const [localSort, setLocalSort] = useState<ResourceSort>(sort);
  
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
    </div>
  );
};

export default SortControls;
