import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery, useQueryClient } from 'react-query';
import { resourcesApi } from '../api/resourcesApi';
import { useAuth } from '../contexts/AuthContext';
import Pagination from '../components/shared/Pagination';
import FilterControls from '../components/resources/FilterControls';
import SortControls from '../components/resources/SortControls';
import ResourceTable from '../components/resources/ResourceTable';
import { ResourceFilters, ResourceSort } from '../types/resource';
import { PageInfo } from '../types/common';

const ResourceListPage: React.FC = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { authState } = useAuth();
  const isAdmin = authState.user?.is_admin || false;
  
  // Use refs to track the current values for the query function
  const filtersRef = useRef<ResourceFilters>({
    owner_id: null,
    is_public: null,
    search: '',
  });
  
  const sortRef = useRef<ResourceSort>({
    sort_by: 'name',
    sort_order: 'asc',
  });
  
  // State for pagination, filtering, and sorting
  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(10);
  const [filters, setFilters] = useState<ResourceFilters>(filtersRef.current);
  const [sort, setSort] = useState<ResourceSort>(sortRef.current);
  
  // Add a state to track when to force refetch
  const [forceRefetch, setForceRefetch] = useState(0);
  
  // Update refs when state changes
  useEffect(() => {
    filtersRef.current = filters;
  }, [filters]);
  
  useEffect(() => {
    sortRef.current = sort;
  }, [sort]);
  
  // Calculate skip for pagination
  const skip = (page - 1) * limit;
  
  // Define the fetch function outside of useQuery to ensure it always uses the latest state
  const fetchResources = useCallback(async () => {
    console.log('Fetching resources with:', {
      skip,
      limit,
      filters: filtersRef.current,
      sort: sortRef.current
    });
    
    return resourcesApi.getResources(
      skip,
      limit,
      filtersRef.current,
      sortRef.current
    );
  }, [skip, limit, forceRefetch]); // Only depend on pagination and forceRefetch
  
  // Fetch resources with React Query
  const { data, isLoading, error, refetch } = useQuery(
    ['resources', skip, limit, forceRefetch],
    fetchResources,
    {
      keepPreviousData: true,
      staleTime: 0, // Always consider data stale to ensure refetching
      cacheTime: 0, // Don't cache the data
      refetchOnWindowFocus: false,
    }
  );
  
  // Reset to first page when filters or limit changes
  useEffect(() => {
    setPage(1);
  }, [filters, limit]);
  
  // Handle filter changes
  const handleFilterChange = useCallback((newFilters: ResourceFilters) => {
    console.log('Filter changed:', newFilters);
    setFilters(newFilters);
    filtersRef.current = newFilters;
  }, []);
  
  // Handle sort changes
  const handleSortChange = useCallback((newSort: ResourceSort) => {
    console.log('Sort changed:', newSort);
    setSort(newSort);
    sortRef.current = newSort;
  }, []);
  
  // Force refetch data
  const handleApplyChanges = useCallback(() => {
    console.log('Applying changes with:', {
      filters: filtersRef.current,
      sort: sortRef.current
    });
    
    // Increment forceRefetch to trigger a new query
    setForceRefetch(prev => prev + 1);
    
    // Clear the cache for this query
    queryClient.removeQueries(['resources']);
    
    // Manually refetch
    setTimeout(() => {
      refetch();
    }, 0);
  }, [refetch, queryClient]);
  
  // Handle pagination changes
  const handlePageChange = (newPage: number) => {
    setPage(newPage);
  };
  
  // Handle limit changes
  const handleLimitChange = (newLimit: number) => {
    setLimit(newLimit);
  };
  
  // Handle resource deletion
  const handleDeleteResource = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this resource?')) {
      try {
        await resourcesApi.deleteResource(id);
        refetch();
      } catch (error) {
        console.error('Failed to delete resource:', error);
        alert('Failed to delete resource. Please try again.');
      }
    }
  };
  
  // Create empty page info for when data is loading
  const emptyPageInfo: PageInfo = {
    total: 0,
    page: 1,
    pages: 1,
    has_next: false,
    has_prev: false,
  };
  
  return (
    <div className="resource-list-page">
      <div className="page-header">
        <h1 className="page-title">Resources</h1>
        <button
          onClick={() => navigate('/resources/create')}
          className="button"
        >
          Create Resource
        </button>
      </div>
      
      <div className="card">
        <FilterControls
          filters={filters}
          onChange={handleFilterChange}
          showOwnerFilter={authState.user?.is_admin}
          onApply={handleApplyChanges}
        />
        
        <SortControls 
          sort={sort} 
          onChange={handleSortChange} 
          onApply={handleApplyChanges}
        />
        
        {isLoading ? (
          <div className="loading-container">
            <div className="spinner"></div>
          </div>
        ) : error ? (
          <div className="error-message">
            <p>Error loading resources. Please try again.</p>
            <button onClick={() => refetch()} className="button">
              Retry
            </button>
          </div>
        ) : (
          <>
            <ResourceTable
              resources={data?.items || []}
              onDelete={handleDeleteResource}
              onRefresh={refetch}
            />
            
            <Pagination
              pageInfo={data?.page_info || emptyPageInfo}
              onPageChange={handlePageChange}
              onLimitChange={handleLimitChange}
            />
          </>
        )}
      </div>
    </div>
  );
};

export default ResourceListPage;
