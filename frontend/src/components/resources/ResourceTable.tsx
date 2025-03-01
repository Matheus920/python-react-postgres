import React from 'react';
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
              <th>Visibility</th>
              <th>Owner ID</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {resources.map((resource) => (
              <tr key={resource.id}>
                <td>{resource.id}</td>
                <td>
                  <Link to={`/resources/${resource.id}`}>{resource.name}</Link>
                </td>
                <td>{resource.description || 'No description'}</td>
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
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default ResourceTable;
