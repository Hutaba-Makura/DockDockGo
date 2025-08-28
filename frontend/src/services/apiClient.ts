import { SearchQuery, SearchResponse, ErrorResponse } from '../types/search';

// 開発環境と本番環境で異なるデフォルトURLを使用
const API_BASE_URL = import.meta.env.VITE_PUBLIC_API_BASE || 
  (import.meta.env.DEV ? 'http://localhost:8000' : 'https://app-8c454da6-195d-408c-800e-23226514c8dc.ingress.apprun.sakura.ne.jp');

class ApiClient {
  private baseURL: string;

  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData: ErrorResponse = await response.json();
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('ネットワークエラーが発生しました');
    }
  }

  async search(query: SearchQuery): Promise<SearchResponse> {
    const params = new URLSearchParams({
      q: query.query,
      page: query.page?.toString() || '1',
      limit: query.limit?.toString() || '10',
    });

    return this.request<SearchResponse>(`/search?${params}`);
  }
}

export const apiClient = new ApiClient(API_BASE_URL);
