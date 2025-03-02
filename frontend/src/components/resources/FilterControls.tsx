import React, { useState, useEffect } from 'react';
import { ResourceFilters } from '../../types/resource';
import { useAuth } from '../../contexts/AuthContext';

interface FilterControlsProps {
  filters: ResourceFilters;
  onChange: (filters: ResourceFilters) => void;
  showOwnerFilter?: boolean;
  onApply?: () => void;
}

const FilterControls: React.FC<FilterControlsProps> = ({
  filters,
  onChange,
  showOwnerFilter = true,
  onApply
}: FilterControlsProps) => {
  const { authState } = useAuth();
  const isAdmin = authState.user?.is_admin || false;
  const [localFilters, setLocalFilters] = useState<ResourceFilters>(filters);
  const [isApplying, setIsApplying] = useState(false);
  
  // Update local filters when props change
  useEffect(() => {
    setLocalFilters(filters);
  }, [filters]);
  
  // Handle input changes
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target as HTMLInputElement;
    
    let parsedValue: string | boolean | number | null = value;
    
    // Parse boolean values
    if (type === 'checkbox') {
      parsedValue = (e.target as HTMLInputElement).checked;
    }
    
    // Parse number values or null
    if (name === 'owner_id') {
      parsedValue = value === '' ? null : value === 'current' ? authState.user?.id || null : parseInt(value, 10);
    }
    
    // Update local filters
    setLocalFilters({
      ...localFilters,
      [name]: parsedValue,
    });
  };
  
  // Apply filters
  const applyFilters = () => {
    // Show loading state
    setIsApplying(true);
    
    try {
      console.log('Applying filters:', localFilters);
      
      // First update the parent component's state with the local filters
      onChange(localFilters);
      
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
      console.error('Error applying filters:', error);
      setIsApplying(false);
    }
  };
  
  // Reset filters
  const resetFilters = () => {
    // Show loading state
    setIsApplying(true);
    
    try {
      const resetValues: ResourceFilters = {
        search: '',
        is_public: null,
      };
      
      if (showOwnerFilter) {
        resetValues.owner_id = null;
      }
      
      console.log('Resetting filters to:', resetValues);
      
      setLocalFilters(resetValues);
      onChange(resetValues);
      
      if (onApply) {
        // Use setTimeout to ensure the state update has been processed
        setTimeout(() => {
          onApply();
          // Hide loading state after a short delay
          setTimeout(() => {
            setIsApplying(false);
          }, 300);
        }, 100);
      } else {
        // If no onApply callback, just hide the loading state
        setIsApplying(false);
      }
    } catch (error) {
      console.error('Error resetting filters:', error);
      setIsApplying(false);
    }
  };
  
  return (
    <div className="filter-controls">
      <div className="filter-control">
        <label htmlFor="search">Search</label>
        <input
          type="text"
          id="search"
          name="search"
          value={localFilters.search || ''}
          onChange={handleInputChange}
          placeholder="Search resources..."
        />
      </div>
      
      {showOwnerFilter && (
        <div className="filter-control">
          <label htmlFor="owner_id">Owner</label>
          <select
            id="owner_id"
            name="owner_id"
            value={localFilters.owner_id === null ? '' : 
                  localFilters.owner_id === authState.user?.id ? 'current' : 
                  localFilters.owner_id}
            onChange={handleInputChange}
          >
            <option value="">All Resources</option>
            <option value="current">My Resources</option>
            {isAdmin && <option value="shared">Shared Resources</option>}
          </select>
        </div>
      )}
      
      <div className="filter-control">
        <label htmlFor="is_public">Visibility</label>
        <select
          id="is_public"
          name="is_public"
          value={localFilters.is_public === null ? '' : localFilters.is_public ? 'true' : 'false'}
          onChange={(e) => {
            const value = e.target.value;
            // Cast to unknown first to avoid type error
            handleInputChange({
              ...e,
              target: {
                ...e.target,
                name: 'is_public',
                value: value === '' ? null : value === 'true',
              },
            } as unknown as React.ChangeEvent<HTMLSelectElement>);
          }}
        >
          <option value="">All Visibility</option>
          <option value="true">Public Only</option>
          <option value="false">Private Only</option>
        </select>
      </div>
      
      <div className="filter-actions">
        <button 
          onClick={applyFilters} 
          className="button"
          disabled={isApplying}
        >
          {isApplying ? (
            <>
              <span className="button-spinner"></span>
              Applying...
            </>
          ) : (
            'Apply Filters'
          )}
        </button>
        <button 
          onClick={resetFilters} 
          className="button button-secondary"
          disabled={isApplying}
        >
          Reset
        </button>
      </div>
    </div>
  );
};

export default FilterControls;
