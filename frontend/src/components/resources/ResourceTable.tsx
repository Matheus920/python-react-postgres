import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Resource } from '../../types/resource';

interface ResourceTableProps {
  resources: Resource[];
  onDelete?: (id: number) => void;
  onRefresh?: () => void;
}

const ResourceTable: React.FC<ResourceTableProps> = ({
  resources,
  onDelete,
  onRefresh,
}) => {
  const [expandedMetadata, setExpandedMetadata] = useState<number | null>(null);

  // Format date string
  const formatDate = (dateString?: string) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
  };

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

  // Toggle metadata expansion
  const toggleMetadata = (resourceId: number) => {
    if (expandedMetadata === resourceId) {
      setExpandedMetadata(null);
    } else {
      setExpandedMetadata(resourceId);
    }
  };

  return (
    <div className="table-container">
      {resources.length === 0 ? (
        <div className="empty-state">
          <p>No resources found.</p>
          {onRefresh && (
            <button onClick={onRefresh} className="button">
              Refresh
            </button>
          )}
        </div>
      ) : (
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Description</th>
              <th>Metadata</th>
              <th>Visibility</th>
              <th>Owner ID</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {resources.map((resource) => (
              <React.Fragment key={resource.id}>
                <tr>
                  <td>{resource.id}</td>
                  <td>
                    <Link to={`/resources/${resource.id}`}>{resource.name}</Link>
                  </td>
                  <td>{resource.description || 'No description'}</td>
                  <td>
                    <button 
                      onClick={() => toggleMetadata(resource.id)} 
                      className={`button button-small ${expandedMetadata === resource.id ? 'button-primary' : 'button-secondary'}`}
                      aria-label={expandedMetadata === resource.id ? "Hide metadata" : "Show metadata"}
                    >
                      {expandedMetadata === resource.id ? 'Hide' : 'View'} Metadata
                    </button>
                  </td>
                  <td>
                    <span className={`badge ${resource.is_public ? 'badge-success' : 'badge-warning'}`}>
                      {resource.is_public ? 'Public' : 'Private'}
                    </span>
                  </td>
                  <td>{resource.owner_id}</td>
                  <td>
                    <div className="action-buttons">
                      <Link to={`/resources/${resource.id}`} className="button button-small">
                        View
                      </Link>
                      <Link to={`/resources/${resource.id}/edit`} className="button button-small">
                        Edit
                      </Link>
                      {onDelete && (
                        <button
                          onClick={() => onDelete(resource.id)}
                          className="button button-small button-danger"
                        >
                          Delete
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
                {expandedMetadata === resource.id && (
                  <tr className="metadata-row">
                    <td colSpan={7}>
                      <div className="metadata-container">
                        <h4>Resource Metadata</h4>
                        <div className="metadata-content">
                          {Object.entries(getMetadata(resource)).length > 0 ? (
                            <div className="metadata-grid">
                              {Object.entries(getMetadata(resource)).map(([key, value]) => (
                                <div key={key} className="metadata-item">
                                  <div className="metadata-key">{key}:</div>
                                  <div className="metadata-value">
                                    {typeof value === 'object' 
                                      ? (
                                        <pre className="metadata-json">
                                          {JSON.stringify(value, null, 2)}
                                        </pre>
                                      ) 
                                      : String(value)}
                                  </div>
                                </div>
                              ))}
                            </div>
                          ) : (
                            <div className="empty-metadata">
                              <p>No metadata available for this resource.</p>
                            </div>
                          )}
                        </div>
                      </div>
                    </td>
                  </tr>
                )}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default ResourceTable;
