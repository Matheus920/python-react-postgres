export interface Resource {
  id: number;
  name: string;
  description?: string;
  content?: string;
  meta_data?: string;
  is_public: boolean;
  owner_id: number;
}

export interface ResourceCreate {
  name: string;
  description?: string;
  content?: string;
  meta_data?: string;
  is_public?: boolean;
}

export interface ResourceUpdate {
  name?: string;
  description?: string;
  content?: string;
  meta_data?: string;
  is_public?: boolean;
}

export interface ResourceShare {
  user_id: number;
  permission_type: 'read' | 'write' | 'admin';
}

export interface ResourceFilters {
  owner_id?: number | null;
  is_public?: boolean | null;
  search?: string;
}

export interface ResourceSort {
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

export interface ResourceListResponse {
  items: Resource[];
  page_info: {
    total: number;
    page: number;
    pages: number;
    has_next: boolean;
    has_prev: boolean;
  };
}
