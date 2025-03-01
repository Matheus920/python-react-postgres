import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from 'react-query';
import { resourcesApi } from '../api/resourcesApi';
import { ResourceCreate, ResourceUpdate } from '../types/resource';

const ResourceCreateEditPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const isEditMode = !!id;
  const resourceId = isEditMode ? parseInt(id, 10) : 0;
  
  // Form state
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [content, setContent] = useState('');
  const [metaData, setMetaData] = useState('');
  const [isPublic, setIsPublic] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Fetch resource if in edit mode
  const { data: resource, isLoading } = useQuery(
    ['resource', resourceId],
    () => resourcesApi.getResource(resourceId),
    {
      enabled: isEditMode,
      staleTime: 30000, // Consider data fresh for 30 seconds
      onSuccess: (data) => {
        // Populate form with resource data
        setName(data.name);
        setDescription(data.description || '');
        setContent(data.content || '');
        setMetaData(data.meta_data || '');
        setIsPublic(data.is_public);
      },
      onError: (error) => {
        console.error('Failed to fetch resource:', error);
        setError('Failed to fetch resource. Please try again.');
      },
    }
  );
  
  // Validate form
  const validateForm = () => {
    if (!name.trim()) {
      setError('Name is required');
      return false;
    }
    
    if (metaData) {
      try {
        JSON.parse(metaData);
      } catch (error) {
        setError('Metadata must be valid JSON');
        return false;
      }
    }
    
    setError(null);
    return true;
  };
  
  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setIsSubmitting(true);
    
    try {
      const resourceData: ResourceCreate | ResourceUpdate = {
        name,
        description: description || undefined,
        content: content || undefined,
        meta_data: metaData || undefined,
        is_public: isPublic,
      };
      
      if (isEditMode) {
        await resourcesApi.updateResource(resourceId, resourceData as ResourceUpdate);
      } else {
        await resourcesApi.createResource(resourceData as ResourceCreate);
      }
      
      navigate('/resources');
    } catch (error) {
      console.error('Failed to save resource:', error);
      setError('Failed to save resource. Please try again.');
      setIsSubmitting(false);
    }
  };
  
  return (
    <div className="resource-form-page">
      <div className="page-header">
        <h1 className="page-title">
          {isEditMode ? 'Edit Resource' : 'Create Resource'}
        </h1>
      </div>
      
      {isLoading ? (
        <div className="loading-container">
          <div className="spinner"></div>
        </div>
      ) : (
        <div className="card">
          {error && <div className="error-message">{error}</div>}
          
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="name">Name *</label>
              <input
                type="text"
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                disabled={isSubmitting}
                required
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="description">Description</label>
              <textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                disabled={isSubmitting}
                rows={3}
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="content">Content</label>
              <textarea
                id="content"
                value={content}
                onChange={(e) => setContent(e.target.value)}
                disabled={isSubmitting}
                rows={5}
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="metaData">Metadata (JSON)</label>
              <textarea
                id="metaData"
                value={metaData}
                onChange={(e) => setMetaData(e.target.value)}
                disabled={isSubmitting}
                rows={5}
                placeholder="{}"
              />
              <small>Enter valid JSON data for metadata</small>
            </div>
            
            <div className="form-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={isPublic}
                  onChange={(e) => setIsPublic(e.target.checked)}
                  disabled={isSubmitting}
                />
                Public Resource
              </label>
            </div>
            
            <div className="form-actions">
              <button
                type="button"
                onClick={() => navigate('/resources')}
                className="button button-secondary"
                disabled={isSubmitting}
              >
                Cancel
              </button>
              <button
                type="submit"
                className="button"
                disabled={isSubmitting}
              >
                {isSubmitting
                  ? isEditMode
                    ? 'Saving...'
                    : 'Creating...'
                  : isEditMode
                    ? 'Save'
                    : 'Create'}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
};

export default ResourceCreateEditPage;
