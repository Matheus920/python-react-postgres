import React, { useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { useQuery } from 'react-query';
import { resourcesApi } from '../api/resourcesApi';
import { Resource } from '../types/resource';

const ResourceDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const resourceId = parseInt(id || '0', 10);
  
  // Fetch resource with React Query
  const { data: resource, isLoading, error, refetch } = useQuery(
    ['resource', resourceId],
    () => resourcesApi.getResource(resourceId),
    {
      enabled: !!resourceId,
      staleTime: 30000, // Consider data fresh for 30 seconds
    }
  );
  
  // Parse metadata
  const getMetadataValue = (resource: Resource, key: string) => {
    if (!resource.meta_data) return 'N/A';
    try {
      const metadata = JSON.parse(resource.meta_data);
      return metadata[key] || 'N/A';
    } catch (error) {
      return 'Invalid';
    }
  };
  
  // Get all metadata as an object
  const getMetadata = (resource: Resource) => {
    if (!resource.meta_data) return {};
    try {
      return JSON.parse(resource.meta_data);
    } catch (error) {
      return { error: 'Invalid metadata format' };
    }
  };
  
  // Handle resource deletion
  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this resource?')) {
      try {
        await resourcesApi.deleteResource(resourceId);
        navigate('/resources');
      } catch (error) {
        console.error('Failed to delete resource:', error);
        alert('Failed to delete resource. Please try again.');
      }
    }
  };
  
  return (
    <div className="resource-detail-page">
      <div className="page-header">
        <h1 className="page-title">Resource Details</h1>
        <div className="page-actions">
          <Link to="/resources" className="button button-secondary">
            Back to Resources
          </Link>
        </div>
      </div>
      
      {isLoading ? (
        <div className="loading-container">
          <div className="spinner"></div>
        </div>
      ) : error ? (
        <div className="error-message">
          <p>Error loading resource. Please try again.</p>
          <button onClick={() => refetch()} className="button">
            Retry
          </button>
        </div>
      ) : resource ? (
        <div className="card">
          <div className="resource-header">
            <h2>{resource.name}</h2>
            <div className="resource-actions">
              <Link to={`/resources/${resource.id}/edit`} className="button">
                Edit
              </Link>
              <button onClick={handleDelete} className="button button-danger">
                Delete
              </button>
            </div>
          </div>
          
          <div className="resource-meta">
            <span className={`badge ${resource.is_public ? 'badge-success' : 'badge-warning'}`}>
              {resource.is_public ? 'Public' : 'Private'}
            </span>
            <span className="resource-id">ID: {resource.id}</span>
            <span className="resource-owner">Owner ID: {resource.owner_id}</span>
          </div>
          
          {resource.description && (
            <div className="resource-section">
              <h3>Description</h3>
              <p>{resource.description}</p>
            </div>
          )}
          
          {resource.content && (
            <div className="resource-section">
              <h3>Content</h3>
              <div className="resource-content">
                {resource.content}
              </div>
            </div>
          )}
          
          {resource.meta_data && (
            <div className="resource-section">
              <h3>Metadata</h3>
              <div className="metadata-container">
                <div className="metadata-content">
                  {Object.entries(getMetadata(resource)).length > 0 ? (
                    <div className="metadata-grid">
                      {Object.entries(getMetadata(resource)).map(([key, value]) => (
                        <div key={key} className="metadata-item">
                          <div className="metadata-key">{key}:</div>
                          <div className="metadata-value">
                            {typeof value === 'object' 
                              ? JSON.stringify(value) 
                              : String(value)}
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p>No metadata available</p>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="empty-state">
          <p>Resource not found.</p>
          <Link to="/resources" className="button">
            Back to Resources
          </Link>
        </div>
      )}
    </div>
  );
};

export default ResourceDetailPage;
