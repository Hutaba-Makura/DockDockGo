// 検索クエリの型定義
export interface SearchQuery {
  query: string;
  page?: number;
  limit?: number;
}

// 検索結果の型定義
export interface SearchResult {
  id: string;
  title: string;
  description: string;
  url: string;
  score: number;
  publishedAt?: string;
}

// 検索レスポンスの型定義
export interface SearchResponse {
  results: SearchResult[];
  total: number;
  page: number;
  limit: number;
  query: string;
}

// エラーレスポンスの型定義
export interface ErrorResponse {
  error: string;
  message: string;
  status: number;
}
