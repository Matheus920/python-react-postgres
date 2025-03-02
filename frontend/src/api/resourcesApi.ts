import { Message, Page } from "../types/common";
import {
  Resource,
  ResourceCreate,
  ResourceFilters,
  ResourceShare,
  ResourceSort,
  ResourceUpdate,
} from "../types/resource";
import axios from "../utils/axios";

export const resourcesApi = {
  /**
   * Get resources with pagination, filtering, and sorting
   */
  async getResources(
    skip = 0,
    limit = 10,
    filters: ResourceFilters = {},
    sort: ResourceSort = {}
  ): Promise<Page<Resource>> {
    const params = {
      skip,
      limit,
      ...filters,
      ...sort,
    };

    // Use URL with trailing slash to avoid redirect issues
    const response = await axios.get<Page<Resource>>("/resources/", { params });
    return response.data;
  },

  /**
   * Get resources owned by the current user
   */
  async getMyResources(skip = 0, limit = 10): Promise<Page<Resource>> {
    const params = { skip, limit };
    const response = await axios.get<Page<Resource>>("/resources/me/", {
      params,
    });
    return response.data;
  },

  /**
   * Get a single resource by ID
   */
  async getResource(id: number): Promise<Resource> {
    // Use URL without trailing slash for ID-based routes
    const response = await axios.get<Resource>(`/resources/${id}`);
    return response.data;
  },

  /**
   * Create a new resource
   */
  async createResource(data: ResourceCreate): Promise<Resource> {
    const response = await axios.post<Resource>("/resources/", data);
    return response.data;
  },

  /**
   * Update a resource
   */
  async updateResource(id: number, data: ResourceUpdate): Promise<Resource> {
    const response = await axios.put<Resource>(`/resources/${id}`, data);
    return response.data;
  },

  /**
   * Delete a resource
   */
  async deleteResource(id: number): Promise<Resource> {
    const response = await axios.delete<Resource>(`/resources/${id}`);
    return response.data;
  },

  /**
   * Share a resource with a user
   */
  async shareResource(id: number, shareData: ResourceShare): Promise<Message> {
    const response = await axios.post<Message>(
      `/resources/${id}/share`,
      shareData
    );
    return response.data;
  },

  /**
   * Unshare a resource from a user
   */
  async unshareResource(id: number, userId: number): Promise<Message> {
    const response = await axios.delete<Message>(
      `/resources/${id}/share/${userId}`
    );
    return response.data;
  },
};
