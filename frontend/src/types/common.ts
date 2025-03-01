export interface PageInfo {
  total: number;
  page: number;
  pages: number;
  has_next: boolean;
  has_prev: boolean;
}

export interface Page<T> {
  items: T[];
  page_info: PageInfo;
}

export interface PaginationParams {
  skip: number;
  limit: number;
}

export interface ApiError {
  status: number;
  message: string;
  detail?: string;
}

export interface Message {
  message: string;
}

export interface ApiResponse<T> {
  data?: T;
  error?: ApiError;
}

export interface SelectOption {
  value: string | number;
  label: string;
}
