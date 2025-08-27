import { useState, useCallback } from 'react';
import { SearchQuery, SearchResponse } from '../types/search';
import { apiClient } from '../services/apiClient';

interface UseSearchReturn {
  searchResults: SearchResponse | null;
  loading: boolean;
  error: string | null;
  search: (query: SearchQuery) => Promise<void>;
  clearResults: () => void;
}

export const useSearch = (): UseSearchReturn => {
  const [searchResults, setSearchResults] = useState<SearchResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const search = useCallback(async (query: SearchQuery) => {
    if (!query.query.trim()) {
      setError('検索クエリを入力してください');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const results = await apiClient.search(query);
      setSearchResults(results);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : '検索中にエラーが発生しました';
      setError(errorMessage);
      setSearchResults(null);
    } finally {
      setLoading(false);
    }
  }, []);

  const clearResults = useCallback(() => {
    setSearchResults(null);
    setError(null);
  }, []);

  return {
    searchResults,
    loading,
    error,
    search,
    clearResults,
  };
};
