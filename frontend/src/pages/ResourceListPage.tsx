import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from 'react-query';
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
  const { authState } = useAuth();
  const isAdmin = authState.user?.is_admin || false;
  
  // State for pagination, filtering, and sorting
  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(10);
  const [filters, setFilters] = useState<ResourceFilters>({
    owner_id: null,
    is_public: null,
    search: '',
  });
  const [sort, setSort] = useState<ResourceSort>({
    sort_by: 'name',
    sort_order: 'asc',
  });
  
  // Calculate skip for pagination
  const skip = (page - 1) * limit;
  
  // Fetch resources with React Query (includes caching)
  // For admin users, use getResources to see all resources
  // For regular users, the backend will automatically filter to show only resources they have access to
  const { data, isLoading, error, refetch } = useQuery(
    ['resources', skip, limit, filters, sort, isAdmin],
    () => resourcesApi.getResources(skip, limit, filters, sort),
    {
      keepPreviousData: true, // Keep previous data while loading new data
      staleTime: 30000, // Consider data fresh for 30 seconds
    }
  );
  
  // Reset to first page when filters or limit changes
  useEffect(() => {
    setPage(1);
  }, [filters, limit]);
  
  // Handle filter changes
  const handleFilterChange = (newFilters: ResourceFilters) => {
    setFilters(newFilters);
  };
  
  // Handle sort changes
  const handleSortChange = (newSort: ResourceSort) => {
    setSort(newSort);
  };
  
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
        />
        
        <SortControls sort={sort} onChange={handleSortChange} />
        
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
